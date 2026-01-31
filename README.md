# Dialectic: The Adversarial Intelligence Layer

[![Bittensor](https://img.shields.io/badge/Bittensor-Subnet-blue)](https://bittensor.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Dialectic** is a Bittensor subnet implementing cryptographic Proof-of-Intelligence (PoI) through adversarial reasoning markets. Miners submit Merkleized reasoning trees; challengers stake capital to attack logical flaws; validators adjudicate via stochastic sampling.

## Core Innovation

Traditional AI verification asks: *"Is this output correct?"*  
Dialectic asks: *"Can this reasoning withstand economically-motivated adversaries?"*

### The Triadic Mechanism
- **Proposers** (60%): Generate Chain-of-Thought reasoning with full Merkle commitment
- **Challengers** (30%): Stake TAO to attack specific logical nodes (profit from finding flaws)  
- **Validators** (10%): Adjudicate via Stochastic Branch Verification (O(log n) sampling)

## Documentation

- **[Incentive & Mechanism Design](./docs/incentive-design.md)** - Triadic game theory and cryptoeconomics
- **[Emission Logic](./docs/emission-logic.md)** - 60/30/10 distribution, slashing, and staking tiers
- **[Proof of Intelligence](./docs/proof-of-intelligence.md)** - Formal proof of why this constitutes PoI
- **[High-Level Algorithm](./docs/algorithm.md)** - Task flow from assignment to reward distribution
- **[Miner Design](./docs/miner-design.md)** - Specs, I/O formats, and performance dimensions
- **[Validator Design](./docs/validator-design.md)** - Scoring, tiers, and calibration mechanisms
- **[Business Logic](./docs/business-logic.md)** - Market rationale and competitive landscape
- **[Go-To-Market](./docs/go-to-market.md)** - Launch strategy and bootstrapping incentives

## Economic Parameters

| Parameter | Value |
|-----------|-------|
| Emission Split (Proposer/Challenger/Validator) | 60/30/10 |
| Challenge Window | 6 hours |
| Defense Window | 2 hours |
| Min Proposer Stake | 100 TAO (scalable by difficulty) |
| Validator Tiers | Scout/Auditor/Arbiter |

## Quick Start

```bash
# Clone repository
git clone https://github.com/[your-username]/dialectic-subnet.git

# Install dependencies
pip install -r requirements.txt

# Register as Proposer
python -m src.miner.proposer --stake 1000 --hotkey <your_key>
