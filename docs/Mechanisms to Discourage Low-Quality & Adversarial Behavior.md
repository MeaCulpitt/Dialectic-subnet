# Mechanisms to Discourage Low-Quality & Adversarial Behavior

Dialectic employs a defense-in-depth architecture where economic, cryptographic, and statistical safeguards create asymmetric cost structures—**cheap to be honest, expensive to attack**.

---

## 1. Anti-Spam: The Cognitive Entropy Filter

**The Attack:** Proposers flood the subnet with low-effort, templated reasoning (e.g., GPT-4 generated generic responses) to harvest base emissions.

### The Defense:

#### A. Minimum Viable Complexity (MVC)

```python
if tree_depth < 5 or unique_lemmas < 3:
    emission = 0  # Automatic rejection
    stake = slashed 10%  # Penalty for waste of validator time
```

#### B. Epistemic Entropy Scoring

Validators compute **Shannon entropy** of reasoning trees:

**`Entropy = -Σ p(lemma_type) × log(p(lemma_type))`**

Templates (high repetition of sentence structures) → **Entropy < 4.0** → **"Stochastic Parrot" Flag**

- **First flag:** Warning
- **Second flag:** 24-hour submission ban
- **Third flag:** Progressive stake lock (50% of TAO frozen for 14 days)

#### C. Temporal Uniqueness

Submissions must include a **recent block hash** (within last 50 blocks) in their Merkle root derivation. This prevents:

- Pre-computing reasoning trees (can't predict future block hashes)
- Copy-pasting old solutions from IPFS/archives

---

## 2. Anti-Griefing: Challenger Sanity Bonds

**The Attack:** Challengers spam frivolous challenges to exhaust Proposer resources (DDoS via challenges) or deliberately challenge correct logic to harass competitors.

### The Defense:

#### A. Frivolous Challenge Tax

If a challenge scores **<20% validity** (validators unanimously deem it nonsense):

**`Challenger_Loss = Stake × 0.25 + Fixed_Fee(10 TAO)`**

This super-linear penalty makes spam challengers bleed capital rapidly.

#### B. Challenge Velocity Limits

**`Max_Challenges_Per_24h = floor(sqrt(Reputation_Score)) + 2`**

- **New account (RS=0):** 2 challenges/day
- **Established (RS=100):** 12 challenges/day
- **Elite (RS=1000):** 33 challenges/day

Prevents bot armies from overwhelming the system. High-reputation challengers earn the right to challenge more because they've proven accuracy.

#### C. The "Cry Wolf" Multiplier

Consecutive failed challenges trigger escalating penalties:

- **1st fail:** Lose stake only
- **2nd consecutive fail:** Lose stake + 5% reputation
- **3rd consecutive fail:** Blacklist from challenging Proposers with RS > 500 for 72 hours (protects high-quality reasoners from harassment)

---

## 3. Collusion Resistance: The Geometric Surveillance

**The Attack:** Proposer A and Challenger B collude—B challenges A with weak arguments, A easily defends, both split the high "Immortality Bonus" for surviving challenges.

### The Defense:

#### A. Latent Challenge Assignment

Challengers don't choose which Proposer to attack directly. They submit **"scent profiles"** describing the type of flaw they're hunting:

Target: "factual errors in legal citations" Risk_Appetite: "high" Min_Reward: 50 TAO


The protocol algorithmically matches challengers to reasoning trees using:

- TF-IDF similarity between challenge profile and tree content
- Consistent hashing of Proposer hotkey + Challenger hotkey to prevent self-selection

#### B. The Stake-Sized Plausibility Check

Challenges must include a **"Proof of Effort"**—a zero-knowledge proof that the challenger expended **>X compute cycles** analyzing the target node. This raises the cost of fake challenges to near the cost of real ones, eliminating the profit margin in collusion.

#### C. Temporal Decoupling

Challengers commit to challenges **encrypted** (commit-reveal). Only after the challenge window closes are identities revealed. This prevents:

- Proposers knowing who challenged them (can't negotiate side deals)
- Challengers knowing if they're attacking a friend until too late

---

## 4. Validator Corruption Prevention

**The Attack:** Validators accept bribes to vote incorrectly, or lazily vote randomly without verification.

### The Defense:

#### A. The Schelling Queue (Ordered Revelation)

Validators don't submit votes simultaneously. They are sequentially ordered by pseudo-random selection (based on stake + reputation).

- **1st Validator:** Votes blind (no prior information)
- **2nd Validator:** Sees 1st vote, but with 2-hour delay
- **3rd Validator:** Sees aggregated signal, but with 4-hour delay
- **Nth Validator:** Sees strong consensus forming, but by now the deadline pressure makes changing votes costly

This creates a cascade of accountability—early validators set the "Schelling point," late validators must justify deviation.

#### B. Cryptographic Commitment to Verification

Validators must submit:

- Hash of verification trace (which branches they checked)
- ZK-proof of LLM inference (proving they actually ran the model, not just guessed)

**"Lazy Validation" Penalty:** If a validator submits **>3 votes in a row** without corresponding ZK-proofs of compute, they are downgraded to **"Scout" tier** (70% emission cut) for 7 days.

#### C. The Dissent Bonus

Validators who vote **against the majority** but are proven correct (upon appeal) receive:

**`Bonus = Majority_Stake_Weighted × 0.10`**

This creates a bounty for whistleblowing against validator cartels. Even if **90%** of validators are corrupt, the **10%** honest minority gets rich proving the truth, attracting more honest validators until equilibrium restores.

---

## 5. Sybil Resistance: The Progressive Stake Ladder

**The Attack:** One actor creates 1000 hotkeys to dominate challenge submission or validator voting.

### The Defense:

#### A. Super-Linear Stake Requirements

**`Effective_Stake = Actual_Stake × (1 + 0.1 × ln(Hotkeys_Overall))`**

- If you control **1 hotkey:** 1.0× multiplier
- If you control **100 hotkeys:** 1.46× multiplier required per key to maintain influence
- If you control **1000 hotkeys:** 1.92× multiplier required per key

This makes Sybil attacks economically irrational—you gain no advantage splitting stake across identities versus concentrating it, while paying higher gas fees for multiple registrations.

#### B. The Turing Barrier (Human Proof)

For the first **30 days**, new hotkeys must solve a **Proof-of-Humanity (PoH)** captcha that requires:

- Sufficient latency between keystrokes (anti-bot)
- Semantic understanding (anti-LLM solver)
- One-time **10 TAO deposit** (refunded after 30 days of honest participation, burned if banned)

#### C. Behavioral Fingerprinting

Statistical analysis of submission patterns detects automation:

- **Timing entropy:** Bots often submit at exact intervals (every 3600 seconds). Human variance required (**>0.3 bits entropy**).
- **Lexical diversity:** Sybil accounts often reuse sentence templates. Jaccard similarity **>0.8** between submissions triggers manual protocol review and potential slashing.

---

## 6. Self-Dealing Prevention: The Chinese Wall

**The Attack:** A single entity runs Proposer, Challenger, and Validator nodes, creating circular logic to extract emissions (e.g., challenge yourself with weak arguments, validate your own win, split the pot).

### The Defense:

#### A. Role Separation by Stake Lock

A hotkey cannot change roles within a **14-day epoch**:

- If you staked as a Validator on Day 1, you cannot propose or challenge until Day 15
- This prevents intra-epoch arbitrage where an actor switches roles to cover their own tracks

#### B. Ownership Graph Analysis

Subnet-level monitoring of correlated stake movements:

- If **Hotkey A** (Proposer) and **Hotkey B** (Challenger) both receive funding from the same parent address within **48 hours** → **Red Flag**
- If **Hotkey C** (Validator) votes on challenges involving A and B with **>90% correlation** → **Red Flag**
- **Shadow Ban:** Flagged pairs cannot interact; challenges auto-rejected, validator votes on that proposer ignored

#### C. The Honest Minority Assumption (Economic)

Even if a cartel controls **60%** of stake, the Challenge-Response latency (2-hour defense window) makes it impossible to coordinate across time zones without leaving traceable evidence. More importantly, the **Calibration Penalty** means that even cartel members are incentivized to "defect" and vote correctly if they believe the other cartel members might be wrong—because being the only honest validator in a corrupt vote earns massive calibration bonuses.

---

## 7. The "Panic Button" Circuit Breakers

Emergency Mechanisms for Extreme Attacks:

### A. The Subnet Freeze

If **>50%** of challenges in a 24-hour window are deemed frivolous by validators (indicating a spam attack), the protocol automatically:

- Extends the Challenge Window by **6 hours** (giving validators more time)
- Increases the Challenge Stake Floor by **3×** (price out the attacker)
- Activates **Governance Mode:** Only validators with **>6 months history** can adjudicate until stability returns

### B. The Reputation Reset

In the event of a discovered exploit (e.g., a novel way to game the entropy score), the protocol can invoke **"Tabula Rasa":**

- All reputation scores are snapshot and frozen
- A new scoring algorithm is deployed
- Miners/validators must re-earn reputation under new rules, but maintain their stake (preventing capital flight while ensuring fair competition)

### C. The Treasury Shield

If a wealthy attacker attempts to grief the network by submitting massive stake to lose on purpose (denial-of-capital attack), the **Subnet Treasury** (funded by burn mechanisms) automatically:

- Matches legitimate challenger stakes to maintain incentive alignment
- Reimburses validators for overtime verification work
- Buys back and burns TAO to offset the attacker's inflationary pressure

---

## Conclusion: The Defense-in-Depth Architecture

No single mechanism prevents all attacks; rather, **asymmetric cost structures** stack to make adversarial behavior prohibitively expensive:

| Attack Vector | Cost to Attack | Cost to Defend | Asymmetry Ratio |
|---------------|----------------|----------------|-----------------|
| Spam Challenges | High (25% slashing risk) | Low (automated filters) | 10:1 |
| Sybil Accounts | High (super-linear stake) | Low (behavioral analysis) | 50:1 |
| Validator Collusion | High (calibration penalties) | Low (quadratic voting) | 100:1 |
| Self-Dealing | High (14-day role lock) | Low (graph analysis) | 20:1 |

The result is a protocol where **honesty is the least expensive strategy**—not because participants are virtuous, but because the math makes virtue profitable.
