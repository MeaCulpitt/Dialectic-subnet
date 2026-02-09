# Miner Design

Dialectic miners operate in two roles: **Proposers** (submit reasoning) and **Challengers** (attack reasoning). This document covers both.

---

## Role Overview

| Role | Primary Activity | Revenue Source | Risk |
|------|------------------|----------------|------|
| Proposer | Generate structured reasoning trees | Emissions (60% pool) | Stake slashed on successful challenges |
| Challenger | Identify and attack reasoning flaws | Challenge rewards (30% pool) | Stake lost on rejected challenges |

Miners can operate as one or both roles. Running both creates natural hedging but requires distinct skill sets.

**Important:** A miner cannot challenge their own proposals. Self-challenges are rejected at the protocol level, and attempts to self-challenge via multiple accounts are detected through statistical analysis and result in slashing for both accounts.

---

## Proposer Implementation

### Input: Task Assignment

Proposers receive tasks from the validator network:

    {
      "task_id": "dt_20260209_0847",
      "domain": "defi_governance",
      "prompt": "Evaluate: Should Aave deploy on Arbitrum Orbit chains?",
      "constraints": {
        "max_depth": 5,
        "min_nodes": 4,
        "evidence_required": true
      },
      "deadline": "2026-02-09T14:47:00Z",
      "base_reward": 0.5
    }

### Output: Reasoning Tree

Proposers submit a Merkle-committed reasoning tree:

    {
      "task_id": "dt_20260209_0847",
      "tree": {
        "root": {
          "id": "n0",
          "claim": "Aave should deploy on Arbitrum Orbit chains",
          "type": "conclusion",
          "children": ["n1", "n2", "n3"]
        },
        "nodes": [
          {
            "id": "n1",
            "claim": "Orbit chains have sufficient TVL to justify deployment costs",
            "type": "premise",
            "evidence": {
              "source": "L2Beat",
              "data": "Combined Orbit TVL: $2.1B as of Feb 2026",
              "url": "https://l2beat.com/scaling/summary"
            },
            "children": []
          },
          {
            "id": "n2", 
            "claim": "Deployment cost is minimal due to existing Arbitrum integration",
            "type": "premise",
            "evidence": {
              "source": "Aave governance forum",
              "data": "Estimated deployment: 40 dev-hours, $15k audit"
            },
            "children": ["n2a"]
          },
          {
            "id": "n2a",
            "claim": "Existing Arbitrum One contracts are 95% compatible",
            "type": "sub_premise",
            "evidence": {
              "source": "Technical analysis",
              "data": "Only bridge contracts require modification"
            },
            "children": []
          },
          {
            "id": "n3",
            "claim": "First-mover advantage in Orbit ecosystem",
            "type": "premise",
            "evidence": {
              "source": "Competitive analysis",
              "data": "No major lending protocol deployed on Orbit chains yet"
            },
            "children": []
          }
        ]
      },
      "merkle_root": "0x7f3a...",
      "stake": 50,
      "proposer_hotkey": "5Hq8..."
    }

### Node Types

| Type | Description | Evidence Required |
|------|-------------|-------------------|
| conclusion | Final claim (root) | No (derived from premises) |
| premise | Direct support for conclusion | Yes |
| sub_premise | Support for a premise | Yes |
| rebuttal | Preemptive counter-argument | Optional |
| qualifier | Scope limitation | No |

### Scoring Dimensions

| Dimension | Weight | Measurement |
|-----------|--------|-------------|
| Survival rate | 40% | % of trees unchallenged or successfully defended |
| Structural quality | 25% | Depth, balance, evidence coverage |
| Challenge attraction | 20% | Trees that attract challenges but survive score higher |
| Response time | 15% | Speed of defense when challenged |

---

## Challenger Implementation

### Input: Candidate Trees

Challengers receive recently-submitted trees for analysis:

    {
      "available_trees": [
        {
          "task_id": "dt_20260209_0847",
          "merkle_root": "0x7f3a...",
          "proposer_stake": 50,
          "proposer_reputation": 1.15,
          "challenge_deadline": "2026-02-09T14:47:00Z",
          "domain": "defi_governance"
        }
      ]
    }

Note: Trees where the challenger's hotkey matches the proposer's hotkey are automatically excluded from the available set.

### Output: Challenge Submission

    {
      "task_id": "dt_20260209_0847",
      "challenge": {
        "target_node": "n1",
        "attack_type": "factual_error",
        "argument": "The L2Beat figure includes non-Orbit Arbitrum chains. Actual Orbit-only TVL is $340M.",
        "evidence": {
          "source": "L2Beat filtered view",
          "data": "Orbit chains specifically: $340M combined"
        },
        "stake": 15
      },
      "challenger_hotkey": "5Gx9..."
    }

### Attack Types

| Type | Description | Reward Multiplier |
|------|-------------|-------------------|
| factual_error | Claimed evidence is incorrect | 2.0x |
| logical_fallacy | Reasoning doesn't follow | 2.5x |
| missing_context | Critical information omitted | 1.5x |
| contradiction | Internal inconsistency | 3.0x |
| outdated | Evidence no longer current | 1.5x |

---

## Defense Protocol

When challenged, proposers have 2 hours to respond:

**1. Refute with counter-evidence:**

    {
      "defense_type": "refute",
      "response": "The L2Beat figure cited includes only Orbit chains. Here is the methodology...",
      "evidence": { "source": "L2Beat methodology doc" }
    }

**2. Concede and limit damage:**

    {
      "defense_type": "concede",
      "affected_nodes": ["n1"],
      "tree_still_valid": true,
      "explanation": "Accepting the correction. Conclusion still holds via n2 and n3."
    }

| Outcome | Proposer Impact | Challenger Impact |
|---------|-----------------|-------------------|
| Successful refutation | +reputation, keep stake | -50% stake |
| Concession | Stake slashed, reputation hit | Full reward |
| No response | Maximum slash | Full reward + bonus |

---

## Hardware Requirements

### Proposer

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 8 GB | 32 GB |
| GPU | Optional | RTX 3080+ for local LLM |
| Storage | 50 GB SSD | 500 GB NVMe |

Proposers can use API-based LLMs or run local models.

### Challenger

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 16 GB | 64 GB |
| GPU | Optional | RTX 4090 for deep analysis |
| Storage | 100 GB SSD | 1 TB NVMe |

---

## Running a Miner

    git clone https://github.com/MeaCulpitt/Dialectic-subnet.git
    cd Dialectic-subnet
    pip install -r requirements.txt
    
    # Proposer
    python neurons/proposer.py \
      --netuid <NETUID> \
      --wallet.name <WALLET> \
      --wallet.hotkey <HOTKEY> \
      --stake 50
    
    # Challenger
    python neurons/challenger.py \
      --netuid <NETUID> \
      --wallet.name <WALLET> \
      --wallet.hotkey <HOTKEY> \
      --min_ev 0.5

---

## Best Practices

### For Proposers
- Cite primary sources (harder to challenge)
- Include timestamps on evidence
- Preempt obvious objections with rebuttal nodes
- Stake proportionally to confidence

### For Challengers
- Verify before challenging (failed challenges are expensive)
- Target weak nodes, not strong ones
- Read the full tree for context
- Specialize in domains where you have expertise

---
