
```python
"""
Challenge Detection and Defense Protocol

Handles:
- Challenge validation and acceptance
- Defense window management
- Stake calculations
- Challenge-defense resolution
"""

import time
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

from .protocol import (
    AttackType, 
    DefenseType, 
    Verdict,
    ChallengeSubmission,
    DefenseSubmission,
    ReasoningTree,
    ATTACK_MULTIPLIERS
)


# ============================================================================
# Constants
# ============================================================================

CHALLENGE_WINDOW_HOURS = 6      # Time to challenge a tree after submission
DEFENSE_WINDOW_HOURS = 2        # Time to defend after challenge
MIN_CHALLENGE_STAKE_RATIO = 0.1 # Min challenge stake = 10% of proposer stake

# Slash rates
PROPOSER_SLASH_RATE = 0.30      # 30% of proposer stake on successful challenge
CHALLENGER_SLASH_RATE = 0.50    # 50% of challenger stake on failed challenge


class DisputeStatus(str, Enum):
    """Status of a dispute."""
    PENDING_DEFENSE = "pending_defense"
    PENDING_ADJUDICATION = "pending_adjudication"
    RESOLVED = "resolved"
    EXPIRED = "expired"


@dataclass
class Dispute:
    """Active dispute between proposer and challenger."""
    dispute_id: str
    task_id: str
    target_node_id: str
    
    # Participants
    proposer_hotkey: str
    challenger_hotkey: str
    
    # Stakes
    proposer_stake: float
    challenger_stake: float
    
    # Challenge details
    attack_type: AttackType
    challenge_argument: str
    challenge_evidence: Optional[Dict] = None
    
    # Defense details
    defense: Optional[DefenseSubmission] = None
    defense_deadline: Optional[datetime] = None
    
    # Resolution
    status: DisputeStatus = DisputeStatus.PENDING_DEFENSE
    verdict: Optional[Verdict] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    
    # Calculated outcomes
    proposer_payout: float = 0.0
    challenger_payout: float = 0.0
    proposer_reputation_delta: float = 0.0
    challenger_reputation_delta: float = 0.0


class ChallengeManager:
    """
    Manages the challenge detection and defense protocol.
    
    Responsibilities:
    - Validate incoming challenges
    - Track defense windows
    - Calculate stake movements
    - Coordinate with validators for adjudication
    """
    
    def __init__(self):
        self.disputes: Dict[str, Dispute] = {}
        self.tree_challenges: Dict[str, List[str]] = {}  # task_id -> dispute_ids
        self.dispute_counter = 0
    
    def validate_challenge(
        self,
        challenge: ChallengeSubmission,
        tree: ReasoningTree
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate an incoming challenge.
        
        Checks:
        - Target node exists in tree
        - Challenge stake meets minimum
        - Tree is still in challenge window
        - Node hasn't already been challenged
        
        Returns:
            (is_valid, error_message)
        """
        # Check target node exists
        node_ids = [tree.root.id] + [n.id for n in tree.nodes]
        if challenge.target_node not in node_ids:
            return False, f"Target node {challenge.target_node} not found in tree"
        
        # Check minimum stake
        min_stake = tree.stake * MIN_CHALLENGE_STAKE_RATIO
        if challenge.stake < min_stake:
            return False, f"Challenge stake {challenge.stake} below minimum {min_stake}"
        
        # Check challenge window
        if tree.submitted_at:
            submitted = datetime.fromisoformat(tree.submitted_at)
            window_end = submitted + timedelta(hours=CHALLENGE_WINDOW_HOURS)
            if datetime.utcnow() > window_end:
                return False, "Challenge window has closed"
        
        # Check for duplicate challenges on same node
        task_disputes = self.tree_challenges.get(tree.task_id, [])
        for dispute_id in task_disputes:
            dispute = self.disputes.get(dispute_id)
            if dispute and dispute.target_node_id == challenge.target_node:
                if dispute.status != DisputeStatus.RESOLVED:
                    return False, f"Node {challenge.target_node} already has active challenge"
        
        return True, None
    
    def create_dispute(
        self,
        challenge: ChallengeSubmission,
        tree: ReasoningTree
    ) -> Dispute:
        """Create a new dispute from a validated challenge."""
        self.dispute_counter += 1
        dispute_id = f"disp_{tree.task_id}_{self.dispute_counter}"
        
        dispute = Dispute(
            dispute_id=dispute_id,
            task_id=tree.task_id,
            target_node_id=challenge.target_node,
            proposer_hotkey=tree.proposer_hotkey,
            challenger_hotkey=challenge.challenger_hotkey,
            proposer_stake=tree.stake,
            challenger_stake=challenge.stake,
            attack_type=challenge.attack_type,
            challenge_argument=challenge.argument,
            challenge_evidence=challenge.evidence.dict() if challenge.evidence else None,
            defense_deadline=datetime.utcnow() + timedelta(hours=DEFENSE_WINDOW_HOURS),
            status=DisputeStatus.PENDING_DEFENSE
        )
        
        self.disputes[dispute_id] = dispute
        
        if tree.task_id not in self.tree_challenges:
            self.tree_challenges[tree.task_id] = []
        self.tree_challenges[tree.task_id].append(dispute_id)
        
        return dispute
    
    def submit_defense(
        self,
        dispute_id: str,
        defense: DefenseSubmission
    ) -> Tuple[bool, Optional[str]]:
        """
        Process a defense submission.
        
        Returns:
            (success, error_message)
        """
        dispute = self.disputes.get(dispute_id)
        if not dispute:
            return False, f"Dispute {dispute_id} not found"
        
        if dispute.status != DisputeStatus.PENDING_DEFENSE:
            return False, f"Dispute not accepting defenses (status: {dispute.status})"
        
        if datetime.utcnow() > dispute.defense_deadline:
            return False, "Defense window has expired"
        
        dispute.defense = defense
        dispute.status = DisputeStatus.PENDING_ADJUDICATION
        
        return True, None
    
    def check_expired_defenses(self) -> List[str]:
        """
        Check for disputes where defense window expired.
        
        Returns list of dispute IDs that auto-resolved (no defense).
        """
        expired = []
        now = datetime.utcnow()
        
        for dispute_id, dispute in self.disputes.items():
            if dispute.status == DisputeStatus.PENDING_DEFENSE:
                if dispute.defense_deadline and now > dispute.defense_deadline:
                    # No defense submitted - auto-resolve for challenger
                    self._resolve_no_defense(dispute)
                    expired.append(dispute_id)
        
        return expired
    
    def _resolve_no_defense(self, dispute: Dispute):
        """Resolve a dispute where proposer didn't defend."""
        dispute.status = DisputeStatus.RESOLVED
        dispute.verdict = Verdict.CHALLENGE_UPHELD
        dispute.resolved_at = datetime.utcnow()
        
        # Challenger gets full reward + bonus for no-show
        multiplier = ATTACK_MULTIPLIERS[dispute.attack_type]
        base_reward = dispute.challenger_stake * multiplier
        
        # Proposer max slash on no-defense
        proposer_slash = min(
            dispute.proposer_stake * (PROPOSER_SLASH_RATE * 1.5),  # 45% on no-show
            dispute.proposer_stake
        )
        
        dispute.challenger_payout = base_reward + proposer_slash
        dispute.proposer_payout = -proposer_slash
        dispute.proposer_reputation_delta = -0.15  # Heavy rep hit
        dispute.challenger_reputation_delta = 0.05
    
    def resolve_dispute(
        self,
        dispute_id: str,
        verdict: Verdict,
        confidence: float = 1.0
    ) -> Dict:
        """
        Resolve a dispute with a validator verdict.
        
        Args:
            dispute_id: The dispute to resolve
            verdict: The validator consensus verdict
            confidence: Confidence level of the verdict (0-1)
            
        Returns:
            Resolution summary with stake/reputation changes
        """
        dispute = self.disputes.get(dispute_id)
        if not dispute:
            return {"error": f"Dispute {dispute_id} not found"}
        
        dispute.status = DisputeStatus.RESOLVED
        dispute.verdict = verdict
        dispute.resolved_at = datetime.utcnow()
        
        if verdict == Verdict.CHALLENGE_UPHELD:
            self._resolve_challenger_wins(dispute, confidence)
        elif verdict == Verdict.CHALLENGE_REJECTED:
            self._resolve_proposer_wins(dispute, confidence)
        elif verdict == Verdict.PARTIAL:
            self._resolve_partial(dispute, confidence)
        
        return {
            "dispute_id": dispute_id,
            "verdict": verdict.value,
            "proposer_payout": dispute.proposer_payout,
            "challenger_payout": dispute.challenger_payout,
            "proposer_reputation_delta": dispute.proposer_reputation_delta,
            "challenger_reputation_delta": dispute.challenger_reputation_delta
        }
    
    def _resolve_challenger_wins(self, dispute: Dispute, confidence: float):
        """Calculate payouts when challenger wins."""
        multiplier = ATTACK_MULTIPLIERS[dispute.attack_type]
        
        # Challenger reward
        base_reward = dispute.challenger_stake * multiplier * confidence
        proposer_slash = dispute.proposer_stake * PROPOSER_SLASH_RATE * confidence
        
        dispute.challenger_payout = base_reward + proposer_slash
        dispute.proposer_payout = -proposer_slash
        dispute.proposer_reputation_delta = -0.10 * confidence
        dispute.challenger_reputation_delta = 0.05 * confidence
    
    def _resolve_proposer_wins(self, dispute: Dispute, confidence: float):
        """Calculate payouts when proposer wins (challenge rejected)."""
        challenger_slash = dispute.challenger_stake * CHALLENGER_SLASH_RATE * confidence
        
        # Distribution: 60% to proposer, 30% to validators (handled elsewhere), 10% burned
        proposer_recovery = challenger_slash * 0.6
        
        dispute.challenger_payout = -challenger_slash
        dispute.proposer_payout = proposer_recovery
        dispute.proposer_reputation_delta = 0.02 * confidence
        dispute.challenger_reputation_delta = -0.05 * confidence
    
    def _resolve_partial(self, dispute: Dispute, confidence: float):
        """Calculate payouts for partial verdict."""
        # Both sides take reduced hits
        partial_factor = 0.5
        
        multiplier = ATTACK_MULTIPLIERS[dispute.attack_type]
        challenger_reward = dispute.challenger_stake * multiplier * partial_factor * confidence
        proposer_slash = dispute.proposer_stake * PROPOSER_SLASH_RATE * partial_factor * confidence
        
        dispute.challenger_payout = challenger_reward + proposer_slash - (dispute.challenger_stake * 0.2)
        dispute.proposer_payout = -proposer_slash
        dispute.proposer_reputation_delta = -0.03 * confidence
        dispute.challenger_reputation_delta = 0.01 * confidence
    
    def get_dispute(self, dispute_id: str) -> Optional[Dispute]:
        """Get a dispute by ID."""
        return self.disputes.get(dispute_id)
    
    def get_pending_adjudication(self) -> List[Dispute]:
        """Get all disputes pending adjudication."""
        return [
            d for d in self.disputes.values() 
            if d.status == DisputeStatus.PENDING_ADJUDICATION
        ]
    
    def get_active_disputes_for_tree(self, task_id: str) -> List[Dispute]:
        """Get all active disputes for a reasoning tree."""
        dispute_ids = self.tree_challenges.get(task_id, [])
        return [
            self.disputes[did] for did in dispute_ids 
            if did in self.disputes and self.disputes[did].status != DisputeStatus.RESOLVED
        ]


# ============================================================================
# Challenge Detection Utilities
# ============================================================================

def analyze_challenge_quality(
    challenge: ChallengeSubmission,
    tree: ReasoningTree
) -> Dict:
    """
    Analyze the quality of a challenge before submission.
    
    Returns scoring signals that challengers can use to evaluate EV.
    """
    # Find the target node
    target_node = None
    if tree.root.id == challenge.target_node:
        target_node = tree.root
    else:
        for node in tree.nodes:
            if node.id == challenge.target_node:
                target_node = node
                break
    
    if not target_node:
        return {"error": "Target node not found"}
    
    analysis = {
        "target_node_type": target_node.node_type.value,
        "has_evidence": target_node.evidence is not None,
        "num_children": len(target_node.children),
        "attack_multiplier": ATTACK_MULTIPLIERS[challenge.attack_type],
        "estimated_reward": challenge.stake * ATTACK_MULTIPLIERS[challenge.attack_type],
        "max_slash_if_rejected": challenge.stake * CHALLENGER_SLASH_RATE,
    }
    
    # Risk assessment
    if not challenge.evidence:
        analysis["warning"] = "Challenge has no supporting evidence - higher rejection risk"
    
    return analysis


def calculate_challenge_ev(
    challenge_stake: float,
    attack_type: AttackType,
    proposer_stake: float,
    win_probability: float
) -> float:
    """
    Calculate expected value of a challenge.
    
    Args:
        challenge_stake: TAO to stake on challenge
        attack_type: Type of attack
        proposer_stake: Proposer's stake on the tree
        win_probability: Estimated probability of winning (0-1)
        
    Returns:
        Expected value in TAO
    """
    multiplier = ATTACK_MULTIPLIERS[attack_type]
    
    # Win outcome
    reward = (challenge_stake * multiplier) + (proposer_stake * PROPOSER_SLASH_RATE)
    
    # Lose outcome
    penalty = challenge_stake * CHALLENGER_SLASH_RATE
    
    ev = (win_probability * reward) - ((1 - win_probability) * penalty)
    
    return ev
```

---
