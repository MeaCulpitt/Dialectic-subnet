# Validator Design: The Adjudication Layer

## Scoring and Evaluation Methodology

### Stochastic Branch Verification (SBV)

Validators **do not** score full reasoning trees (computationally prohibitive). Instead, they employ **probabilistic verification**:

*   **Randomized Depth Sampling**: When a challenge occurs at node *N*, validators randomly select *k* ancestral branches (where `k = log₂(tree depth)`) to verify **logical consistency** across the proof path.

*   **Formal Logic Probes**: Deploy lightweight **SMT solvers** (Z3) for mathematical claims; use **NLI models** (Natural Language Inference) for semantic entailment in text-based reasoning.

*   **Adversarial Cross-Examination**: Validators prompt miners with **follow-up questions** (*Q*) derived from challenged nodes; responses must maintain **logical equivalence** with the original submission under perturbation.

---

#### The Scoring Function

Validator_Score = (Calibration × 0.4) + (Efficiency × 0.3) + (Coverage × 0.3)

Where:

*   **Calibration** = `1 - |Your_Vote - Consensus_Result|`  
    *Heavily penalized for being wrong when consensus is strong (>80%).*

*   **Efficiency** = `1 / (Compute_Cost × Time_to_Verify)`  
    *Faster verification with fewer LLM calls = **higher score**.*

*   **Coverage** = `Unique_Branches_Verified / Total_Branches_Challenged`  
    *Prevents validators from "cherry-picking" only easy, shallow nodes.*

#### Consensus Mechanisms

*   **Quadratic Voting**: Validators stake TAO per decision; stake weight follows **`√stake`** to prevent **whale dominance**.

*   **Truth Latency Adjustment**: If a validator is "**early correct**" (votes correctly before the **67%** threshold is reached), they receive a **1.5x** emission multiplier for identifying truth *before* crowd consensus forms.

---

## Evaluation Cadence

### Phased Verification Windows

*   **Preliminary Scan (Continuous)**: Validators run automated **coherence checks** (syntax validation, citation verification, basic logical fallacy detection) within **15 minutes** of submission. This filters obvious garbage before the challenge phase opens.

*   **Challenge Arbitration (Event-driven)**: When a challenge is lodged, validators enter a strict **4-hour adjudication window** to submit verdicts on disputed branches.

*   **Settlement Epochs (Every 12 hours)**: **Batch processing** of all resolved debates; reward distribution and slashing applied **atomically**.

*   **Appeal Quorum (Weekly)**: The top **5%** most contested resolutions enter a **48-hour** secondary review by **high-reputation validators** (stake >**1,000 TAO**). These arbiters can overturn primary decisions with a **75% supermajority** *(prevents 51% validator collusion)*.

### Dynamic Evaluation Load

*   Validators specify `max_concurrent_verifications` based on hardware constraints; the subnet automatically routes challenges to available validators using **consistent hashing** on `problem_id`.

*   **Cooldown Period**: Validators **cannot** evaluate consecutive submissions from the same miner. This prevents gaming through validator-miner relationship building.

---

## Validator Incentive Alignment

### "Skin in the Game" Slashing Conditions

*   **Consensus Divergence Penalty**: If a validator votes against the eventual majority—and that majority is **>80%** confident—the validator loses **5%** of staked TAO, distributed to validators who voted correctly.

*   **Lazy Validation Detection**: Validators who consistently vote "**Agree**" without submitting **verification traces** (ZK-proof of computation or signed API logs from LLM calls) receive **exponentially decaying rewards** (halving every epoch of lazy behavior).

*   **Challenge Collusion Resistance**: Validators who approve **>3 challenges** from the same challenger address within **24 hours** trigger "**Suspicion Mode**":
    *   Their votes require **90%** consensus thresholds for **72 hours**.
    *   Their rewards are **escrowed** pending manual review by the subnet owner.

### Long-term Alignment Mechanisms

*   **Reputation Decay**: Validator effectiveness scores decay by **2% per day** of inactivity. This prevents "**sleeping giant**" validators from dominating emission history without current participation.

*   **Proportional Representation**: Emissions weighted by:  
    **`stake × reputation_score × diversity_factor`**  
    Where **diversity_factor** penalizes validators running identical models/configurations (ensures **decentralized verification methodologies**).

*   **Treasury Alignment**: Top **10%** of validators (by accuracy) gain **governance rights** over subnet hyperparameters (e.g., challenge window duration, minimum stake thresholds), aligning them with **long-term subnet health** rather than short-term extraction.

---

## Validator Attraction Design

### The Hardware Gradient

Three distinct validator tiers create a "**verification market**" where validators specialize based on capital/hardware, preventing centralization while ensuring every reasoning branch faces **economically-motivated scrutiny**:

1.  **Scouts**: Lightweight verification of shallow logic.  
    *Rewards: **Lower** / Hardware: **Consumer GPUs** (accessible)*

2.  **Auditors**: Deep verification utilizing heavy LLMs.  
    *Rewards: **Higher** / Hardware: **A100s** (professional)*

3.  **Arbiters**: Final appeal layer for contested resolutions.  
    *Requirements: **Highest stake** / Rotation: **Monthly** (prevents stagnation)*

**Result**: A decentralized verification marketplace where **economic rationality** enforces truth.
