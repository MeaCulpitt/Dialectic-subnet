# Mechanism Design

This document covers Dialectic's game theory, incentive structure, and emission logic.

---

## Core Mechanism

Dialectic implements a three-party adversarial game:

    ┌─────────────┐     submits      ┌─────────────────┐
    │  Proposer   │ ───────────────► │  Reasoning Tree │
    └─────────────┘                  └────────┬────────┘
                                              │
    ┌─────────────┐     attacks      ┌────────▼────────┐
    │  Challenger │ ───────────────► │  Specific Node  │
    └─────────────┘                  └────────┬────────┘
                                              │
    ┌─────────────┐   adjudicates    ┌────────▼────────┐
    │  Validator  │ ───────────────► │    Verdict      │
    └─────────────┘                  └─────────────────┘

Each role has distinct economic incentives aligned toward accurate reasoning.

---

## Emission Distribution

| Role | Share | Source |
|------|-------|--------|
| Proposers | 60% | Base emissions + unchallenged bonuses |
| Challengers | 30% | Successful challenge rewards + bounties |
| Validators | 10% | Adjudication fees + calibration bonuses |

### Why 60/30/10?

**Proposers (60%):** The primary work product is reasoning. Higher share attracts quality contributors.

**Challengers (30%):** Adversarial pressure requires meaningful rewards, but challengers only add value when flaws exist. Lower share prevents challenge-farming.

**Validators (10%):** Adjudication is essential but shouldn't be the profit center. Lower share keeps validators neutral.

---

## Staking Mechanics

### Proposer Stakes

When submitting a reasoning tree:

| Tree Complexity | Minimum Stake | Maximum Stake |
|-----------------|---------------|---------------|
| Simple (1-5 nodes) | 10 TAO | 50 TAO |
| Medium (6-20 nodes) | 25 TAO | 100 TAO |
| Complex (21+ nodes) | 50 TAO | 250 TAO |

Higher stakes signal confidence and attract proportionally higher rewards if unchallenged.

### Challenger Stakes

To challenge a specific node:

| Challenge Type | Minimum Stake | Maximum Reward |
|----------------|---------------|----------------|
| Factual error | 5 TAO | 2x stake |
| Logical fallacy | 10 TAO | 2.5x stake |
| Missing context | 5 TAO | 1.5x stake |
| Contradiction | 10 TAO | 3x stake |

Challenger stake must be at least 10% of proposer's stake on the contested branch.

### Validator Stakes

Validators stake to participate in adjudication:

| Tier | Stake | Cases/Epoch | Weight |
|------|-------|-------------|--------|
| Scout | 100 TAO | Up to 10 | 1x |
| Auditor | 500 TAO | Up to 50 | 2x |
| Arbiter | 2,000 TAO | Unlimited | 5x |

Higher tiers receive more cases and more weight in disputed verdicts.

---

## Reward Calculations

### Unchallenged Proposer Reward

If a reasoning tree survives the challenge window:

    reward = base_emission × (stake_weight / total_stakes) × quality_multiplier
    
    quality_multiplier = reputation_score × complexity_bonus × freshness

**Example:** 
- Proposer stakes 50 TAO on a medium-complexity tree
- Total proposer stakes this epoch: 5,000 TAO
- Reputation score: 1.2 (good history)
- Complexity bonus: 1.15 (12 nodes)
- Base emission: 100 TAO

    reward = 100 × (50/5000) × (1.2 × 1.15) = 1.38 TAO

### Successful Challenge Reward

When a challenger wins:

    challenger_reward = challenger_stake × reward_multiplier + proposer_slash
    
    proposer_slash = min(proposer_stake × 0.3, challenged_branch_stake)

**Example:**
- Challenger stakes 10 TAO on a logical fallacy (2.5x multiplier)
- Proposer had staked 50 TAO total, 15 TAO on challenged branch

    challenger_reward = (10 × 2.5) + (15 × 0.3) = 25 + 4.5 = 29.5 TAO

The proposer loses 4.5 TAO plus reputation damage.

### Failed Challenge Penalty

When a challenge is rejected:

    penalty = challenger_stake × 0.5
    distribution = 60% to proposer, 30% to validators, 10% burned

This prevents frivolous challenges while not being so punitive that legitimate challenges are deterred.

---

## Game Theory Analysis

### Proposer Strategy

**Optimal behavior:** Submit well-reasoned trees with appropriate stakes.

- Understaking invites challenges (low downside for attackers)
- Overstaking risks larger losses if flaws exist
- Quality reasoning is the best defense

**Equilibrium:** Proposers stake proportionally to their confidence and reasoning quality.

### Challenger Strategy

**Optimal behavior:** Challenge only when expected value is positive.

    EV = P(win) × reward - P(lose) × penalty
    
    Challenge when EV > 0

- Deep analysis before challenging is incentivized
- Marginal challenges are filtered by stake requirements
- High-reputation proposers are challenged less (higher P(lose))

**Equilibrium:** Only substantive challenges are submitted.

### Validator Strategy

**Optimal behavior:** Judge accurately to maximize calibration score.

Validators are scored on:
1. Agreement with final consensus (after appeals)
2. Speed of response
3. Consistency across similar cases

Poor calibration reduces case assignment and effective stake weight.

---

## Anti-Gaming Mechanisms

### Collusion Prevention

**Self-challenge detection:**
- Statistical analysis of proposer-challenger pairs
- Suspiciously correlated behavior triggers review
- Penalty: Both parties slashed + reputation reset

**Sybil resistance:**
- Minimum stake requirements make Sybil attacks expensive
- Reputation is per-key, not transferable
- New accounts start with neutral (not high) reputation

### Quality Inflation Prevention

**Reputation decay:**
- 5% decay per epoch for inactive participants
- Recent performance weighted higher than historical
- Prevents "rest on laurels" behavior

**Difficulty adjustment:**
- As average quality increases, challenge criteria tighten
- Maintains adversarial pressure even in mature network

### Validator Manipulation Prevention

**Random assignment:**
- Validators cannot choose which disputes to judge
- Assignments weighted by tier and stake
- No foreknowledge of which cases they'll receive

**Calibration penalties:**
- Validators who consistently deviate from consensus lose stake weight
- Extreme outliers face escalating penalties
- Prevents biased or captured validators

---

## Epoch Structure

Each epoch runs on a 24-hour cycle:

| Phase | Duration | Activity |
|-------|----------|----------|
| Submission | 0-18h | Proposers submit reasoning trees |
| Challenge | 0-24h | Challengers can attack any tree (6h window per tree) |
| Defense | Per challenge | 2h defense window after each challenge |
| Adjudication | Rolling | Validators judge as disputes arise |
| Settlement | 24h | Rewards and slashes distributed |

Submissions and challenges overlap. A tree submitted at hour 10 can be challenged until hour 16.

---

## Upgrade Path

### Phase 1: Launch
- Conservative parameters (higher stakes, simpler trees)
- Limited validator set (curated Arbiters)
- Manual review of edge cases

### Phase 2: Expansion
- Stake requirements reduced based on observed behavior
- Validator set opens to Scouts
- Automated adjudication for clear-cut cases

### Phase 3: Maturity
- Full parameter governance by stakers
- Cross-subnet integration (reasoning as a service)
- Specialized domains (legal, scientific, financial)

---

## Parameter Governance

After Phase 2, key parameters can be adjusted through governance:

| Parameter | Adjustment Range | Vote Threshold |
|-----------|------------------|----------------|
| Emission split | ±10% per role | 66% of validator stake |
| Minimum stakes | ±50% | 50% of total stake |
| Challenge windows | ±2 hours | 50% of validator stake |
| Slashing rates | ±10% | 75% of total stake |

Changes require a 7-day notice period before implementation.

---
