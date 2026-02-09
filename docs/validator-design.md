# Validator Design

Validators adjudicate disputes between Proposers and Challengers. This document covers the adjudication protocol, scoring, and validator tiers.

---

## Role Overview

Validators don't evaluate all reasoning — they judge contested claims when challenges arise. Their role is judicial, not editorial.

**Validator responsibilities:**
1. Adjudicate challenges fairly
2. Maintain calibration (accuracy over time)
3. Respond within time limits
4. Stake to back their judgments

---

## Adjudication Protocol

### When a Challenge is Submitted

    1. Challenge received → assigned to validator pool
    2. Validators have 4 hours to review and vote
    3. Weighted consensus determines outcome
    4. Stakes redistributed based on verdict

### What Validators See

    {
      "dispute_id": "disp_20260209_1423",
      "task_id": "dt_20260209_0847",
      "contested_node": {
        "id": "n1",
        "claim": "Orbit chains have sufficient TVL to justify deployment costs",
        "evidence": {
          "source": "L2Beat",
          "data": "Combined Orbit TVL: $2.1B as of Feb 2026"
        }
      },
      "challenge": {
        "attack_type": "factual_error",
        "argument": "The L2Beat figure includes non-Orbit chains. Actual Orbit-only TVL is $340M.",
        "evidence": {
          "source": "L2Beat filtered view",
          "data": "Orbit chains specifically: $340M combined"
        }
      },
      "defense": {
        "type": "refute",
        "response": "The cited figure is correct. Here is the methodology..."
      },
      "proposer_reputation": 1.15,
      "challenger_reputation": 0.95
    }

Validators see the contested node, the challenge, and any defense — not the full tree.

### Validator Verdict

    {
      "dispute_id": "disp_20260209_1423",
      "verdict": "challenge_upheld",
      "confidence": 0.85,
      "reasoning": "Verified L2Beat source. Challenger's filtered view is accurate.",
      "validator_hotkey": "5Vx7..."
    }

**Verdict options:**
- challenge_upheld — Challenger wins
- challenge_rejected — Proposer wins
- partial — Flaw exists but less severe than claimed
- abstain — Insufficient information (costs reputation)

---

## Consensus Mechanism

### Weighted Voting

Each validator's vote is weighted by:

    weight = stake_weight × calibration_score × tier_multiplier
    
    Where:
    - stake_weight = validator_stake / total_validator_stake
    - calibration_score = historical accuracy (0.5 to 1.5)
    - tier_multiplier = 1x (Scout), 2x (Auditor), 5x (Arbiter)

### Threshold

    If weighted_votes(challenge_upheld) > 0.6: Challenger wins
    If weighted_votes(challenge_rejected) > 0.6: Proposer wins
    If neither > 0.6: Escalate to Arbiter panel

### Escalation

When consensus isn't reached:
1. Dispute escalates to Arbiter-only panel
2. Arbiters have 6 additional hours
3. Simple majority among Arbiters decides
4. Non-Arbiter validators who voted with eventual majority gain calibration; others lose

---

## Validator Tiers

| Tier | Stake Required | Max Cases/Epoch | Vote Weight | Requirements |
|------|----------------|-----------------|-------------|--------------|
| Scout | 100 TAO | 10 | 1x | None |
| Auditor | 500 TAO | 50 | 2x | 30 days + 0.7 calibration |
| Arbiter | 2,000 TAO | Unlimited | 5x | 90 days + 0.85 calibration |

### Tier Progression

    Scout → Auditor: 
      - 30 days active
      - Calibration score ≥ 0.7
      - ≥ 50 verdicts submitted
      - Stake increased to 500 TAO
    
    Auditor → Arbiter:
      - 90 days active  
      - Calibration score ≥ 0.85
      - ≥ 200 verdicts submitted
      - Stake increased to 2,000 TAO
      - No slashing events in past 60 days

### Tier Demotion

Validators can be demoted for:
- Calibration score dropping below tier threshold
- Extended inactivity (>14 days without verdict)
- Slashing event (immediate demotion one tier)

---

## Calibration Scoring

Calibration measures how well a validator's verdicts align with final outcomes.

### Calculation

    calibration = (correct_verdicts × confidence_alignment) / total_verdicts
    
    Where:
    - correct_verdict = voted with eventual consensus
    - confidence_alignment = 1 - |stated_confidence - actual_outcome|

**Example:**
- Validator votes challenge_upheld with 0.85 confidence
- Final outcome: challenge upheld (1.0)
- Alignment: 1 - |0.85 - 1.0| = 0.85
- This verdict scores 0.85

### Calibration Decay

- Calibration decays 2% per epoch without activity
- Recent verdicts weighted more heavily (exponential decay, τ = 30 days)
- New validators start at 1.0 (neutral)

### Calibration Penalties

| Calibration Score | Effect |
|-------------------|--------|
| > 1.2 | Bonus cases, priority assignment |
| 1.0 - 1.2 | Normal operation |
| 0.7 - 1.0 | Reduced case assignment |
| 0.5 - 0.7 | Scout-only cases, tier demotion risk |
| < 0.5 | Suspended from adjudication |

---

## Validator Rewards

### Base Rewards

Validators receive 10% of epoch emissions, distributed by:

    validator_reward = base_emission × 0.1 × (validator_weight / total_validator_weight)
    
    validator_weight = stake × calibration × tier_multiplier × activity_bonus

### Per-Dispute Rewards

Additionally, validators earn per dispute:

| Outcome | Reward |
|---------|--------|
| Voted with consensus | 0.5% of dispute stakes |
| Voted against consensus | -0.25% of own stake |
| Abstained | No reward, small calibration hit |

### Activity Bonus

    activity_bonus = min(1.5, 1.0 + (verdicts_this_epoch / expected_verdicts) × 0.5)

Active validators earn up to 50% more than passive ones.

---

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 16 GB | 32 GB |
| GPU | Not required | Optional for analysis |
| Storage | 100 GB SSD | 500 GB NVMe |
| Network | 50 Mbps | 100 Mbps, low latency |

Validators need:
- Reliable uptime (disputes have time limits)
- Fast evidence verification (web access)
- Sufficient compute for analysis tooling

---

## Running a Validator

    git clone https://github.com/MeaCulpitt/Dialectic-subnet.git
    cd Dialectic-subnet
    pip install -r requirements.txt
    
    python neurons/validator.py \
      --netuid <NETUID> \
      --wallet.name <WALLET> \
      --wallet.hotkey <HOTKEY> \
      --stake 100 \
      --auto_verdict false

### Configuration Options

| Flag | Description | Default |
|------|-------------|---------|
| --stake | TAO to stake | 100 |
| --auto_verdict | Use AI-assisted verdicts | false |
| --domains | Limit to specific domains | all |
| --max_cases | Cases per epoch | tier limit |
| --response_hours | Time before auto-abstain | 4 |

---

## Best Practices

1. **Verify evidence independently.** Don't trust either party's citations.
2. **State confidence accurately.** Overconfidence hurts calibration.
3. **Abstain when uncertain.** Better than a wrong verdict.
4. **Specialize.** Focus on domains you understand.
5. **Stay active.** Calibration decays with inactivity.
6. **Read defenses carefully.** Proposers sometimes have valid rebuttals.

---
