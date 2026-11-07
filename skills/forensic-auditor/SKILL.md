---
name: forensic-research-auditor
description: Audits scientific papers across a 7-Gate & 10-Domain Polyglot FastMCP & Cellular Sheaf Hypergraph Architecture (Rust petgraph, Z3 SMT, Julia Catlab, DuckDB PGQ, R, Python): (Gate 1-2) Provenance, Retraction Watch & Reagents, (Gate 3) GRIM/GRIMMER/DEBIT/SPRITE, Carlisle-Stouffer ANOVA, statcheck, 95% CI, 2nd-digit Benford, Cochran sparse tables (3.8), logit linearity (3.9), Excel-Trap covariance/PSD (3.10), continuous assay constant-CV (3.11) & blind GCD denominator N recovery (3.12), (Gate 3.5) Surya OCR + VLM charts, KM-IPD survival, TruFor/CAT-Net/DINOv2 splicing & Lean ImageTwin, (Gate 3.6) MedSAM/SAM 2/BiomedParse/TotalSegmentator anatomy masks, DICOM headers & cine-video forensics, (Gate 4-4.5) Spectrum/cutoff validity, Qualitative IRR kappa, Quote DAG & LLM stylometry, and (Gate 5) Multimodal Epistemic Hypergraph connecting Abstract, Assumptions, Methods, Findings, References/Recency, Author/COI Agendas & Conclusions.
---
# Forensic Research Auditor (6-Gate SOTA v3: Merged 10,000-Study Blind Benchmark, Lean ImageTwin, Excel-Trap/Assay Closers, Graph DAG/GNN & Qualitative Forensics Edition)

Synchronized with [`lauyeehow1986-hub/forensic_research_auditor`](https://github.com/lauyeehow1986-hub/forensic_research_auditor) (commits `4d8d353` and `cfae062`) and empirically grounded in the **10,000-Study Quintuple-Wave Blind Full-Text Benchmark + Wave 6 Multimodal Case-Control Suite** ([`lauyeehow1986-hub.github.io/forensic_research_auditor_validation/#blind-audit`](https://lauyeehow1986-hub.github.io/forensic_research_auditor_validation/#blind-audit)).

## Empirical Grounding: The 10,000-Study Quintuple-Wave Blind Benchmark & SOTA v3 Gap Closers

- **Baseline Waves 1–5 (10,000 Studies; 33,043 Tables; 345,533 Rows):**
  - **Tier-1 Definite Fraud Specificity:** **99.20%** (`8 / 1,000` clean controls flagged; Positive Likelihood Ratio $	ext{LR}^+ > 50.0$).
  - **Clean Control Specificity:** **86.00%** in Wave 5 (`860 / 1,000` clean controls passed; `76.34%` pooled across 5,000 controls), upgraded in SOTA v3 with **Multi-Item Subscale ($k$-item) & Survey-Weight Guardrails** to suppress false alarms on legitimate survey cohorts.
  - **Gate 3 Math Sensitivity:** `20.73%` pooled (`386 / 1,862`), reaching `80.81%` on strict-$N$ integer tables, upgraded in SOTA v3 with **Gates 3.8–3.12** specifically targeting the **4 Anatomies of Missed Retractions** (`Excel =AVERAGE()/=STDEV() Trap`, `Continuous Unbounded Assays`, `Header N Omission`, and `Narrative/Bar-Chart-Only Papers`).

## Core Workflow: The 6-Gate Lexicographic & 9-Domain FastMCP Architecture

### Gate 1: Provenance & Retraction Hygiene (`thinkingLevel: "low"`)
1. Check Crossref (`update-to`), Retraction Watch (`gitlab.com/crossref/retraction-watch-data`), Expressions of Concern, and PubPeer threads.
2. **Anti-Circularity Rule:** Report registry status separately from blind empirical table/image/graph detections. **Kill-Switch 1:** Halt on verified retraction or unresolved EoC.

### Gate 2: Paper-Mill, Tortured Phrases & Reagent Forensics (`thinkingLevel: "medium"`)
1. Screen against the Problematic Paper Screener (PPS) tortured phrases dictionary, ICLAC misidentified cell lines, and oligonucleotide BLAST homology (`Seek & Blastn` / `biomcp`). **Kill-Switch 2:** Halt if $\ge 1$ tortured phrase or invalidated reagent is found.

### Gate 3: Universal Table, Continuous Assay & Covariance Math (`mcp_servers/forensic_math_mcp.py` & `scripts/audit_paper.R`)
1. **Core Discrete & Continuous Sieves:** Run `GRIM`, `Analytic-GRIMMER` ($\sum x_i^2 \equiv \sum x_i \pmod 2$), `DEBIT`, `SPRITE` / Bhatia-Davis bounds (with multi-item scale $k$ and survey-weight guards), `Carlisle-Stouffer` RCT baseline ANOVA ($\Phi(Z_{	ext{pool}})$), `statcheck` 2D NHST recalculation, **95% CI symmetry/variance compression ($	ext{LR}=0.14$)/GRADE OIS imprecision ($	ext{LR}=0.40$)**, and scale-gated ($\ge 2.0$ orders) **2nd-Digit Benford + Synthetic Tabular DNR (`LR=0.10`)**.
2. **Gate 3.7 — Diagnostic 2x2 Contingency & Bootstrap Shrinkage (`run_diagnostic_2x2_audit`, `run_bootstrap_resampling_audit`):** Verify Bayes PPV/NPV against true clinical prevalence and check whether claimed bootstrap shrinkage was applied to deployed $eta$ coefficients.
3. **Gate 3.8 — Cochran Sparse Contingency Table Sieve (`audit_cochran_sparse_contingency_table`):** Flag $E_{ij} < 1.0$ or $> 20\%$ of cells $< 5.0$ tested with uncorrected Pearson $\chi^2$ instead of Fisher's exact test (`LR = 0.20`; `LR = 0.15` if Fisher $p \ge 0.05$).
4. **Gate 3.9 — Logit Linearity & Continuous Ratio Skewness (`run_logit_linearity_and_ratio_audit`):** Flag heavy-tailed biological ratios modeled linearly without spline/Box-Tidwell checks (`LR = 0.30`).
5. **Gate 3.10 — "Excel Trap" Pre-Post Covariance & PSD Sieve (`audit_excel_trap_pre_post_and_regression`):** Reconstruct implied pre-post correlation $r_{01} = rac{\sigma_0^2 + \sigma_1^2 - \sigma_\Delta^2}{2\sigma_0\sigma_1}$ (trigger **Kill-Switch 3.10** if $|r_{01}| > 1.03$), verify correlation matrix positive semi-definiteness ($\lambda_{\min}(R) \ge 0$), and check exact $F	ext{-to-}R^2$ regression identity.
6. **Gate 3.11 — Continuous Wet-Lab Assay Fold-Change & Constant-CV Sieve (`audit_continuous_assay_fold_change_and_cv`):** Flag Western blot/qPCR control-group `1.00 ± 0.00` two-sample $t$-test $df$ inflation (`LR = 0.25`), constant-CV bar templates ($	ext{CV}_{	ext{of CV}} < 0.012$ across $\ge 4$ groups, `LR = 0.10`), and ELISA OD 450nm $> 4.0$ saturation (`LR = 0.10`).
7. **Gate 3.12 — Blind Denominator ($N$) GCD Recovery (`recover_blind_column_denominator_n`):** Recover omitted column $N \in [5, 500]$ from categorical percentages (**Kill-Switch 3.12** if zero integer $N$ exists across $\ge 3$ percentages).

### Gate 3.5: OCR/VLM Chart Digitizer, KM-IPD Survival, Multi-Omics & Lean ImageTwin (`mcp_servers/forensic_chart_mcp.py` & `src/vision/`)
1. **Layout OCR & VLM Chart Transcription (`verify_vlm_bar_and_error_bar_pixels`, `transcribe_and_pipe_to_table_math`):** Extract bars/whiskers via MinerU/Surya OCR + Qwen2.5-VL / Gemini 3.8 Flash to catch `SE` whiskers plotted as `SD` (`LR = 0.15`), audit clinical scatterplot tail density (`LR = 0.20`), and pipe bar-chart/narrative values into Gate 3 math sieves.
2. **Guyot KM-IPD Survival & Z-Curve (`reconstruct_km_ipd_guyot`, `audit_p_curve_and_z_curve`):** Reconstruct interval survival events/censoring from KM curves (**Kill-Switch** on non-monotonicity or impossible at-risk counts) and test P-curve/Z-curve skewness (`LR = 0.20`).
3. **Manhattan & Volcano Plot MCP Grounding (`run_manhattan_volcano_audit`):** Flag single-SNP chimneys (`< 2` LD flanking SNPs), $\lambda_{	ext{GC}} > 1.15$, or ungrounded loci in EMBL-EBI GWAS Catalog / `open-targets-mcp` (`LR = 0.15`), and volcano plot raw-$p$-as-FDR masquerades (`LR = 0.20`).
4. **Deep Learning Image Splicing & Phase 3 DuckDB SIMD Lean ImageTwin (`image_splicing_dl.py`, `src/vision/`):** Run Branch A (TruFor `Noiseprint++` high-pass residual variance + CAT-Net v2 JPEG ELA) and Branch B (dihedral $D_4$ rotation/flip-invariant DINOv2 + LightGlue clone matching + DuckDB SIMD inter-paper retraction fingerprint index). **Kill-Switch 3.5:** Halt on verified splicing, erasure, or intra-/inter-paper cloning.

### Gate 4: Governance, Spectrum Truncation, Cutoff Validity & Graph Engineering (`graph_engineering.py`)
1. **Gate 4.1 — Spectrum Truncation & Etiological Purging (`run_spectrum_truncation_audit`):** Flag $> 30\%$ screening exclusions that purge primary clinical etiologies or misuse MCAR (`LR = 0.25`).
2. **Gate 4.2 — Population-Phenotype Cutoff & Descriptive Alignment (`run_population_phenotype_cutoff_audit`, `run_descriptive_methods_table_audit`):** Flag mismatched ethnic phenotype cutoffs (`LR = 0.30`) and Methods-to-Table parametric vs. non-parametric contradictions (`LR = 0.25`).
3. **Gate 4.3 — Internal Manuscript Consistency DAG (`audit_manuscript_consistency_dag`):** Verify exact participant and event conservation from CONSORT $	o$ Table 1 $	o$ Table N $	o$ Subgroups (`LR = 0.25`; **Kill-Switch** on CONSORT overflow).
4. **Gate 4.4 — External Bibliometric & Editor-Collusion GNN (`audit_bibliometric_collusion_graph`):** Score handling-editor dominance ($\ge 35\% \implies 	ext{LR} = 0.20$), peer-review turnaround velocity ($< 10	ext{ days} \implies 	ext{LR} = 0.35$), citation cartel reciprocity ($\ge 40\% \implies 	ext{LR} = 0.30$), and co-author retraction contagion ($\ge 25\% \implies 	ext{LR} = 0.30$).

### Gate 4.5: Qualitative & Mixed-Methods Forensics (`qualitative_and_blind_gaps.py` & `qualitativeresearch` MCP)
1. **Gate 4.5A — Qualitative Inter-Rater Reliability (IRR) Granularity (`verify_qualitative_irr_granularity`):** Test whether reported Cohen's $\kappa$, Pabak, and observed percent agreement $P_o$ can mathematically exist for $N$ double-coded transcripts (**Kill-Switch 4.5A** on impossible $(\kappa, P_o, N)$ combinations).
2. **Gate 4.5B — Participant-Quote Pigeonhole & Attribute Contradiction DAG (`audit_qualitative_quote_participant_dag`):** Track every inline quote (`[P14, Male, 68y]`) via `@modelcontextprotocol/server-qualitativeresearch` (`github:tejpalvirk/qualitativeresearch`). Trigger **Kill-Switch 4.5B** if any participant ID exceeds recruited $N$ or changes sex/age/role across quotes; apply `LR = 0.20` if $> 80\%$ of quotes come from $\le 2$ participants ("Frankenstein" GenAI participant-spread bias).
3. **Gate 4.5C — Synthetic LLM Interview Stylometry & COREQ/SRQR/Gupta Audit (`detect_synthetic_qualitative_quotes`):** Flag abnormally uniform utterance-length burstiness ($	ext{CV} < 0.12$) across interviewees or 4-gram voice bleed ($> 25\%$) from author prose (`LR = 0.15`), and grade COREQ (32-item), SRQR (21-item), and Gupta et al. (2026) 8-item AI qualitative audit trail compliance.

## Mandatory Deliverables (`audit_[STUDY_KEY].md`, `tweet_[STUDY_KEY].md`, `pubpeer_[STUDY_KEY].md`)

When auditing a publication for public or post-publication review, generate:
1. `audit_[STUDY_KEY].md`: Complete 6-Gate Forensic Report & Case-Control Calibrated Empirical Bayes Scorecard.
2. `tweet_[STUDY_KEY].md`: Neutral, evidence-grounded metascience thread citing only deterministic mathematical/visual invariants.
3. `pubpeer_[STUDY_KEY].md`: Objective, COPE/PubPeer-compliant comment formatted with exact table coordinates, equations, and R/FastMCP reproduction code.

## Supplementary Resources in This Skill

- `references/gate3_advanced_forensic_sieves.md`: Detailed mathematical formulations for Gates 3.8–3.12 and Gate 4.5 Qualitative Forensics.
- `references/audit_paper_r.md`: Complete 20-function R forensic script (`scripts/audit_paper.R`).
- `references/antigravity_kit.md`: `.agents/mcp_config.json` (wiring `forensic-math-mcp`, `forensic-chart-mcp`, `qualitativeresearch`, `quantitativeresearch`, `datacommons-mcp`, `mcp-analytics`, `open-targets-mcp`, `biomcp`, `rstudio`) and `AGENTS.md`.
- `references/example_42802996_audit.md`: Reference Forensic Audit Packet.


### Gate 3.6: Anatomical Segmentation (`MedSAM` / `SAM 2` / `BiomedParse` / `TotalSegmentator`), DICOM & Cine-Video Forensics (`medsam_dicom_video_forensics.py`)
1. **Mask-to-Table Biometric Conservation (`audit_medsam_mask_to_table_biometrics`):** Segment lesions, organs, lumens, and histological structures via [MedSAM](https://github.com/bowang-lab/medsam), [MedSAM 2](https://huggingface.co/wanglab/MedSAM2/discussions/1/files) ([SAM 2](https://github.com/facebookresearch/sam2)), [BiomedParse](https://github.com/microsoft/BiomedParse), [TotalSegmentator](https://github.com/wasserth/totalsegmentator), and [MONAI](https://github.com/project-monai/monai). Convert pixel masks using scale bars or DICOM `PixelSpacing (0028,0030)` into physical area ($	ext{mm}^2$), RECIST diameter ($	ext{mm}$), or Simpson's volume ($	ext{mL}$) and cross-check against Table 1/2 (`|Z| > 3.5` triggers `LR = 0.15`; **Kill-Switch** on uncalibrated crop-zoom scale-bar manipulation).
2. **3D Organ Topology & DICOM Provenance (`audit_anatomical_topology_and_dicom_provenance`):** Build the organ centroid adjacency graph (`Liver` vs. `Spleen`/`Heart_Apex`) to catch horizontally flipped radiology scans (artificial situs inversus), verify that DICOM `StudyDate` does not precede IRB/NCT registration, check `SliceThickness` against Methods text, and flag duplicate `SeriesInstanceUID` tags across supposedly distinct patients (**Kill-Switch**).
3. **SAM 2 Cine-Video Forensics (`audit_cine_video_sam2_temporal_integrity`):** Track anatomical structures across echocardiography, angiography, and microscopy video frames to catch freeze-frame loops (`duplicate_frame_ratio > 0.25`), temporal splice jump cuts ($Z_{	ext{step}} > 8.0$), and playback speed acceleration ($2	imes$ frame-rate manipulation).

### Gate 5: Unified Multimodal Epistemic Hypergraph (UMEH) & Cellular Sheaf Laplacian (`multimodal_epistemic_hypergraph.py` & `polyglot/`)
1. **Cellular Sheaf Cohomology & Frustration Energy (`compute_cellular_sheaf_laplacian_energy`):** Model all 14 paper & context domains (`Abstract`, `Assumptions`, `Methods`, `Tables`, `Charts`, `Blots/Pictures`, `MedSAM/DICOM Anatomy`, `Cine-Videos`, `Qualitative Quotes`, `References/Recency`, `Author Personal History`, `Retraction/PubPeer History`, `COI/Sponsor/Agencies`, `Conclusion/Relevancy`) as stalks on a Cellular Sheaf $\mathcal{F}$ with restriction maps $\mathcal{F}_{u 	rianglelefteq e}$. Compute global Dirichlet frustration energy $\mathcal{E}_{	ext{Sheaf}}(\mathbf{x}) = \mathbf{x}^T \Delta_{\mathcal{F}} \mathbf{x} = \sum_{e=(u,v)} w_e \|\mathcal{F}_{u 	rianglelefteq e}\mathbf{x}_u - \mathcal{F}_{v 	rianglelefteq e}\mathbf{x}_v\|_2^2$ (**Kill-Switch** if $\mathcal{E}_{	ext{Sheaf}} > 2.50$ or $\ge 3$ cross-modal edges are frustrated).
2. **Narrative Spin, Assumption Falsification, Reference Amnesia & COI/Agenda Coupling (`audit_narrative_to_evidence_spin_and_coi_hypergraph`):**
   - **Abstract/Conclusion Spin:** Flag positive headline claims when the primary table endpoint is null ($p \ge 0.05$, `LR = 0.20`) or when a secondary subgroup is swapped into the conclusion.
   - **Formal Assumption Falsification (`polyglot/smt_z3/`):** Encode statistical/causal assumptions in [Z3 Theorem Prover](https://github.com/z3prover/z3) and penalize when empirical plots/tables violate them (`LR = 0.30` per violated assumption).
   - **Reference Recency ("Selective Amnesia") & Citation Polarity:** Flag 2026 papers with median reference age $> 9	ext{ years}$ and zero recent references or $\ge 2$ omitted recent contradicting RCTs (`LR = 0.25`), contrasting citations misrepresented as supporting (`LR = 0.25`), or zombie retracted citations.
   - **Author Personal History & COI/Agency Agenda Coupling:** Flag hyper-prolific velocity ($\ge 35$ papers/yr) or multi-specialty topic-jumping ($\ge 15$ papers across $\ge 4$ fields/yr, `LR = 0.20`), and trigger `LR = 0.05` (or **Kill-Switch** when paired with zombie retractions) when undeclared COI / sponsor agendas align with narrative spin over a null primary table.
3. **Polyglot High-Performance Execution (`polyglot/`):**
   - **Rust (`polyglot/rust_hypergraph/`):** `petgraph` + `rayon` parallel SIMD Sheaf Laplacian solver.
   - **C++ / SMT-LIB 2.6 (`polyglot/smt_z3/`):** [Z3 Theorem Prover](https://github.com/z3prover/z3) formal satisfiability checker.
   - **Julia (`polyglot/julia_sheaf/`):** [Catlab.jl](https://github.com/AlgebraicJulia/catlab.jl) algebraic sheaf cohomology module.
   - **DuckDB SQL/PGQ (`polyglot/duckdb_pgq/`):** In-process property graph + SIMD vector index.


### Gate 6: Deterministic Agent Lifecycle Hooks (`.agents/hooks.json`) & Adaptive Swarm / `/boost` Router (`swarm_and_boost_router.py`)
1. **Three OS-Level Agent Hooks (`hooks/` & `.agents/hooks.json`):**
   - **`PreToolUse` Hook (`verify_pre_tool_use_hook`):** Intercepts `Write`/`Edit` calls before execution (`exit code 2` hard block). Physically blocks anti-circularity ground-truth leakage or secret exposure in public reports, and blocks writing `audit_[STUDY_KEY].md` or `pubpeer_[STUDY_KEY].md` before deterministic FastMCP tools have executed.
   - **`PostToolUse` Hook (`evaluate_post_tool_sheaf_ratchet`):** Appends each tool's output stalk vector to the session Sheaf ledger and immediately injects a `KILL_SWITCH_HALT` directive when a Tier-1 fatal impossibility fires, short-circuiting downstream VLM/Swarm passes.
   - **`Stop` Hook (`verify_stop_completion_gate`):** Blocks agent completion (`exit code 2`) unless `audit_[STUDY_KEY].md`, `tweet_[STUDY_KEY].md`, and `pubpeer_[STUDY_KEY].md` all exist, Gate 5 Sheaf energy is logged, and any misconduct claim in `pubpeer_[STUDY_KEY].md` is backed by $\ge 1$ Tier-1 Definite Impossibility ($99.20\%$ specificity, $\text{LR}^+ > 50$).
2. **Adaptive 4-Mode Execution Router (`route_execution_mode_swarm_vs_boost`):**
   - **`NO_SWARM_NO_BOOST`:** Default for early Tier-1 Kill-Switches (short-circuited by `PostToolUse`), low-complexity clean papers ($C < 3.5, \mathcal{E}_{\text{Sheaf}} < 0.25$), and routine local 8GB VRAM scans.
   - **`TARGETED_BOOST_ONLY` (Prosecutor $\to$ Defense Counsel $\to$ Z3 Judge):** Triggered sequentially when Sheaf frustration energy is elevated ($\mathcal{E}_{\text{Sheaf}} \ge 0.25$), posterior credibility falls in the $15\%–65\%$ grey zone, or before emitting a public `pubpeer_[STUDY_KEY].md` post (safe on 8GB VRAM because only one role runs at a time).
   - **`PARALLEL_5_AGENT_SWARM` (Cloud Antigravity Only):** Spawns 5 concurrent extraction sub-agents (`Tabular/Assay Math`, `Visual/MedSAM/Video`, `Qualitative/Narrative`, `Provenance/References/COI`, `Sheaf Aggregator`) when multimodal complexity $C \ge 3.5$ on Cloud `gemini-3.8-flash` (disabled on local 8GB VRAM to prevent KV-cache thrashing).
   - **`PARALLEL_5_AGENT_SWARM_PLUS_BOOST`:** Combines parallel 5-agent cloud extraction with adversarial `/boost` verification on high-complexity, high-frustration studies.
