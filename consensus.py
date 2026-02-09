
```python
"""
Validator Consensus Mechanism

Implements weighted voting, calibration scoring, and tier-based adjudication
for dispute resolution.
"""

import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import math

from .protocol import Verdict, DisputeForAdjudication


# ============================================================================
# Constants
# ============================================================================

ADJUDICATION_WINDOW_HOURS = 4
ESCALATION_WINDOW_HOURS = 6
CONSENSUS_THRESHOLD = 0.6
CALIBRATION_DECAY_PER_EPOCH = 0.02
CALIBRATION_TIME_CONSTANT_DAYS = 30


class ValidatorTier(str, Enum):
    """Validator tiers with different weights and responsibilities."""
    SCOUT = "scout"       # Entry tier
    AUDITOR = "auditor"   # Mid tier
    ARBITER = "arbiter"   # Top tier


TIER_CONFIG = {
    ValidatorTier.SCOUT: {
        "stake_required": 100,
        "max_cases_per_epoch": 10,
        "weight_multiplier": 1.0,
        "min_calibration": 0.5,
    },
    ValidatorTier.AUDITOR: {
        "stake_required": 500,
        "max_cases_per_epoch": 50,
        "weight_multiplier": 2.0,
        "min_calibration": 0.7,
    },
    ValidatorTier.ARBITER: {
        "stake_required": 2000,
        "max_cases_per_epoch": float('inf'),
        "weight_multiplier": 5.0,
        "min_calibration": 0.85,
    },
}


@dataclass
class ValidatorState:
    """Tracks a validator's state and history."""
    hotkey: str
    tier: ValidatorTier
    stake: float
    calibration_score: float = 1.0
    verdicts_submitted: int = 0
    correct_verdicts: int = 0
    cases_this_epoch: int = 0
    last_active: datetime = field(default_factory=datetime.utcnow)
    tier_start_date: datetime = field(default_factory=datetime.utcnow)
    slashing_events: List[datetime] = field(default_factory=list)
    
    # Verdict history for calibration
    verdict_history: List[Dict] = field(default_factory=list)
    
    @property
    def effective_weight(self) -> float:
        """Calculate effective voting weight."""
        tier_mult = TIER_CONFIG[self.tier]["weight_multiplier"]
        return self.stake * self.calibration_score * tier_mult
    
    @property
    def can_take_case(self) -> bool:
        """Check if validator can take more cases this epoch."""
        max_cases = TIER_CONFIG[self.tier]["max_cases_per_epoch"]
        return self.cases_this_epoch < max_cases


@dataclass
class Vote:
    """A validator's vote on a dispute."""
    validator_hotkey: str
    verdict: Verdict
    confidence: float
    reasoning: str
    submitted_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ConsensusResult:
    """Result of consensus voting."""
    dispute_id: str
    final_verdict: Verdict
    weighted_score: float
    total_weight: float
    vote_breakdown: Dict[Verdict, float]
    participating_validators: List[str]
    escalated: bool = False
    
    @property
    def consensus_reached(self) -> bool:
        return self.weighted_score >= CONSENSUS_THRESHOLD


class ValidatorConsensus:
    """
    Manages validator consensus for dispute adjudication.
    
    Features:
    - Weighted voting based on stake, calibration, tier
    - Calibration tracking and decay
    - Tier progression/demotion
    - Random assignment (anti-manipulation)
    - Escalation to Arbiter panels
    """
    
    def __init__(self):
        self.validators: Dict[str, ValidatorState] = {}
        self.active_disputes: Dict[str, Dict] = {}  # dispute_id -> dispute state
        self.dispute_votes: Dict[str, List[Vote]] = {}  # dispute_id -> votes
        self.epoch_start: datetime = datetime.utcnow()
    
    # ========================================================================
    # Validator Management
    # ========================================================================
    
    def register_validator(
        self,
        hotkey: str,
        stake: float,
        tier: ValidatorTier = ValidatorTier.SCOUT
    ) -> ValidatorState:
        """Register a new validator."""
        if stake < TIER_CONFIG[tier]["stake_required"]:
            tier = ValidatorTier.SCOUT
            if stake < TIER_CONFIG[ValidatorTier.SCOUT]["stake_required"]:
                raise ValueError(f"Stake {stake} below minimum {TIER_CONFIG[ValidatorTier.SCOUT]['stake_required']}")
        
        validator = ValidatorState(
            hotkey=hotkey,
            tier=tier,
            stake=stake
        )
        self.validators[hotkey] = validator
        return validator
    
    def get_validator(self, hotkey: str) -> Optional[ValidatorState]:
        """Get validator state."""
        return self.validators.get(hotkey)
    
    def update_calibration(self, hotkey: str, was_correct: bool, confidence: float):
        """
        Update validator calibration based on verdict outcome.
        
        Calibration = (correct_verdicts × confidence_alignment) / total_verdicts
        """
        validator = self.validators.get(hotkey)
        if not validator:
            return
        
        validator.verdicts_submitted += 1
        if was_correct:
            validator.correct_verdicts += 1
        
        # Calculate alignment score
        # If correct with high confidence = good
        # If incorrect with high confidence = bad
        if was_correct:
            alignment = 1 - abs(1.0 - confidence)  # Reward high confidence when correct
        else:
            alignment = 1 - confidence  # Penalize high confidence when wrong
        
        # Add to history
        validator.verdict_history.append({
            "timestamp": datetime.utcnow(),
            "correct": was_correct,
            "confidence": confidence,
            "alignment": alignment
        })
        
        # Recalculate calibration with exponential decay weighting
        self._recalculate_calibration(validator)
        
        # Check tier demotion
        self._check_tier_status(validator)
    
    def _recalculate_calibration(self, validator: ValidatorState):
        """Recalculate calibration with time-weighted history."""
        if not validator.verdict_history:
            return
        
        now = datetime.utcnow()
        weighted_sum = 0.0
        weight_total = 0.0
        
        for entry in validator.verdict_history:
            # Exponential decay weight
            age_days = (now - entry["timestamp"]).days
            weight = math.exp(-age_days / CALIBRATION_TIME_CONSTANT_DAYS)
            
            score = entry["alignment"] if entry["correct"] else entry["alignment"] * 0.5
            weighted_sum += score * weight
            weight_total += weight
        
        if weight_total > 0:
            validator.calibration_score = min(1.5, max(0.3, weighted_sum / weight_total))
    
    def apply_calibration_decay(self):
        """Apply epoch calibration decay to inactive validators."""
        now = datetime.utcnow()
        for validator in self.validators.values():
            days_inactive = (now - validator.last_active).days
            if days_inactive > 7:
                decay = CALIBRATION_DECAY_PER_EPOCH * (days_inactive // 7)
                validator.calibration_score = max(0.5, validator.calibration_score - decay)
    
    def _check_tier_status(self, validator: ValidatorState):
        """Check if validator should be demoted."""
        min_cal = TIER_CONFIG[validator.tier]["min_calibration"]
        
        if validator.calibration_score < min_cal:
            # Demote
            if validator.tier == ValidatorTier.ARBITER:
                validator.tier = ValidatorTier.AUDITOR
            elif validator.tier == ValidatorTier.AUDITOR:
                validator.tier = ValidatorTier.SCOUT
            validator.tier_start_date = datetime.utcnow()
    
    def check_tier_promotion(self, hotkey: str) -> Optional[ValidatorTier]:
        """Check if validator qualifies for tier promotion."""
        validator = self.validators.get(hotkey)
        if not validator:
            return None
        
        now = datetime.utcnow()
        
        # Scout -> Auditor requirements
        if validator.tier == ValidatorTier.SCOUT:
            days_active = (now - validator.tier_start_date).days
            if (days_active >= 30 and 
                validator.calibration_score >= 0.7 and
                validator.verdicts_submitted >= 50 and
                validator.stake >= TIER_CONFIG[ValidatorTier.AUDITOR]["stake_required"]):
                validator.tier = ValidatorTier.AUDITOR
                validator.tier_start_date = now
                return ValidatorTier.AUDITOR
        
        # Auditor -> Arbiter requirements
        elif validator.tier == ValidatorTier.AUDITOR:
            days_active = (now - validator.tier_start_date).days
            recent_slashes = [s for s in validator.slashing_events if (now - s).days < 60]
            
            if (days_active >= 90 and
                validator.calibration_score >= 0.85 and
                validator.verdicts_submitted >= 200 and
                len(recent_slashes) == 0 and
                validator.stake >= TIER_CONFIG[ValidatorTier.ARBITER]["stake_required"]):
                validator.tier = ValidatorTier.ARBITER
                validator.tier_start_date = now
                return ValidatorTier.ARBITER
        
        return None
    
    # ========================================================================
    # Dispute Assignment
    # ========================================================================
    
    def assign_dispute(
        self,
        dispute_id: str,
        dispute: DisputeForAdjudication,
        num_validators: int = 5
    ) -> List[str]:
        """
        Randomly assign validators to adjudicate a dispute.
        
        Uses weighted random selection based on tier and availability.
        """
        eligible = [
            v for v in self.validators.values()
            if v.can_take_case and v.calibration_score >= 0.5
        ]
        
        if not eligible:
            return []
        
        # Weight by effective weight
        weights = [v.effective_weight for v in eligible]
        total_weight = sum(weights)
        probabilities = [w / total_weight for w in weights]
        
        # Select validators (without replacement)
        selected = []
        available = list(eligible)
        available_probs = list(probabilities)
        
        for _ in range(min(num_validators, len(available))):
            if not available:
                break
            
            # Normalize probabilities
            prob_sum = sum(available_probs)
            normalized = [p / prob_sum for p in available_probs]
            
            # Select one
            r = random.random()
            cumsum = 0
            for i, p in enumerate(normalized):
                cumsum += p
                if r <= cumsum:
                    selected.append(available[i].hotkey)
                    available.pop(i)
                    available_probs.pop(i)
                    break
        
        # Track assignment
        self.active_disputes[dispute_id] = {
            "dispute": dispute,
            "assigned_validators": selected,
            "deadline": datetime.utcnow() + timedelta(hours=ADJUDICATION_WINDOW_HOURS),
            "escalated": False
        }
        self.dispute_votes[dispute_id] = []
        
        # Update validator case counts
        for hotkey in selected:
            self.validators[hotkey].cases_this_epoch += 1
        
        return selected
    
    # ========================================================================
    # Voting
    # ========================================================================
    
    def submit_vote(
        self,
        dispute_id: str,
        validator_hotkey: str,
        verdict: Verdict,
        confidence: float,
        reasoning: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Submit a validator vote on a dispute.
        
        Returns:
            (success, error_message)
        """
        if dispute_id not in self.active_disputes:
            return False, f"Dispute {dispute_id} not found"
        
        dispute_state = self.active_disputes[dispute_id]
        
        if validator_hotkey not in dispute_state["assigned_validators"]:
            return False, "Validator not assigned to this dispute"
        
        if datetime.utcnow() > dispute_state["deadline"]:
            return False, "Adjudication window closed"
        
        # Check for duplicate vote
        existing = [v for v in self.dispute_votes[dispute_id] if v.validator_hotkey == validator_hotkey]
        if existing:
            return False, "Already voted on this dispute"
        
        vote = Vote(
            validator_hotkey=validator_hotkey,
            verdict=verdict,
            confidence=min(1.0, max(0.0, confidence)),
            reasoning=reasoning
        )
        self.dispute_votes[dispute_id].append(vote)
        
        # Update validator activity
        if validator_hotkey in self.validators:
            self.validators[validator_hotkey].last_active = datetime.utcnow()
        
        return True, None
    
    def calculate_consensus(self, dispute_id: str) -> Optional[ConsensusResult]:
        """
        Calculate weighted consensus from votes.
        
        Returns ConsensusResult or None if dispute not found.
        """
        if dispute_id not in self.active_disputes:
            return None
        
        votes = self.dispute_votes.get(dispute_id, [])
        if not votes:
            return ConsensusResult(
                dispute_id=dispute_id,
                final_verdict=Verdict.ABSTAIN,
                weighted_score=0.0,
                total_weight=0.0,
                vote_breakdown={},
                participating_validators=[]
            )
        
        # Calculate weighted votes per verdict
        verdict_weights: Dict[Verdict, float] = {v: 0.0 for v in Verdict}
        total_weight = 0.0
        
        for vote in votes:
            validator = self.validators.get(vote.validator_hotkey)
            if not validator:
                continue
            
            weight = validator.effective_weight * vote.confidence
            verdict_weights[vote.verdict] += weight
            total_weight += weight
        
        # Find winning verdict
        if total_weight == 0:
            return ConsensusResult(
                dispute_id=dispute_id,
                final_verdict=Verdict.ABSTAIN,
                weighted_score=0.0,
                total_weight=0.0,
                vote_breakdown=verdict_weights,
                participating_validators=[v.validator_hotkey for v in votes]
            )
        
        # Normalize
        vote_breakdown = {k: v / total_weight for k, v in verdict_weights.items()}
        
        # Find winner
        winner = max(vote_breakdown.items(), key=lambda x: x[1])
        
        return ConsensusResult(
            dispute_id=dispute_id,
            final_verdict=winner[0],
            weighted_score=winner[1],
            total_weight=total_weight,
            vote_breakdown=vote_breakdown,
            participating_validators=[v.validator_hotkey for v in votes]
        )
    
    def finalize_dispute(self, dispute_id: str) -> Optional[ConsensusResult]:
        """
        Finalize a dispute and apply calibration updates.
        
        Returns final consensus result.
        """
        result = self.calculate_consensus(dispute_id)
        if not result:
            return None
        
        # Check if needs escalation
        if not result.consensus_reached and not self.active_disputes[dispute_id]["escalated"]:
            return self.escalate_to_arbiters(dispute_id)
        
        # Update calibration for all voters
        for vote in self.dispute_votes.get(dispute_id, []):
            was_correct = vote.verdict == result.final_verdict
            self.update_calibration(vote.validator_hotkey, was_correct, vote.confidence)
        
        # Clean up
        del self.active_disputes[dispute_id]
        
        return result
    
    def escalate_to_arbiters(self, dispute_id: str) -> ConsensusResult:
        """
        Escalate dispute to Arbiter-only panel.
        """
        dispute_state = self.active_disputes.get(dispute_id)
        if not dispute_state:
            return None
        
        # Find all Arbiters
        arbiters = [
            v for v in self.validators.values()
            if v.tier == ValidatorTier.ARBITER and v.can_take_case
        ]
        
        if not arbiters:
            # No arbiters available - use existing votes
            result = self.calculate_consensus(dispute_id)
            result.escalated = True
            return result
        
        # Mark as escalated
        dispute_state["escalated"] = True
        dispute_state["deadline"] = datetime.utcnow() + timedelta(hours=ESCALATION_WINDOW_HOURS)
        dispute_state["assigned_validators"] = [a.hotkey for a in arbiters]
        
        # Clear non-Arbiter votes for re-vote
        arbiter_hotkeys = {a.hotkey for a in arbiters}
        self.dispute_votes[dispute_id] = [
            v for v in self.dispute_votes.get(dispute_id, [])
            if v.validator_hotkey in arbiter_hotkeys
        ]
        
        return ConsensusResult(
            dispute_id=dispute_id,
            final_verdict=Verdict.ABSTAIN,  # Pending
            weighted_score=0.0,
            total_weight=0.0,
            vote_breakdown={},
            participating_validators=list(arbiter_hotkeys),
            escalated=True
        )
    
    # ========================================================================
    # Epoch Management
    # ========================================================================
    
    def new_epoch(self):
        """Reset epoch-specific counters."""
        self.epoch_start = datetime.utcnow()
        for validator in self.validators.values():
            validator.cases_this_epoch = 0
        self.apply_calibration_decay()
    
    def get_validator_stats(self, hotkey: str) -> Optional[Dict]:
        """Get comprehensive validator statistics."""
        validator = self.validators.get(hotkey)
        if not validator:
            return None
        
        return {
            "hotkey": validator.hotkey,
            "tier": validator.tier.value,
            "stake": validator.stake,
            "calibration_score": validator.calibration_score,
            "effective_weight": validator.effective_weight,
            "verdicts_submitted": validator.verdicts_submitted,
            "correct_verdicts": validator.correct_verdicts,
            "accuracy": validator.correct_verdicts / validator.verdicts_submitted if validator.verdicts_submitted > 0 else 0,
            "cases_this_epoch": validator.cases_this_epoch,
            "can_take_case": validator.can_take_case,
            "last_active": validator.last_active.isoformat(),
        }
```

---
