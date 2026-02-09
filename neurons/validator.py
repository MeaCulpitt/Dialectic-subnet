
```python
"""
Dialectic Validator Neuron

Adjudicates disputes between proposers and challengers.
Implements the weighted consensus mechanism.
"""

import argparse
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, List

import bittensor as bt

# Add parent to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dialectic.protocol import (
    TaskAssignment,
    TreeSubmission,
    ChallengeSubmission,
    DefenseSubmission,
    DisputeForAdjudication,
    VerdictAnnouncement,
    ReasoningTree,
    ReasoningNode,
    Verdict,
)
from dialectic.challenge import (
    ChallengeManager,
    DisputeStatus,
)
from dialectic.consensus import (
    ValidatorConsensus,
    ValidatorTier,
    ConsensusResult,
)
from dialectic.merkle import ReasoningMerkleTree


class Validator:
    """
    Validator neuron for Dialectic subnet.
    
    Responsibilities:
    - Assign tasks to proposers
    - Accept and route challenges
    - Adjudicate disputes via weighted consensus
    - Distribute rewards and slashes
    """
    
    def __init__(self, config: bt.config):
        self.config = config
        
        # Initialize bittensor objects
        self.wallet = bt.wallet(config=config)
        self.subtensor = bt.subtensor(config=config)
        self.metagraph = self.subtensor.metagraph(netuid=config.netuid)
        self.axon = bt.axon(wallet=self.wallet, config=config)
        
        # Validator components
        self.challenge_manager = ChallengeManager()
        self.consensus = ValidatorConsensus()
        
        # State
        self.submitted_trees: Dict[str, ReasoningTree] = {}
        self.task_counter = 0
        self.stake = config.stake if hasattr(config, 'stake') else 100.0
        self.tier = ValidatorTier(config.tier) if hasattr(config, 'tier') else ValidatorTier.SCOUT
        self.auto_verdict = config.auto_verdict if hasattr(config, 'auto_verdict') else False
        
        # Register self with consensus system
        self.consensus.register_validator(
            hotkey=self.wallet.hotkey.ss58_address,
            stake=self.stake,
            tier=self.tier
        )
        
        # Attach handlers to axon
        self._setup_axon()
        
        bt.logging.info(f"Validator initialized - tier: {self.tier.value}, stake: {self.stake}")
    
    def _setup_axon(self):
        """Set up axon with request handlers."""
        self.axon.attach(
            forward_fn=self.handle_tree_submission,
            blacklist_fn=self.blacklist_tree_submission,
        ).attach(
            forward_fn=self.handle_challenge,
            blacklist_fn=self.blacklist_challenge,
        ).attach(
            forward_fn=self.handle_defense,
            blacklist_fn=self.blacklist_defense,
        )
    
    # ========================================================================
    # Task Assignment
    # ========================================================================
    
    async def assign_task(self, domain: str, prompt: str) -> TaskAssignment:
        """Create and broadcast a new task assignment."""
        self.task_counter += 1
        task_id = f"dt_{datetime.utcnow().strftime('%Y%m%d_%H%M')}_{self.task_counter}"
        
        task = TaskAssignment(
            task_id=task_id,
            domain=domain,
            prompt=prompt,
            constraints={
                "max_depth": 5,
                "min_nodes": 4,
                "evidence_required": True
            },
            deadline=(datetime.utcnow() + timedelta(hours=6)).isoformat(),
            base_reward=0.5
        )
        
        return task
    
    # ========================================================================
    # Submission Handling
    # ========================================================================
    
    async def handle_tree_submission(self, synapse: TreeSubmission) -> TreeSubmission:
        """Process a reasoning tree submission from a proposer."""
        bt.logging.info(f"Received tree submission for task {synapse.task_id}")
        
        try:
            # Validate the submission
            is_valid, error = self._validate_tree(synapse.tree)
            
            if not is_valid:
                synapse.accepted = False
                synapse.rejection_reason = error
                return synapse
            
            # Verify Merkle commitment
            if not self._verify_merkle(synapse.tree):
                synapse.accepted = False
                synapse.rejection_reason = "Invalid Merkle commitment"
                return synapse
            
            # Store the tree
            synapse.tree.submitted_at = datetime.utcnow().isoformat()
            self.submitted_trees[synapse.task_id] = synapse.tree
            
            synapse.accepted = True
            bt.logging.info(f"Tree accepted for task {synapse.task_id}")
            
        except Exception as e:
            bt.logging.error(f"Error handling tree submission: {e}")
            synapse.accepted = False
            synapse.rejection_reason = str(e)
        
        return synapse
    
    def _validate_tree(self, tree: ReasoningTree) -> tuple[bool, Optional[str]]:
        """Validate a reasoning tree structure."""
        if not tree.root:
            return False, "Tree has no root node"
        
        if not tree.merkle_root:
            return False, "Tree has no Merkle commitment"
        
        if tree.stake < 10:  # Minimum stake
            return False, f"Stake {tree.stake} below minimum 10 TAO"
        
        # Check node structure
        node_ids = {tree.root.id}
        for node in tree.nodes:
            node_ids.add(node.id)
        
        # Verify all child references are valid
        for node in [tree.root] + tree.nodes:
            for child_id in node.children:
                if child_id not in node_ids:
                    return False, f"Invalid child reference: {child_id}"
        
        return True, None
    
    def _verify_merkle(self, tree: ReasoningTree) -> bool:
        """Verify the Merkle commitment of a tree."""
        merkle_tree = ReasoningMerkleTree()
        
        all_nodes = [tree.root.dict() if hasattr(tree.root, 'dict') else tree.root.__dict__]
        all_nodes.extend([n.dict() if hasattr(n, 'dict') else n.__dict__ for n in tree.nodes])
        
        computed_root = merkle_tree.build_from_reasoning_tree(all_nodes)
        
        return computed_root == tree.merkle_root
    
    def blacklist_tree_submission(self, synapse: TreeSubmission) -> tuple[bool, str]:
        """Blacklist check for tree submissions."""
        # Allow all for now
        return False, ""
    
    # ========================================================================
    # Challenge Handling
    # ========================================================================
    
    async def handle_challenge(self, synapse: ChallengeSubmission) -> ChallengeSubmission:
        """Process a challenge submission from a challenger."""
        bt.logging.info(f"Received challenge on task {synapse.task_id}, node {synapse.target_node}")
        
        try:
            # Get the tree being challenged
            tree = self.submitted_trees.get(synapse.task_id)
            if not tree:
                synapse.accepted = False
                return synapse
            
            # Validate the challenge
            is_valid, error = self.challenge_manager.validate_challenge(synapse, tree)
            
            if not is_valid:
                synapse.accepted = False
                bt.logging.warning(f"Challenge rejected: {error}")
                return synapse
            
            # Create dispute
            dispute = self.challenge_manager.create_dispute(synapse, tree)
            
            synapse.accepted = True
            synapse.dispute_id = dispute.dispute_id
            
            bt.logging.info(f"Challenge accepted, dispute created: {dispute.dispute_id}")
            
            # Notify proposer (async)
            asyncio.create_task(self.notify_proposer_of_challenge(tree, dispute))
            
        except Exception as e:
            bt.logging.error(f"Error handling challenge: {e}")
            synapse.accepted = False
        
        return synapse
    
    async def notify_proposer_of_challenge(self, tree: ReasoningTree, dispute):
        """Notify the proposer that their tree has been challenged."""
        # In practice, would send synapse to proposer's axon
        bt.logging.info(f"Notifying proposer {tree.proposer_hotkey} of challenge {dispute.dispute_id}")
    
    def blacklist_challenge(self, synapse: ChallengeSubmission) -> tuple[bool, str]:
        """Blacklist check for challenges."""
        return False, ""
    
    # ========================================================================
    # Defense Handling
    # ========================================================================
    
    async def handle_defense(self, synapse: DefenseSubmission) -> DefenseSubmission:
        """Process a defense submission from a proposer."""
        bt.logging.info(f"Received defense for dispute {synapse.dispute_id}")
        
        try:
            success, error = self.challenge_manager.submit_defense(
                synapse.dispute_id,
                synapse
            )
            
            synapse.accepted = success
            
            if success:
                bt.logging.info(f"Defense accepted for dispute {synapse.dispute_id}")
                # Trigger adjudication
                asyncio.create_task(self.initiate_adjudication(synapse.dispute_id))
            else:
                bt.logging.warning(f"Defense rejected: {error}")
            
        except Exception as e:
            bt.logging.error(f"Error handling defense: {e}")
            synapse.accepted = False
        
        return synapse
    
    def blacklist_defense(self, synapse: DefenseSubmission) -> tuple[bool, str]:
        """Blacklist check for defenses."""
        return False, ""
    
    # ========================================================================
    # Adjudication
    # ========================================================================
    
    async def initiate_adjudication(self, dispute_id: str):
        """Initiate the adjudication process for a dispute."""
        dispute = self.challenge_manager.get_dispute(dispute_id)
        if not dispute:
            bt.logging.error(f"Dispute {dispute_id} not found for adjudication")
            return
        
        # Get the tree and contested node
        tree = self.submitted_trees.get(dispute.task_id)
        if not tree:
            bt.logging.error(f"Tree not found for dispute {dispute_id}")
            return
        
        # Find the contested node
        contested_node = None
        if tree.root.id == dispute.target_node_id:
            contested_node = tree.root
        else:
            for node in tree.nodes:
                if node.id == dispute.target_node_id:
                    contested_node = node
                    break
        
        if not contested_node:
            bt.logging.error(f"Contested node {dispute.target_node_id} not found")
            return
        
        # Create adjudication synapse
        adjudication = DisputeForAdjudication(
            dispute_id=dispute_id,
            task_id=dispute.task_id,
            contested_node=contested_node,
            challenge=ChallengeSubmission(
                task_id=dispute.task_id,
                target_node=dispute.target_node_id,
                attack_type=dispute.attack_type,
                argument=dispute.challenge_argument,
                stake=dispute.challenger_stake,
                challenger_hotkey=dispute.challenger_hotkey
            ),
            defense=dispute.defense,
            proposer_reputation=1.0,  # Would look up from reputation system
            challenger_reputation=1.0
        )
        
        # Assign validators to adjudicate
        assigned = self.consensus.assign_dispute(
            dispute_id=dispute_id,
            dispute=adjudication,
            num_validators=5
        )
        
        bt.logging.info(f"Assigned {len(assigned)} validators to adjudicate {dispute_id}")
        
        # If auto_verdict enabled, submit our own vote
        if self.auto_verdict:
            verdict = await self.generate_verdict(adjudication)
            self.consensus.submit_vote(
                dispute_id=dispute_id,
                validator_hotkey=self.wallet.hotkey.ss58_address,
                verdict=verdict["verdict"],
                confidence=verdict["confidence"],
                reasoning=verdict["reasoning"]
            )
    
    async def generate_verdict(self, dispute: DisputeForAdjudication) -> Dict:
        """
        Generate a verdict for a dispute.
        
        Override for sophisticated adjudication logic.
        """
        # Placeholder - in practice would:
        # 1. Verify the challenger's evidence
        # 2. Evaluate the proposer's defense
        # 3. Check logical validity
        # 4. Determine verdict with confidence
        
        # Simple heuristic: if defense exists and has evidence, lean toward rejection
        if dispute.defense and dispute.defense.evidence:
            return {
                "verdict": Verdict.CHALLENGE_REJECTED,
                "confidence": 0.6,
                "reasoning": "Defense provided counter-evidence"
            }
        elif dispute.defense and dispute.defense.defense_type.value == "concede":
            return {
                "verdict": Verdict.CHALLENGE_UPHELD,
                "confidence": 0.9,
                "reasoning": "Proposer conceded the challenge"
            }
        else:
            return {
                "verdict": Verdict.PARTIAL,
                "confidence": 0.5,
                "reasoning": "Insufficient information for clear verdict"
            }
    
    async def finalize_disputes(self):
        """Check and finalize any disputes ready for resolution."""
        # Check for expired defense windows
        expired = self.challenge_manager.check_expired_defenses()
        for dispute_id in expired:
            bt.logging.info(f"Defense window expired for {dispute_id}")
        
        # Check for disputes ready for consensus
        pending = self.challenge_manager.get_pending_adjudication()
        for dispute in pending:
            result = self.consensus.finalize_dispute(dispute.dispute_id)
            if result and result.consensus_reached:
                # Apply resolution
                resolution = self.challenge_manager.resolve_dispute(
                    dispute.dispute_id,
                    result.final_verdict,
                    result.weighted_score
                )
                
                # Announce verdict
                await self.announce_verdict(dispute.dispute_id, result, resolution)
    
    async def announce_verdict(
        self, 
        dispute_id: str, 
        result: ConsensusResult,
        resolution: Dict
    ):
        """Announce the final verdict to the network."""
        announcement = VerdictAnnouncement(
            dispute_id=dispute_id,
            final_verdict=result.final_verdict,
            weighted_score=result.weighted_score,
            proposer_impact={
                "payout": resolution.get("proposer_payout", 0),
                "reputation_delta": resolution.get("proposer_reputation_delta", 0)
            },
            challenger_impact={
                "payout": resolution.get("challenger_payout", 0),
                "reputation_delta": resolution.get("challenger_reputation_delta", 0)
            },
            participating_validators=result.participating_validators
        )
        
        bt.logging.info(f"Verdict announced for {dispute_id}: {result.final_verdict.value}")
        
        # Broadcast to network (implementation depends on subnet design)
    
    # ========================================================================
    # Main Loop
    # ========================================================================
    
    async def run(self):
        """Main loop for the validator."""
        bt.logging.info("Starting validator main loop...")
        
        # Start axon
        self.axon.serve(netuid=self.config.netuid, subtensor=self.subtensor)
        self.axon.start()
        
        bt.logging.info(f"Axon serving on port {self.config.axon.port}")
        
        while True:
            try:
                # Sync metagraph
                self.metagraph.sync()
                
                # Finalize any ready disputes
                await self.finalize_disputes()
                
                # Sleep between iterations
                await asyncio.sleep(12)  # One block
                
            except KeyboardInterrupt:
                bt.logging.info("Validator shutting down...")
                break
            except Exception as e:
                bt.logging.error(f"Error in main loop: {e}")
                await asyncio.sleep(12)
        
        self.axon.stop()


def get_config():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Dialectic Validator Neuron")
    
    parser.add_argument("--netuid", type=int, required=True, help="Subnet UID")
    parser.add_argument("--stake", type=float, default=100.0, help="Validator stake")
    parser.add_argument("--tier", type=str, default="scout", choices=["scout", "auditor", "arbiter"])
    parser.add_argument("--auto_verdict", action="store_true", help="Automatically generate verdicts")
    parser.add_argument("--domains", type=str, help="Comma-separated domain specializations")
    
    # Add bittensor args
    bt.wallet.add_args(parser)
    bt.subtensor.add_args(parser)
    bt.axon.add_args(parser)
    bt.logging.add_args(parser)
    
    config = bt.config(parser)
    return config


def main():
    config = get_config()
    bt.logging(config=config)
    
    validator = Validator(config)
    asyncio.run(validator.run())


if __name__ == "__main__":
    main()
```

---

And finally `requirements.txt`:

```
# Dialectic Subnet Requirements

# Core
bittensor>=7.0.0

# Data validation
pydantic>=2.0.0

# Async support
aiohttp>=3.9.0

# Utilities
python-dateutil>=2.8.0
```

---
