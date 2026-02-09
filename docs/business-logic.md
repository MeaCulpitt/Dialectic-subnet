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

## Who Are Our Customers?

### Primary Customers: Proposers

Proposers pay through stake-at-risk. They want verified reasoning for credibility.

**DeFi Governance Contributors**
- Compound, Aave, MakerDAO, Uniswap proposal authors
- Currently: Write proposals, hope voters read them, face no penalty for bad reasoning
- With Dialectic: Submit proposals as reasoning trees, stake TAO, earn "survived challenge" credibility
- Why they pay: Proposals that survive adversarial review carry more weight in votes

**Protocol Teams Pre-Vote**
- Teams proposing major parameter changes, token migrations, or treasury allocations
- Currently: Internal review, maybe forum discussion, then vote
- With Dialectic: Formal adversarial review before vote, demonstrates rigor
- Why they pay: Reduces governance attack surface, signals confidence

**Security Teams Post-Audit**
- Projects that paid $100k+ for a one-time audit
- Currently: Audit report sits in a PDF, code evolves, assumptions break
- With Dialectic: Continuous adversarial coverage on security reasoning
- Why they pay: Audit is a snapshot; Dialectic is ongoing

**Crypto Research Firms**
- Messari, Delphi Digital, Galaxy Research, independent analysts
- Currently: Publish investment theses with no immediate accountability
- With Dialectic: Submit theses as reasoning trees, stake reputation
- Why they pay: "Dialectic Verified" becomes credibility signal for subscribers

**Token Projects Pre-Launch**
- Teams designing tokenomics, emission schedules, incentive mechanisms
- Currently: Internal review, maybe advisor feedback
- With Dialectic: Adversarial stress-test before mainnet
- Why they pay: Flawed tokenomics are expensive to fix post-launch

### Secondary Customers: Consumers (Future API)

Once "Dialectic Verified" means something, consumers pay to query verification status.

**Voters in DAO Governance**
- Check if a proposal survived adversarial review before voting
- Pay per query or via subscription

**Due Diligence Teams**
- Funds, family offices, institutional investors
- Query verification status of research memos, audit reasoning
- Pay for API access + historical dispute data

**Integration Partners**
- Governance platforms (Snapshot, Tally) embed Dialectic status
- Pay for API access + white-label verification badges

---

## Who Earns?

### Challengers

Security researchers, auditors, analysts who profit from finding flaws.

**Current Bug Bounty Hunters**
- Immunefi, HackerOne participants
- Currently: Find code bugs, earn bounties
- With Dialectic: Find reasoning flaws, earn challenge rewards
- New venue: Expands from "is the code broken?" to "is the logic broken?"

**Independent Analysts**
- Crypto Twitter researchers, governance watchers
- Currently: Post threads pointing out flaws, earn followers
- With Dialectic: Post challenges, earn TAO
- Monetization path: Turn analysis into income

**Professional Adversaries**
- Firms that specialize in red-teaming
- Currently: Hired for one-off engagements
- With Dialectic: Continuous earning from challenge pool
- Business model: Adversarial review as a service

### Validators

Domain experts who adjudicate disputes.

**Governance Specialists**
- People who deeply understand DeFi protocol mechanics
- Earn by accurately judging governance-related disputes

**Security Experts**
- Auditors, security researchers
- Earn by adjudicating smart contract reasoning disputes

**Legal/Compliance Professionals**
- As Dialectic expands to legal domain
- Earn by judging regulatory and contractual reasoning

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

---
