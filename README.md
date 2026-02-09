# Dialectic: Adversarial verification for AI reasoning

Dialectic is a Bittensor subnet where AI reasoning is stress-tested by economic adversaries. Proposers submit structured reasoning. Challengers stake TAO to attack flaws. Validators adjudicate. Truth emerges from economic pressure, not authority.

---

## The Problem

AI systems produce reasoning that *looks* convincing but may contain subtle flaws. Current verification approaches fall short:

- **Human review** doesn't scale
- **Consensus** rewards popular answers, not correct ones
- **ZKML** proves computation was executed, not that the logic is sound
- **Prediction markets** verify outcomes, not the reasoning that produced them

There's no mechanism for adversarial verification of *reasoning quality itself*.

---

## How Dialectic Works

### The Mechanism

Three roles, economically aligned toward truth:

| Role | Share | Function |
|------|-------|----------|
| **Proposer** | 60% | Submits structured reasoning with cryptographic commitment |
| **Challenger** | 30% | Stakes TAO to attack specific logical steps |
| **Validator** | 10% | Samples and adjudicates disputes |

### A Worked Example

**Task:** "Should MakerDAO increase the DAI stability fee from 5% to 7%?"

**1. Proposer submits reasoning tree:**

    ROOT: Recommend increasing to 7%
    ├── CLAIM: DAI is trading below peg ($0.997 avg last 30 days)
    │   └── EVIDENCE: Chainlink price feed data
    ├── CLAIM: Higher rates reduce DAI supply, supporting peg
    │   └── EVIDENCE: Historical correlation (R²=0.73)
    ├── CLAIM: Competing stablecoin rates are 6-8%
    │   └── EVIDENCE: Aave/Compound current rates
    └── CLAIM: 2% increase is within historical adjustment range
        └── EVIDENCE: Previous adjustments ranged 1-3%

Each node is Merkle-committed. The proposer stakes 50 TAO.

**2. Challenger attacks a weak node:**

A challenger notices the correlation claim is misleading — it's based on a period when rates moved in one direction. They stake 20 TAO targeting that specific branch:

    CHALLENGE: Node 2.1 (historical correlation)
    ATTACK: Selection bias — correlation calculated only during 
            rate-increase periods. Full dataset shows R²=0.31.
    STAKE: 20 TAO

**3. Proposer defends or concedes:**

The proposer has 2 hours to provide counter-evidence. If they can't refute the challenge, the challenger wins their stake plus a portion of the proposer's.

**4. Validator adjudicates:**

If disputed, validators sample the specific branch. They don't review the entire tree — just the contested node. Their verdict determines stake distribution.

**Outcome:** The challenger profits from finding the flaw. Future proposers are incentivized to use complete datasets. The reasoning quality improves.

---

## Why This Works

### Economic Pressure Finds Flaws

Challengers are bounty hunters. They profit by finding errors others missed. This creates continuous adversarial pressure on reasoning quality.

### Skin in the Game

Both sides stake capital:
- Proposers can't submit sloppy reasoning — they'll lose their stake
- Challengers can't make frivolous attacks — they'll lose theirs
- The economic cost of being wrong disciplines both parties

### Efficient Verification

Validators don't check everything. They sample contested branches using O(log n) verification. This scales to complex reasoning trees without proportional validator burden.

### Reputation Compounds

High-quality proposers build reputation over time. Their reasoning carries more weight, attracting fewer challenges. Poor performers see their reputation decay, reducing their effective stake.

---

## Use Cases

**DeFi Governance:** Protocol proposals with structured justifications. Challengers stress-test assumptions before votes.

**Smart Contract Audits:** Security reasoning submitted as trees. Economic incentives to find the flaws auditors missed.

**Legal Analysis:** Contract interpretation with explicit logical steps. Adversarial review before execution.

**Research Validation:** Scientific reasoning structured for challenge. Pre-publication stress-testing.

**Investment Theses:** Structured cases for investment decisions. Adversarial due diligence.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Mechanism Design](./docs/mechanism_design.md) | Game theory, incentive structure, equilibrium analysis |
| [Miner Guide](./docs/miner_design.md) | Proposer and Challenger implementation |
| [Validator Guide](./docs/validator_design.md) | Adjudication protocol and scoring |
| [Business Logic](./docs/business_logic.md) | Market positioning and competitive analysis |
| [Go-To-Market](./docs/go_to_market.md) | Launch strategy and growth plan |

---

## Economic Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Emission Split | 60/30/10 | Rewards reasoning production while funding adversarial pressure |
| Challenge Window | 6 hours | Sufficient time for thorough analysis |
| Defense Window | 2 hours | Prevents indefinite delays |
| Min Proposer Stake | 50 TAO | Low enough for entry, high enough for skin in the game |
| Min Challenge Stake | 10 TAO | Accessible but non-trivial |
| Reputation Decay | 5%/epoch | Maintains pressure for continued quality |

---

## Quick Start

    # Clone and install
    git clone https://github.com/MeaCulpitt/Dialectic-subnet.git
    cd Dialectic-subnet
    pip install -r requirements.txt
    
    # Run as Proposer
    python neurons/proposer.py --netuid <NETUID> --wallet.name <WALLET> --wallet.hotkey <HOTKEY>
    
    # Run as Challenger  
    python neurons/challenger.py --netuid <NETUID> --wallet.name <WALLET> --wallet.hotkey <HOTKEY>

See [Miner Guide](./docs/miner_design.md) for detailed setup.

---

## Why Bittensor

Dialectic requires:
- Native token staking (TAO provides this)
- Decentralized validator set (subnet architecture provides this)
- Emission incentives (Yuma Consensus provides this)

Bittensor's infrastructure handles the economic layer. Dialectic adds the adversarial verification mechanism.

---

## Status

Dialectic is in development for Bittensor Subnet Ideathon 2026.

**License:** MIT
</doc>

---
