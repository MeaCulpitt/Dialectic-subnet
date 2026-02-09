# Business Logic

This document covers Dialectic's market positioning, competitive landscape, and value proposition.

---

## Market Problem

AI systems increasingly make high-stakes decisions: investment analysis, legal reasoning, governance proposals, security audits. The reasoning behind these decisions is often opaque and unverified.

**Current verification approaches fail:**

| Approach | What It Verifies | What It Misses |
|----------|------------------|----------------|
| Human review | Reasoning quality | Doesn't scale |
| Consensus | Popular opinion | Popularity ≠ correctness |
| ZKML | Computation executed correctly | Logic soundness |
| Prediction markets | Outcome accuracy | The reasoning that produced it |
| Inference consensus | Output consistency | Consistent errors |

None verify that *the reasoning itself* is sound.

---

## Dialectic's Solution

**Adversarial verification of reasoning quality.**

Instead of asking "is this answer correct?" Dialectic asks "can this reasoning withstand economically-motivated attack?"

The mechanism:
1. Proposers submit structured reasoning with economic stake
2. Challengers profit by finding flaws
3. Validators adjudicate disputes
4. Economic pressure drives quality

This creates a market for reasoning verification where truth-finding is incentive-compatible.

---

## Competitive Landscape

### vs. ZKML (EZKL, Modulus, Giza)

| Dimension | ZKML | Dialectic |
|-----------|------|-----------|
| Verifies | Computation integrity | Reasoning quality |
| Proves | "This model produced this output" | "This reasoning withstands scrutiny" |
| Cost | High (ZK proving) | Lower (economic, not cryptographic) |
| Scope | Narrow (specific models) | Broad (any structured reasoning) |

**Relationship:** Complementary. ZKML proves the computation; Dialectic proves the logic.

### vs. Prediction Markets (Polymarket, Metaculus)

| Dimension | Prediction Markets | Dialectic |
|-----------|-------------------|-----------|
| Verifies | Outcome probability | Reasoning soundness |
| Resolution | External events | Internal logic |
| Timeline | Waits for outcomes | Immediate verification |
| Value | "What will happen?" | "Is this analysis sound?" |

**Relationship:** Different questions. Prediction markets verify outcomes; Dialectic verifies the reasoning used to predict them.

### vs. Inference Subnets (SN1, SN18, etc.)

| Dimension | Inference Subnets | Dialectic |
|-----------|-------------------|-----------|
| Focus | Output generation | Output verification |
| Scoring | Consistency/quality | Adversarial survival |
| Role | Production | Assurance |

**Relationship:** Complementary. Inference subnets produce reasoning; Dialectic stress-tests it.

### vs. Audit Firms

| Dimension | Traditional Audits | Dialectic |
|-----------|-------------------|-----------|
| Model | Hired experts | Economic bounties |
| Incentive | Reputation (weak) | Profit (strong) |
| Coverage | Sampled | Continuous |
| Speed | Weeks/months | Hours |
| Cost | $50k-500k | Market-driven |

**Relationship:** Competitive for some use cases, complementary for others. Audits provide depth; Dialectic provides breadth and speed.

---

## Target Use Cases

### Tier 1: Immediate Value

**DeFi Governance**
- Protocol proposals require structured justification
- Challengers stress-test assumptions before votes
- Reduces governance attacks and poorly-reasoned proposals
- *Market size:* $50B+ in governed TVL

**Smart Contract Security**
- Audit reasoning submitted as trees
- Economic incentive to find what auditors missed
- Continuous post-deployment monitoring
- *Market size:* $500M+ annual audit spend

### Tier 2: Near-Term Expansion

**Legal Analysis**
- Contract interpretation with explicit logic
- Adversarial review before execution
- Regulatory compliance reasoning
- *Market size:* Legal AI market $15B by 2027

**Investment Research**
- Structured investment theses
- Adversarial due diligence
- Track record verification
- *Market size:* Research spend $30B+ annually

### Tier 3: Long-Term Vision

**Scientific Reasoning**
- Pre-publication adversarial review
- Replication crisis mitigation
- Structured methodology verification

**AI Alignment**
- Verify AI reasoning chains
- Adversarial testing of AI decisions
- Human-AI collaboration verification

---

## Value Proposition by Stakeholder

### For Proposers (Reasoning Producers)

- **Credibility:** Survived-challenge status is valuable signal
- **Monetization:** Earn TAO for quality reasoning
- **Improvement:** Challenges identify blind spots
- **Track record:** Reputation accumulates over time

### For Challengers (Adversarial Reviewers)

- **Profit:** Earn by finding errors others miss
- **Specialization:** Domain expertise becomes valuable
- **Scalability:** Review many proposals, challenge few
- **Independence:** No client relationships to manage

### For Validators (Adjudicators)

- **Yield:** Earn 10% of emissions for judgment
- **Expertise monetization:** Domain knowledge → calibration → rewards
- **Network effects:** More disputes → more opportunity

### For End Users (Reasoning Consumers)

- **Trust:** Adversarially-verified reasoning is more reliable
- **Efficiency:** Skip manual review for survived-challenge content
- **Auditability:** Full dispute history available
- **Price discovery:** Market determines verification cost

---

## Revenue Model

### Network Revenue

Dialectic is a Bittensor subnet. Revenue flows through TAO emissions:

| Source | Mechanism |
|--------|-----------|
| Block emissions | TAO distributed to subnet based on network weight |
| Registration fees | New participants pay to register |
| Stake lockups | Staked TAO provides network security |

### External Revenue (Future)

As the network matures, external revenue sources include:

| Source | Mechanism |
|--------|-----------|
| Verification API | Pay-per-query for reasoning verification |
| Enterprise integration | Custom domains, SLAs, private instances |
| Certification | "Dialectic Verified" badge licensing |

---

## Network Effects

### Supply Side

More proposers → more reasoning to challenge → more challenger opportunity → more challengers → more adversarial pressure → higher quality → more proposers (quality attracts quality)

### Demand Side

More verified reasoning → more consumer trust → more demand → higher rewards → more participants

### Data Effects

More disputes → better calibration data → better validator scoring → fairer outcomes → more trust → more disputes

---

## Moat

**1. Economic Security**
- Staked TAO creates attack cost
- Higher stake = harder to manipulate
- Network effect compounds security

**2. Reputation Data**
- Historical performance is non-transferable
- New entrants start from scratch
- Incumbent advantage accumulates

**3. Domain Expertise**
- Specialized challengers develop expertise
- Expertise is hard to replicate
- Quality gap widens over time

**4. Integration Lock-in**
- Once integrated into governance/audit flows
- Switching costs are high
- Embedded in decision processes

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Low initial liquidity | Bootstrap incentives, reduced stakes at launch |
| Collusion | Statistical detection, reputation penalties |
| Validator capture | Random assignment, multi-tier consensus |
| Quality ceiling | Difficulty adjustment, domain expansion |
| Regulatory | Focus on verification, not advice |
</doc>

---
