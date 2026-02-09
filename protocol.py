
```python
"""
Dialectic Protocol Definitions

Defines the synapse types for communication between proposers, challengers, and validators.
"""

import bittensor as bt
from typing import Optional, List, Dict, Any
from pydantic import Field
from enum import Enum


class NodeType(str, Enum):
    """Types of nodes in a reasoning tree."""
    CONCLUSION = "conclusion"
    PREMISE = "premise"
    SUB_PREMISE = "sub_premise"
    REBUTTAL = "rebuttal"
    QUALIFIER = "qualifier"


class AttackType(str, Enum):
    """Types of challenges that can be made against reasoning nodes."""
    FACTUAL_ERROR = "factual_error"           # 2.0x multiplier
    LOGICAL_FALLACY = "logical_fallacy"       # 2.5x multiplier
    MISSING_CONTEXT = "missing_context"       # 1.5x multiplier
    CONTRADICTION = "contradiction"           # 3.0x multiplier
    OUTDATED = "outdated"                     # 1.5x multiplier


class DefenseType(str, Enum):
    """Types of defenses a proposer can mount."""
    REFUTE = "refute"      # Counter-evidence provided
    CONCEDE = "concede"    # Accept the challenge, limit damage
    PARTIAL = "partial"    # Accept part, contest rest


class Verdict(str, Enum):
    """Validator verdicts on disputed nodes."""
    CHALLENGE_UPHELD = "challenge_upheld"
    CHALLENGE_REJECTED = "challenge_rejected"
    PARTIAL = "partial"
    ABSTAIN = "abstain"


# ============================================================================
# Data Models
# ============================================================================

class Evidence(bt.Synapse):
    """Evidence supporting a reasoning node."""
    source: str = Field(description="Source of the evidence")
    data: str = Field(description="The evidence data/content")
    url: Optional[str] = Field(default=None, description="URL reference if applicable")
    timestamp: Optional[str] = Field(default=None, description="When evidence was gathered")


class ReasoningNode(bt.Synapse):
    """A single node in the reasoning tree."""
    id: str = Field(description="Unique node identifier")
    claim: str = Field(description="The claim being made")
    node_type: NodeType = Field(description="Type of reasoning node")
    evidence: Optional[Evidence] = Field(default=None)
    children: List[str] = Field(default_factory=list, description="Child node IDs")
    merkle_hash: Optional[str] = Field(default=None, description="Merkle hash of this node")


class ReasoningTree(bt.Synapse):
    """Complete reasoning tree submitted by a proposer."""
    task_id: str = Field(description="Task identifier")
    root: ReasoningNode = Field(description="Root node of the tree")
    nodes: List[ReasoningNode] = Field(default_factory=list, description="All nodes in tree")
    merkle_root: str = Field(description="Merkle root of the entire tree")
    stake: float = Field(description="TAO staked on this tree")
    proposer_hotkey: str = Field(description="Proposer's hotkey")
    submitted_at: Optional[str] = Field(default=None)


# ============================================================================
# Synapse Definitions
# ============================================================================

class TaskAssignment(bt.Synapse):
    """
    Validator → Proposer: Assigns a reasoning task.
    """
    task_id: str = Field(description="Unique task identifier")
    domain: str = Field(description="Domain of the task (defi_governance, security, etc.)")
    prompt: str = Field(description="The reasoning prompt to address")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Task constraints")
    deadline: str = Field(description="ISO timestamp deadline for submission")
    base_reward: float = Field(default=0.5, description="Base reward for the task")


class TreeSubmission(bt.Synapse):
    """
    Proposer → Validator: Submits a completed reasoning tree.
    """
    task_id: str = Field(description="Task this tree addresses")
    tree: ReasoningTree = Field(description="The complete reasoning tree")
    
    # Response fields (filled by validator)
    accepted: Optional[bool] = Field(default=None)
    rejection_reason: Optional[str] = Field(default=None)


class ChallengeSubmission(bt.Synapse):
    """
    Challenger → Validator: Submits a challenge against a reasoning tree node.
    """
    task_id: str = Field(description="Task ID of the target tree")
    target_node: str = Field(description="ID of the node being challenged")
    attack_type: AttackType = Field(description="Type of attack")
    argument: str = Field(description="The challenger's argument")
    evidence: Optional[Evidence] = Field(default=None)
    stake: float = Field(description="TAO staked on this challenge")
    challenger_hotkey: str = Field(description="Challenger's hotkey")
    
    # Response fields
    accepted: Optional[bool] = Field(default=None)
    dispute_id: Optional[str] = Field(default=None)


class DefenseSubmission(bt.Synapse):
    """
    Proposer → Validator: Responds to a challenge.
    """
    dispute_id: str = Field(description="Dispute being defended")
    defense_type: DefenseType = Field(description="Type of defense")
    response: str = Field(description="Defense argument")
    evidence: Optional[Evidence] = Field(default=None)
    affected_nodes: List[str] = Field(default_factory=list, description="Nodes affected if conceding")
    tree_still_valid: Optional[bool] = Field(default=None, description="For partial concessions")
    
    # Response fields
    accepted: Optional[bool] = Field(default=None)


class DisputeForAdjudication(bt.Synapse):
    """
    Validator → Validator: Internal synapse for dispute adjudication.
    """
    dispute_id: str = Field(description="Unique dispute identifier")
    task_id: str = Field(description="Original task ID")
    contested_node: ReasoningNode = Field(description="The node being challenged")
    challenge: ChallengeSubmission = Field(description="The challenge details")
    defense: Optional[DefenseSubmission] = Field(default=None)
    proposer_reputation: float = Field(default=1.0)
    challenger_reputation: float = Field(default=1.0)
    
    # Validator response
    verdict: Optional[Verdict] = Field(default=None)
    confidence: Optional[float] = Field(default=None)
    reasoning: Optional[str] = Field(default=None)
    validator_hotkey: Optional[str] = Field(default=None)


class VerdictAnnouncement(bt.Synapse):
    """
    Validator → All: Announces the final verdict on a dispute.
    """
    dispute_id: str = Field(description="Dispute identifier")
    final_verdict: Verdict = Field(description="Final consensus verdict")
    weighted_score: float = Field(description="Weighted consensus score")
    proposer_impact: Dict[str, Any] = Field(description="Impact on proposer (stake, reputation)")
    challenger_impact: Dict[str, Any] = Field(description="Impact on challenger (stake, reputation)")
    participating_validators: List[str] = Field(description="Validators who adjudicated")


# ============================================================================
# Reward Multipliers
# ============================================================================

ATTACK_MULTIPLIERS = {
    AttackType.FACTUAL_ERROR: 2.0,
    AttackType.LOGICAL_FALLACY: 2.5,
    AttackType.MISSING_CONTEXT: 1.5,
    AttackType.CONTRADICTION: 3.0,
    AttackType.OUTDATED: 1.5,
}
```

---
