# Incentive Alignment Architecture: Why They Play By The Rules

Dialectic uses multi-period game theory and irreversible reputation staking to transform short-term exploiters into long-term truth-seekers. Here is the specific alignment logic for each actor.

---

## Miner Alignment (Proposers & Challengers)

### The Reputation Lock-In Mechanism

**The Problem:** In standard subnets, miners can "hit-and-run"—extract emissions with low-quality work, deregister, and restart fresh.

**The Solution: Cognitive Capital Accumulation**

**`Effective_Emission_Rate = Base_Rate × (1 + ln(1 + Reputation_Score/100))`**

**Reputation Score (RS):** Persists across subnet registrations (stored on Bittensor parent chain)

**Growth Pattern:** Linear in effort, logarithmic in decay
- **+10 RS** for surviving a high-stake challenge
- **-2 RS** per day of inactivity (halving time: 35 days)

**Permanence:** RS > 1000 grants **"Elder"** status—emission floor guarantees and governance rights

**Alignment Effect:** A miner with RS=500 earns **6.2x** the TAO per unit of work vs. a new miner (RS=0). This creates exit friction—leaving the subnet destroys months of accumulated cognitive capital.

### The Dual-Role Optimization

Miners can act as Proposers in Round N and Challengers in Round N+1, creating a portfolio strategy.

**The Kelly Criterion Allocation:** Rational miners optimize their capital allocation:

- **High Reputation (RS>300):** Allocate **70%** to Proposing (stable income), **30%** to Challenging (high variance upside)
- **Low Reputation:** Allocate **90%** to Challenging (asymmetric upside—find one critical bug → instant reputation boost)

**Anti-Collusion Design:** Miners cannot challenge their own submissions (hotkey linking prevents Sybil masking). More critically, **Challenge Anonymity** ensures that even if Proposer A and Challenger B are friends, B cannot prove to A that they didn't challenge them—creating a trustless betrayal incentive.

### Quality-Over-Quantity Binding

**The Dilution Penalty:** Proposers submitting **>3 solutions per day** face cognitive entropy decay:

**`Quality_Multiplier = max(0.5, 1 - (Submissions_Today - 3) × 0.15)`**

- Fourth submission = **85%** emissions
- Fifth = **70%**

This prevents spam attacks that flood validators with noise.

**Challenger Precision Incentives:** Challengers receive a **Discovery Premium** only for first valid challenge to a specific node. Subsequent challengers to the same flaw receive diminishing returns (**50%, 25%, 10%**), preventing "piggybacking" on others' research.

---

## Validator Alignment: The Calibration Trap

### The Informed Minority Problem

**The Risk:** Validators might lazily vote with the majority to avoid slashing, creating an information cascade where no one actually verifies.

**The Solution: Private Scoring with Public Revelation**

- Validators submit **encrypted votes** during the adjudication window (commit-reveal scheme)
- Consensus is calculated **only after** the window closes
- **Late Reveal Penalty:** Validators revealing after the deadline lose **50%** of rewards regardless of correctness

**Alignment Effect:** You cannot see which way the wind is blowing before voting. You must independently verify or risk being wrong in a public vote.

### The Calibration Gradient

Validators are ranked on a **Brier Score** (probability calibration):

**`Brier_Penalty = (Validator_Confidence - Consensus_Margin)²`**

- If you vote **90% confident** but consensus is **51/49**, you are "overconfident" and penalized
- If you vote **51% confident** but consensus is **90/10**, you are "underconfident" and penalized

**Long-term Alignment:** Validators with poor calibration drift to the bottom of the weight distribution, eventually receiving **<1%** of validator emissions. They are phase-shifted out of the active set organically.

### Hardware Commitment & Sunk Costs

**Validator Tiers** create sticky capital:

| Tier | Minimum Stake | Hardware Requirement | Lock Period | Exit Penalty |
|------|---------------|---------------------|-------------|--------------|
| Scout | 100 TAO | Consumer GPU (RTX 4090) | 7 days | 5% burn |
| Auditor | 1,000 TAO | A100/H100 | 30 days | 10% burn |
| Arbiter | 10,000 TAO | Multi-node cluster | 90 days | 20% burn |

**Alignment Logic:** The **20% exit penalty** for Arbiters means they must believe the subnet will survive **>1 year** to recoup hardware costs. This filters for long-term aligned validators who actively improve protocol security rather than extract short-term MEV.

---

## Cross-Actor Alignment: The Virtuous Cycle

### The Client-Miner-Validator Trilemma

Traditional markets suffer from adverse selection: clients don't know quality, so they pay average prices, driving out high-quality providers.

**Dialectic's Fix: Adversarial Certification as Collateral**

- Proposers effectively post **collateral** (their stake) that Challengers can win
- This collateral is **verifiable on-chain**, creating a bonding curve of trust
- Clients pay **premium rates (2x base)** for reasoning with **>100 TAO** in challenged-but-survived collateral

**Alignment:** Miners want high collateral at risk (signals quality) but need Challengers to test them (proves quality). Challengers want high-quality targets (bigger jackpots). Validators want high-stakes debates (higher fees). All three want expensive-looking, rigorous truth.

### The "Doomsday" Scenario Resistance

**Scenario:** A cartel of Proposers and Challengers collude to fake debates and split rewards.

**Counter-Mechanisms:**

1. **Independent Validation:** Validators are randomly selected from the global pool; cartel must corrupt **>67%** of stake-weighted validators to guarantee fake wins

2. **Client Oracle Injection:** Enterprise clients can inject **"Canary Tasks"**—problems with known objectively correct answers. If the cartel gets these wrong (because they aren't actually verifying), they are slashed heavily (**-50% RS**)

3. **Entropy Requirements:** Reasoning trees must contain novel cryptographic entropy (hashes of recent block headers) proving real-time computation, preventing replay of old debates

### Temporal Consistency: The Multi-Game

Dialectic is designed as an indefinitely repeated game with open boundaries:

**`Lifetime_Value = Σ (Current_Emission × Discount_Rate^t) + (Exit_Liquidity_Value)`**

Where **`Exit_Liquidity_Value = Reputation_Score × 0.1 TAO`**

- **High Discount Rate (impatient miners):** Must extract maximum now, incentivizes low-effort spam
  - **System Response:** High decay rate on reputation for low-quality work makes "maximum extraction" actually lower than "steady quality" over 6 months
  - **Result:** Rational actors choose patience

---

## Emergent Alignment: The Truth Premium

Ultimately, the subnet aligns all parties toward objective logical validity because:

- **For Proposers:** Only objectively valid reasoning survives challenges → Only survivors earn long-term reputation → Only reputation earns sustainable yield
- **For Challengers:** Only objectively invalid reasoning can be profitably challenged → Must develop superior detection capability to find flaws before others → Capability requires understanding truth
- **For Validators:** Only objectively correct adjudication maintains calibration → Miscalibration leads to exponential emission loss → Must accurately model truth to survive

**The Nash Equilibrium:** All parties independently pursuing maximum TAO extraction converge on verifiable truth as the dominant strategy.

---

## Visual Summary: The "Alignment Triangle"

The incentive architecture creates a stable equilibrium through three mutually reinforcing pressure vectors:

  Clients (Demand)
       /\
      /  \
     /    \
    /      \
   /        \
Miners (Supply) — Validators (Arbitration)


**Vector 1: Client → Miner**

Clients demand bulletproof reasoning. Miners supply it or get slashed. The **"Canary Task"** mechanism ensures clients can verify quality without trusting the subnet—if a miner fails a known-answer problem, they're economically ejected.

**Vector 2: Miner → Validator**

Miners need validators to recognize valid reasoning. Validators need miners to generate high-stakes challenges to justify their fees. The **Calibration Scoring** ensures validators must be accurate to survive, creating a "market for judgment" where only precise adjudicators earn recurring revenue.

**Vector 3: Validator → Client**

Validators implicitly guarantee the network's output quality. Clients pay premiums for this guarantee. The **"Result Insurance"** mechanism (200% refunds on failed validations) makes validators the ultimate backstop for client trust.

### The Equilibrium Condition

At the center of this triangle is **TAO**. Each actor must acquire and stake TAO to participate. As the subnet produces more verified truths, client demand increases, driving TAO price appreciation. This appreciation increases the value of:

- Miner block rewards (higher $/TAO)
- Validator staking yields (higher $/TAO)
- Challenger jackpots (higher $/TAO)

Thus, all three actors are **long TAO** and must protect the network's reputation for truthfulness to protect their own financial positions. This creates the **"Skin in the Game" Triangle**—a three-sided mutual hostage situation where defecting from honest play destroys one's own TAO holdings.

---

## Conclusion: Why This Works

Traditional AI safety relies on alignment through architecture (designing models that "want" to be helpful) or alignment through oversight (humans monitoring AI). Dialectic achieves **alignment through economics**—it doesn't ask participants to be good; it makes being good the only profitable strategy.

Miners can't cheat because challengers are paid to catch them.
Challengers can't spam because stakes are slashed for frivolous attacks.
Validators can't collude because calibration scoring makes lazy voting economically suicidal.
Clients can't free-ride because they must pay for quality or receive none.
The result is a spontaneous order—a decentralized market that produces truth as a byproduct of rational self-interest. This is the "Adversarial Genesis" not just of a subnet, but of a new primitive: cryptographic truth certificates that can underpin the next generation of high-stakes AI applications.
