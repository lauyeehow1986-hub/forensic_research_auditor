---
name: forensic-research-auditor
description: Audits scientific publications, preprints, clinical trials, DOIs, PMIDs, and PDFs for statistical fabrication (GRIM, statcheck, SPRITE, Benford, 95% CI symmetry/variance compression), GRADE CI imprecision, paper-mill tortured phrases, retraction status, outcome switching, Cochrane RoB 2 methodological bias, universal table consistency, clinical scatterplot density, and Manhattan/volcano plot genomics grounding via MCP. Use whenever the user asks to vet, audit, fact-check, critique, or evaluate a research paper, clinical trial, or study results.
---
# Forensic Research Auditor (Universal Table, 95% CI & Multi-Omics Plot Edition)

A comprehensive metascience and forensic peer-review workflow designed for both Gemini (with NotebookLM integration) and Google Antigravity (`gemini-3.8-flash` with MCP orchestration and RStudio execution). It evaluates scientific studies across a **4-Gate Lexicographic Triage** (fast-fail kill-switches) followed by **Tier 2 Bayesian Likelihood Ratio credibility scoring**, ensuring every table (Table 1 through Table N), every 95% confidence interval (CI), and every clinical/genomic figure (scatterplots, forest plots, Manhattan plots, and volcano plots) is audited for mathematical consistency, external MCP grounding, and clinical relevancy.

## When to Use

- The user asks to audit, vet, fact-check, or evaluate a scientific paper, clinical trial, GWAS/transcriptomics study, preprint, DOI, PMID, arXiv ID, or uploaded study PDF.
- The user wants to check if a paper's results are flawed, p-hacked, underpowered/imprecise (wide 95% CI), variance-compressed (too-narrow 95% CI), over-extrapolated, or fabricated.
- The user wants to generate or run a 4-Gate Forensic Audit packet for their Gemini Notebook (`Forensic Research Auditor`) or Google Antigravity workspace.

## Core Workflow: The 4-Gate Triage & Universal Table/CI/Chart Audit

Execute these steps sequentially. If a study triggers a fatal kill-switch in Gates 1, 2, 3, or 3.5, halt downstream synthesis and issue a **HARD REJECT (0% Credibility / Do Not Cite)** verdict.

### Step 1: Gate 1 - Provenance & Retraction Hygiene (`thinkingLevel: "low"`)

1. Verify the publication's retraction status (`is_retracted`), Expressions of Concern, and post-publication peer-review flags (via OpenAlex, Crossref, PubMed, Zotero, or web search for PubPeer comments).
2. **Kill-Switch 1:** If the paper is retracted, has an unresolved Expression of Concern, or has verified image duplication/cloning on PubPeer, halt immediately and reject.

### Step 2: Gate 2 - Paper-Mill, Tortured Phrases & Reagent Forensics (`thinkingLevel: "medium"`)

1. Scan the manuscript text and Methods section for Problematic Paper Screener (PPS) tortured phrases:
   - `"counterfeit consciousness"` or `"fake brainpower"` (artificial intelligence)
   - `"profound learning"` or `"profound comprehension"` (deep learning)
   - `"irregular backwoods"` (random forest)
   - `"credulous Bayes"` (naive Bayes)
   - `"haze figuring"` or `"vapor processing"` (cloud computing)
   - `"bosom peril"` (breast cancer)
   - `"cruel"` used in place of statistical *mean*, or `"caesarean section"` used in place of *standard deviation*.
2. For wet-lab/biomedical studies, check for verifiable Research Resource Identifiers (`RRID:`), known cross-contaminated/misidentified cell lines (e.g., Chang liver used as normal hepatocytes, HEp-2 used as laryngeal carcinoma instead of HeLa), and PCR primer / shRNA target homology (`Seek & Blastn` / `biomcp`).
3. **Kill-Switch 2:** If `>= 1` tortured phrase or invalidated cell-line/primer reagent is found, halt immediately and reject.

### Step 3: Gate 3 - Universal Mathematical, Table & 95% CI Forensics (`thinkingLevel: "high"`)

Do not restrict statistical checks to Table 1. Audit **every summary, outcome, subgroup, and regression table** (Table 1, Table 2, Table 3+) in the manuscript:

1. **Inline NHST Recalculation (`statcheck` & `academic-stats-mcp`):** Extract all inline test statistics (`t`, `F`, `r`, `chi2`, `Z`, `p`) and verify whether the reported test statistic and degrees of freedom (`df`) yield the reported p-value. Flag any **Decision Error** (claimed `p < .05`, recalculated `p > .05`).
2. **95% Confidence Interval (CI) Symmetry, P-Value Concordance & Width Forensics (`run_ci_consistency_and_width_audit`):**
   - **Symmetry Check:** For linear differences (MD, beta), verify `Estimate == (LL + UL) / 2` (within rounding tolerance). For ratio measures (OR, RR, HR), verify log-scale symmetry: `log(Estimate) == (log(LL) + log(UL)) / 2`.
   - **Implied SE & P-Value Reconstruction:** Compute `SE = (UL - LL) / 3.9199` (or `(log(UL) - log(LL)) / 3.9199` for ratios), `Z = Estimate / SE`, and `p_recalc = 2 * pnorm(-abs(Z))`. Flag a **Primary Decision Error** if claimed `p < 0.05` while the 95% CI crosses the null (`0` for differences, `1.0` for ratios) or `p_recalc > 0.05`.
   - **Too-Narrow 95% CI (Variance Compression / SE-as-SD Misreporting):** Reconstruct the implied sample standard deviation (`SD_implied = SE * sqrt(N)`). If `SD_implied` is `< 25%` of established physiological/clinical reference SD (via `datacommons-mcp` or domain priors), flag as **Implausible Variance Compression or SE-for-CI Mislabeling (`LR = 0.15`)**.
   - **Too-Wide 95% CI (GRADE Imprecision & Low Clinical Relevancy):** Evaluate against Cochrane GRADE Optimal Information Size (OIS) and Minimal Clinically Important Difference (MCID). If the 95% CI spans both clinically appreciable benefit and appreciable harm, or its width exceeds `2 * MCID` with `< 300` dichotomous events (`< 400` continuous N), apply the **Severe 95% CI Imprecision Penalty (`LR = 0.40`)**.
3. **Universal Granularity Audit (`GRIM`, `GRIMMER`, `DEBIT`):** Across all tables reporting integer/discrete data or Likert scales (where sample size `N < 100` for 2 decimal places), test whether `round(round(Mean * N) / N, 2)` matches the reported mean (`GRIM`) and whether binary proportions match their standard deviations (`DEBIT`).
4. **Sample Size (`N`) Continuity & Knowledge Graph Lineage (`quantitativeresearch` MCP):** Cross-check sample sizes and variable definitions from Table 1 through all outcome and subgroup tables. Flag any unexplained sample size shifts or missingness not accounted for in the CONSORT flow diagram.
5. **Carlisle Baseline Table 1 & Macro-Epidemiological Grounding (`datacommons-mcp`):** In RCTs, inspect Table 1 baseline differences across arms for implausible uniformity (`p > 0.9999` hyper-balance) or severe baseline imbalance (`p < 0.0001`). In observational/epidemiological cohorts, cross-check baseline prevalence and incidence rates against `datacommons-mcp` regional statistics.
6. **Multi-Magnitude Numerical Tables (`Benford's Law`) & Raw Data Re-Execution (`mcp-analytics`):** For regression tables, hazard ratios, or large count tables, check first-digit conformity using `benford.analysis`. When supplementary raw data CSVs are provided, execute verification models via `mcp-analytics` or `rstudio-mcp`.
7. **Execution Rule:** In Google Antigravity, run `scripts/audit_paper.R` via `rstudio-mcp` and paste the verbatim R console stdout block into the report. Never perform mental math to fake R console output.
8. **Kill-Switch 3:** Halt and reject if `>= 2` GRIM/DEBIT impossibilities occur, a primary `statcheck` or `95% CI-to-p` Decision Error is found, or `SPRITE` shows impossible scale variance.

### Step 4: Gate 3.5 - Universal Chart, Scatterplot, Manhattan & Volcano Plot Audit (`thinkingLevel: "high"`)

Inspect **every figure, clinical scatterplot, dose-response curve, forest plot, Manhattan plot, and volcano plot** in the manuscript:

1. **Clinical Scatterplot Data Density vs. Claimed Therapeutic Envelope:** Check whether actual data points populate the clinical range claimed in the title, abstract, and conclusions. For example, if a hypertension study claims efficacy across uncontrolled/severe hypertension (e.g., SBP > 160 mm Hg), count how many scatterplot points actually lie above `SBP > 160`.
2. **Outlier-Driven Trends & Subgroup Forest Plots:** Check whether regression lines or interaction p-values in scatterplots are driven by `< 5%` of the sample (or 2-3 extreme outlier points), and whether forest plot subgroup claims rest on tiny, underpowered strata with wide 95% CIs.
3. **Manhattan Plot Forensics & GWAS MCP Grounding (`run_manhattan_volcano_audit` + `gwas-catalog` / `open-targets-mcp`):**
   - **Single-SNP "Chimney" Detection:** Inspect genome-wide significant peaks (`p < 5e-8`, `-log10(p) > 7.301`). Authentic GWAS loci exhibit a linkage disequilibrium (LD) "tower" of correlated flanking SNPs within `+- 500 kb`. Flag solitary single-dot chimneys (`< 2` supporting SNPs with `p < 1e-4` in the locus window) as genotyping artifacts or synthetic point injection.
   - **Threshold & Inflation Audit:** Verify that the significance line is set at `5e-8` (not relaxed to `1e-5` without declaration) and that the genomic inflation factor `lambda_GC` on the Q-Q plot is between `0.95` and `1.10`.
   - **External MCP Grounding:** Query lead rsIDs and traits against **EMBL-EBI GWAS Catalog REST API v2** (`https://www.ebi.ac.uk/gwas/rest/api/v2/`) and **Open Targets Platform MCP** (`open-targets-mcp`). If claimed novel or replicated lead variants have contradictory risk alleles, implausible minor allele frequencies (MAF), or zero colocalization/tractability support despite claiming replication, apply `LR = 0.15` (or halt if rsIDs are nonexistent/fabricated in dbSNP via `biomcp`).
4. **Volcano Plot Forensics & Transcriptomics MCP Grounding (`run_manhattan_volcano_audit` + `open-targets-mcp` / `biomcp`):**
   - **Raw P-Value vs. FDR Y-Axis Masquerade:** Check whether the y-axis plots unadjusted `-log10(raw p)` while the text claims Benjamini-Hochberg `FDR < 0.05` significance.
   - **Fold-Change Noise-Zone Cherry-Picking & Clipping Cliffs:** Verify whether highlighted "hub genes" or "biomarkers" sit inside the low-effect noise corridor (`|log2FC| < 0.585`, i.e., `< 1.5x` fold change) or exhibit artificial vertical/horizontal clipping boundaries.
   - **External MCP Grounding:** Cross-check claimed differentially expressed hub genes against `open-targets-mcp` and `biomcp` for tissue expression specificity and pathway concordance.
5. **Over-Extrapolation & Genomics Artifact Penalty / Kill-Switch:** Apply `LR = 0.20` for clinical scatterplot over-extrapolation (`< 10%` points in claimed range) or volcano-plot FDR/noise-zone misrepresentation, and `LR = 0.15` (or **Kill-Switch 3.5** if rsIDs/loci are fabricated) for Manhattan plot chimney/grounding failures.

### Step 5: Gate 4 - Pre-Registration, Risk of Bias & Bayesian Credibility Scorecard (`thinkingLevel: "high"`)

1. **Pre-Registration & Outcome Switching Check:** Compare the published primary and secondary endpoints (and assessment timepoints) against the timestamped registry record (`NCT` on ClinicalTrials.gov, `OSF`, `ISRCTN`, `PROSPERO`), tracked via `quantitativeresearch` MCP.
2. **Methodological Risk of Bias Grading:** Grade all 5 **Cochrane RoB 2** domains (for RCTs), 7 **ROBINS-I V2** domains (for observational studies), or **AMSTAR 2** domains (for systematic reviews), citing verbatim quotes from the text.
3. **Tier 2 Bayesian Credibility Calculation:**
   - Start with the baseline Field Prior Probability (`P_prior = 0.50` for confirmatory RCT; `0.30` for exploratory clinical/biomedical/psychology study; `0.20` for observational epidemiology or discovery multi-omics).
   - Compute `Prior_Odds = P_prior / (1 - P_prior)`.
   - Multiply by all applicable Likelihood Ratios (`LR_i`):
     - Pre-registered with exact primary endpoint match: `LR = 2.50`
     - Open raw data and reproducible code verified (via `mcp-analytics` / `rstudio-mcp`): `LR = 2.00`
     - Independent supporting replication in `scite.ai` or GWAS Catalog / Open Targets MCP: `LR = 4.00`
     - Primary p-value in `.041 - .049` p-hacking zone: `LR = 0.25`
     - Single isolated non-decision rounding or CI asymmetry typo: `LR = 0.20`
     - Underpowered sample (`< 50%` power for target effect): `LR = 0.35`
     - Severe 95% CI Imprecision (too-wide CI crossing MCID / spanning appreciable benefit & harm, or failing GRADE OIS): `LR = 0.40`
     - Suspiciously narrow 95% CI (`SD_implied < 25%` of reference SD or SE-as-CI misreporting): `LR = 0.15`
     - Unreconciled sample size (`N`) shifts across tables: `LR = 0.30`
     - Scatterplot over-extrapolation / sparse tail density (`< 10%` points in claimed range): `LR = 0.20`
     - Volcano plot unadjusted-p-as-FDR masquerade or noise-zone (`|log2FC| < 0.585`) hub-gene overclaim: `LR = 0.20`
     - Manhattan plot isolated single-SNP chimney (`< 2` LD flanking SNPs), `lambda_GC > 1.15`, or GWAS Catalog / Open Targets contradiction: `LR = 0.15`
     - Baseline Table 1 clinical imbalance or `datacommons-mcp` epidemiological mismatch confounding the outcome: `LR = 0.25`
     - Benford's Law severe anomaly on numerical tables: `LR = 0.10`
     - Cochrane RoB 2 "Some Concerns" (2+ domains): `LR = 0.50`
     - Cochrane RoB 2 "High Risk" (any domain): `LR = 0.15`
     - Undeclared primary outcome switching: `LR = 0.05`
   - Calculate `Posterior_Odds = Prior_Odds * Product(LR_i)` and `Posterior_Probability = Posterior_Odds / (1 + Posterior_Odds)`.
4. **NotebookLM Grounded Sync:** When the user's **Forensic Research Auditor** Gemini Notebook (`notebooks/6b8609aa-fa3d-4a82-a123-5ffe7b4518e1`) is available, cross-check against its sources or export the verified audit packet (`<ID>_gate1to3_verified.md`) into the notebook.

## Required Output Structure

Always present the final audit using these 5 sections:

1. **Executive Integrity Verdict:** (`PASS`, `QUALIFIED PASS`, `SKEPTICAL CAUTION`, or `HARD REJECT - KILL-SWITCH TRIPPED`)
2. **Gate 1 & Gate 2 Provenance & Paper-Mill Summary:** Retraction status, registry ID, and tortured-phrase/reagent screen.
3. **Gate 3 & Gate 3.5 Universal Table, 95% CI & Chart/Genomics Audit:**
   - Inline `statcheck`, `GRIM`/`DEBIT`, and **95% CI Symmetry/Width/Imprecision** results (with verbatim R stdout if executed via RStudio MCP).
   - Table 1 through Table N sample-size continuity, baseline balance, and `datacommons-mcp` population grounding.
   - Clinical scatterplot density (`SBP > 160`, etc.) AND Manhattan/volcano plot audit (`lambda_GC`, LD-tower chimney screen, FDR vs raw-p, and GWAS Catalog / Open Targets MCP grounding).
4. **Gate 4 Outcome Switching & Cochrane RoB 2 Scorecard:** Registry alignment and domain-by-domain risk-of-bias table with verbatim quotes.
5. **Tier 2 Bayesian Credibility Calculation:** Step-by-step table showing Prior Probability, each applied `LR_i` (including 95% CI imprecision/narrow-variance and genomics plot multipliers), final Posterior Credibility Percentage, and GRADE certainty rating.

## Supplementary Resources in This Skill

- `references/audit_paper_r.md`: Complete R forensic script (`statcheck`, `scrutiny::grim_map`, `rsprite2`, `benford.analysis`, Carlisle baseline check, `run_chart_density_audit`, `run_ci_consistency_and_width_audit`, and `run_manhattan_volcano_audit`).
- `references/antigravity_kit.md`: Drop-in `AGENTS.md` Master Prompt for `gemini-3.8-flash` and `.agents/mcp_config.json` with all 10 MCP servers wired up.
- `references/example_42802996_audit.md`: Reference audit packet demonstrating Gate 1-4 evaluation including 95% CI width/consistency and scatterplot density auditing.
