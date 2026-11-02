---
name: forensic-research-auditor
description: Audits scientific publications, preprints, clinical trials, DOIs, PMIDs, and PDFs for statistical fabrication (GRIM, statcheck, SPRITE, Benford, 95% CI symmetry/variance compression), diagnostic 2x2 matrices (High Specificity Mirage), bootstrap shrinkage, spectrum truncation, GRADE CI imprecision, paper-mill tortured phrases, retraction status, outcome switching, Cochrane RoB 2 methodological bias, universal table consistency, clinical scatterplot density, and Manhattan/volcano plot genomics grounding via MCP. Use whenever the user asks to vet, audit, fact-check, critique, or evaluate a research paper, clinical trial, or study results.
---
# Forensic Research Auditor (Universal Table, 95% CI & Multi-Omics Plot Edition)

A comprehensive metascience and forensic peer-review workflow designed for both Gemini (with NotebookLM integration) and Google Antigravity (`gemini-3.8-flash` with MCP orchestration and RStudio execution). It evaluates scientific studies across a **4-Gate Lexicographic Triage** (fast-fail kill-switches) followed by **Tier 2 Bayesian Likelihood Ratio credibility scoring**, ensuring every table (Table 1 through Table N), every 95% confidence interval (CI), diagnostic 2x2 contingency matrix, bootstrap resampling protocol, cohort inclusion/exclusion flow, and every clinical/genomic figure (scatterplots, forest plots, Manhattan plots, and volcano plots) is audited for mathematical consistency, external MCP grounding, and clinical relevancy.

## When to Use

- The user asks to audit, vet, fact-check, or evaluate a scientific paper, clinical trial, diagnostic prediction model, GWAS/transcriptomics study, preprint, DOI, PMID, arXiv ID, or uploaded study PDF.
- The user wants to check if a paper's results are flawed, p-hacked, underpowered/imprecise (wide 95% CI), variance-compressed (too-narrow 95% CI), over-extrapolated, diagnostically distorted (High Specificity Mirage), un-shrunk, cohort-purged (spectrum truncation), or fabricated.
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
5. **Carlisle Baseline Table 1 & Macro-Epidemiological Grounding (`datacommons-mcp`):** In RCTs, inspect Table 1 baseline differences across arms for implausible uniformity (`p > 0.9999` hyper-balance) or severe baseline imbalance (`p < 0.0001`). In observational/epidemiological cohorts, refuse the Carlisle uniformity test (as baseline confounding is expected) and cross-check baseline prevalence and incidence rates against `datacommons-mcp` regional statistics.
6. **Multi-Magnitude Numerical Tables (`Benford's Law`) & Raw Data Re-Execution (`mcp-analytics`):** For regression tables, hazard ratios, or large count tables spanning multiple orders of magnitude, check first-digit conformity using `benford.analysis`. Do NOT apply Benford's Law to homeostatically bounded physiological vitals or regression ratios. When supplementary raw data CSVs are provided, execute verification models via `mcp-analytics` or `rstudio-mcp`.
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

### Step 4b: Gate 3.6 - Diagnostic 2x2 Matrix & High Specificity Mirage (`thinkingLevel: "high"`)

When auditing diagnostic tests, biomarkers, AI classifiers, or triage risk scores (`run_diagnostic_2x2_audit`):

1. **Reconstruct Full 2x2 Contingency Matrix:** Reconstruct true positives (TP), false positives (FP), false negatives (FN), and true negatives (TN) from reported sensitivity, specificity, and sample sizes ($N_{cases}, N_{controls}$).
2. **False Negative Rate (FNR) & Negative Likelihood Ratio (LR-):** Compute `FNR = 1 - Sensitivity` and `LR- = (1 - Sensitivity) / Specificity`.
3. **The "High Specificity Mirage" Sieve:** Authors frequently trumpet "impressive 90-95% specificity!" in abstracts to mask a disastrously poor rule-out performance where Sensitivity is `< 50%` (`FNR > 50%`) or `LR- > 0.80`. A negative test result fails to rule out the condition, leaving the majority of diseased patients undetected.
4. **PPV / NPV Discrepancy & Spectrum Distortion:** Compare reported predictive values against reconstructed values based on realistic disease prevalence. Flag cases where authors report optimistic cohort-derived PPV/NPV while concealing extreme positive-to-negative imbalance.
5. **Bayesian Penalty:** Apply `LR = 0.20` if the High Specificity Mirage is detected.

### Step 4c: Gate 3.7 - Bootstrap Resampling & Shrinkage Sieve (`thinkingLevel: "high"`)

When auditing prediction models, multivariable regression models, or clinical risk nomograms (`run_bootstrap_resampling_audit`):

1. **Iteration Sufficiency Sieve:** Check the number of bootstrap resampling iterations $B$. Flag models utilizing $B < 500$ iterations as numerically unstable and under-resampled.
2. **Sample Size vs. Iteration Conflation:** Detect category errors where authors report "we bootstrapped 50% of the sample" or $B = 0.5 \times N$ or "split into 50% new datasets", conflating cross-validation/subsampling proportions with bootstrap repetitions $B$.
3. **Unapplied Shrinkage / Cosmetic Optimism Correction:** Verify whether claimed heuristic shrinkage factors (e.g. $\gamma = \frac{\chi^2 - p}{\chi^2}$ or uniform shrinkage $\approx 0.85$), LASSO penalties, or bootstrap calibration slopes were actually multiplied into deployed beta coefficients. If the published nomogram, scoring formula, or web risk calculator uses unpenalized raw maximum-likelihood betas (`deployed_betas_match_raw == TRUE`), flag the shrinkage claims as cosmetic posturing.
4. **Bayesian Penalty:** Apply `LR = 0.60` if unapplied shrinkage or inadequate resampling ($B < 500$) is detected.

### Step 4d: Gate 3.8 - Cochran Sparse Table & Expected Count Sieve (`thinkingLevel: "high"`)

When auditing categorical baseline tables, adverse events, or subgroup contingency tables (`run_cochran_sparse_table_audit`):

1. **Reconstruct Expected Cell Frequencies:** For any $2 \times 2$ or $r \times c$ table, compute expected counts $E_{ij} = \frac{R_i \times C_j}{N}$.
2. **Cochran's Rule Forensics:** Flag violation if any expected cell count is $< 1$, or if $> 20\%$ of cells have expected counts $< 5$.
3. **Inappropriate Asymptotic Chi-Square Detection:** Compare the reported p-value against recalculations from uncorrected Pearson's $\chi^2$, Yates' continuity-corrected $\chi^2$, and Fisher's exact test. Flag papers that mechanically ran uncorrected Pearson's $\chi^2$ on sparse tables (e.g. rare surgeries, sparse comorbidities like CABG $n=3$) while ignoring software warning flags and failing to apply Fisher's exact test.
4. **Bayesian Penalty:** Apply `LR = 0.20` if uncorrected Pearson $\chi^2$ was run on sparse cells violating Cochran's rule.

### Step 4e: Gate 3.9 - Logit Linearity & Continuous Ratio Skewness Sieve (`thinkingLevel: "high"`)

When auditing continuous hemodynamic, echocardiographic, or biomarker variables in multivariable regression (`run_logit_linearity_and_ratio_audit`):

1. **Linearity on the Logit Scale:** Audit variables entered linearly into logistic or Cox models. Strictly positive, heavy-tailed biological ratios ($E/e'$, albumin-to-creatinine ratio, NT-proBNP, troponin) violate logit linearity ($\ln(\text{odds}) = \beta \cdot X$) because biological effect curves saturate or exhibit steep non-linear risk tiers.
2. **Outlier Leverage Vulnerability:** In right-skewed variables, extreme outliers exert high leverage on maximum likelihood coefficients ($\hat{\beta}$), distorting risk prediction across central clinical ranges.
3. **Non-Linear Alternatives:** Check whether authors tested for non-linearity using Restricted Cubic Splines (RCS, 3–4 knots), applied stabilizing transformations ($\ln(X)$), or utilized established guideline cutoffs (e.g., ASE/EACVI $E/e' > 14$).
4. **Bayesian Penalty:** Apply `LR = 0.35` if skewed continuous ratios are modeled linearly without evaluating non-linearity or outlier leverage.

### Step 5: Gate 4 - Pre-Registration, Risk of Bias & Reporting Drift (`thinkingLevel: "high"`)

1. **Pre-Registration & Outcome Switching Check:** Compare the published primary and secondary endpoints (and assessment timepoints) against the timestamped registry record (`NCT` on ClinicalTrials.gov, `OSF`, `ISRCTN`, `PROSPERO`), tracked via `quantitativeresearch` MCP.
2. **Abstract-to-Text Reporting Drift:** Cross-check effect sizes, p-values, sample sizes, and primary outcome definitions between the Abstract and the Results/Discussion text:
   - Identify outcome demotion where statistically non-significant primary endpoints are softened or replaced in the Abstract by secondary subgroup p-values.
   - Detect selective metric inflation (e.g., reporting relative risk reduction RRR in the Abstract while concealing near-zero absolute risk reduction ARR in the text).
   - If severe reporting drift or outcome demotion spin is identified, apply `LR = 0.40`.
3. **Gate 4.1: Spectrum Truncation & Etiological Purging (`run_spectrum_truncation_audit`):**
   - **Exclusion Rate Forensics:** Calculate the percentage of screened/eligible patients excluded (`exclusion_rate = n_excluded / n_screened`). Flag moderate truncation if $> 30\%$ and severe truncation if $> 50\%$.
   - **Etiological Paradox / Purging:** Check whether authors deliberately excluded the primary real-world etiologies of the target pathology (e.g., excluding ischemic cardiomyopathy or severe valve disease from a heart failure cohort, or excluding prior MI/stents from a CAD biomarker study). Purging real-world etiologies creates an artificial "toy cohort" that inflates C-statistics/AUC while ensuring the model fails in clinical practice.
   - **MCAR Category Errors:** Detect whether authors misused Little's Missing Completely At Random (MCAR) test across patients who were deliberately excluded by protocol/discretion rather than unobserved item fields.
   - **Bayesian Penalty:** Apply `LR = 0.35` for severe spectrum truncation ($> 50\%$) or etiological purging.
4. **Gate 4.2: Population-Phenotype Cutoff & Construct Validity Sieve (`run_population_phenotype_cutoff_audit`):**
   - **Phenotypic Cutoff Concordance:** Verify that diagnostic and anthropometric thresholds match the target population's established epidemiological guidelines.
   - **Paradoxical Western Import:** Flag studies that purport to build an "ethnicity-tailored" or "Asian-specific" model but contradictorily import Western diagnostic thresholds (e.g., using Western $\text{BMI} > 30 \text{ kg/m}^2$ instead of WHO Asian / Singapore MOH $\text{BMI} \ge 27.5 \text{ kg/m}^2$), misclassifying high-risk individuals and severely deflating sensitivity.
   - **Bayesian Penalty:** Apply `LR = 0.25` for paradoxical population-cutoff discordance.
5. **Gate 4.3: Methods-to-Table Descriptive & Non-Parametric Sieve (`run_descriptive_methods_table_audit`):**
   - **Boilerplate Text Discrepancy:** Detect contradictions between the Methods text (e.g. claiming "mean ± SD and Student's t-test") and published tables (presenting exclusively Medians and IQRs).
   - **Inappropriate Parametric Testing on Skewed Variables:** Flag risk of running parametric $t$-tests or ANOVA on heavily skewed clinical markers (NT-proBNP, creatinine, ratios), or failing to report the actual non-parametric tests applied.
   - **Bayesian Penalty:** Apply `LR = 0.40` for descriptive mismatch and unverified parametric testing.
6. **Methodological Risk of Bias Grading:** Grade all 5 **Cochrane RoB 2** domains (for RCTs), 7 **ROBINS-I V2** domains (for observational studies), **PROBAST** (for prediction models), or **AMSTAR 2** domains (for systematic reviews), citing verbatim quotes from the text.
7. **Tier 2 Bayesian Credibility Calculation:**
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
     - High Specificity Mirage (FNR > 50% or LR- > 0.80 disguised by high specificity): `LR = 0.20`
     - Inappropriate uncorrected Pearson chi-square on sparse cells violating Cochran's rule: `LR = 0.20`
     - Paradoxical population-cutoff discordance (e.g. Western BMI > 30 on Asian cohort): `LR = 0.25`
     - Severe Spectrum Truncation (> 50% excluded or primary etiology purged): `LR = 0.35`
     - Unverified logit linearity / outlier leverage on continuous skewed ratios (e.g. linear E/e'): `LR = 0.35`
     - Methods-to-table descriptive mismatch + parametric testing on skewed variables: `LR = 0.40`
     - Unapplied Shrinkage / Inadequate Resampling ($B < 500$): `LR = 0.60`
     - Abstract-to-Text Reporting Drift / Primary Outcome Demotion Spin: `LR = 0.40`
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
6. **NotebookLM Grounded Sync:** When the user's **Forensic Research Auditor** Gemini Notebook (`notebooks/6b8609aa-fa3d-4a82-a123-5ffe7b4518e1`) is available, cross-check against its sources or export the verified audit packet (`<ID>_gate1to3_verified.md`) into the notebook.

## Required Output Structure & Mandatory Deliverables (.md)

Every forensic audit must automatically generate and write three persistent output files to `./audit_reports/` (creating `./audit_reports/` if not present), alongside delivering the final 5-section consensus directly in chat with clickable file links:

1. **`./audit_reports/audit_[STUDY_KEY].md`**: The complete 5-section consensus audit report.
2. **`./audit_reports/tweet_[STUDY_KEY].md`**: A ready-to-publish 4-tweet Twitter/X disclosure thread containing the hook, deterministic mathematical receipts, sleuth community routing (`@PubPeer`, `@MicrobiomDigest`, `@gcabanac`, `@NickWise82`, `@SholtoDavid`), hashtags (`#AcademicTwitter`, `#PaperMill`, `#ProblematicPaperScreener`, `#ScientificIntegrity`), and GitHub reproduction links.
3. **`./audit_reports/pubpeer_[STUDY_KEY].md`**: A strictly objective, neutral comment formatted for 1-click submission to PubPeer, adhering to PubPeer's moderation policy (zero accusatory language, focusing purely on numerical discrepancies and reproducible verification snippets).

Always format the deliverable using these 5 sections:

1. **Executive Integrity Verdict:** (`PASS`, `QUALIFIED PASS`, `SKEPTICAL CAUTION`, or `HARD REJECT - KILL-SWITCH TRIPPED`)
2. **Gate 1 & Gate 2 Provenance & Paper-Mill Summary:** Retraction status, registry ID, and tortured-phrase/reagent screen.
3. **Gate 3, Gate 3.5, Gate 3.6, Gate 3.7, Gate 3.8 & Gate 3.9 Universal Table, 95% CI & Diagnostic/Resampling Audit:**
   - Inline `statcheck`, `GRIM`/`DEBIT`, and **95% CI Symmetry/Width/Imprecision** results (with verbatim R stdout if executed via RStudio MCP or exact recalculated p-values).
   - Diagnostic 2x2 contingency matrix, False Negative Rate, Negative Likelihood Ratio, and High Specificity Mirage audit (`run_diagnostic_2x2_audit`).
   - Bootstrap iteration sufficiency ($B \ge 500$), sample size conflation, and deployed shrinkage verification (`run_bootstrap_resampling_audit`).
   - Cochran's rule and sparse contingency table expected frequencies audit (`run_cochran_sparse_table_audit`).
   - Continuous ratio logit linearity and outlier leverage audit (`run_logit_linearity_and_ratio_audit`).
   - Table 1 through Table N sample-size continuity, baseline balance, and macro-epidemiological population grounding.
   - Clinical scatterplot density (`SBP > 160`, etc.) AND Manhattan/volcano plot audit (`lambda_GC`, LD-tower chimney screen, FDR vs raw-p, and GWAS Catalog / Open Targets MCP grounding).
4. **Gate 4 Outcome Switching, Methodological Risk of Bias & Population Validity Scorecard:**
   - Registry alignment, abstract-to-text reporting drift, and domain-by-domain risk-of-bias table (Cochrane RoB 2 for RCTs, PROBAST for prediction models, ROBINS-I for observational cohorts) with verbatim quotes.
   - Spectrum truncation and etiological purging audit (`run_spectrum_truncation_audit`).
   - Population-phenotype cutoff and construct validity audit (`run_population_phenotype_cutoff_audit`).
   - Methods-to-table descriptive discrepancy and non-parametric audit (`run_descriptive_methods_table_audit`).
5. **Tier 2 Bayesian Credibility Calculation:** Step-by-step table showing Prior Probability, each applied `LR_i` (including 95% CI imprecision/narrow-variance, High Specificity Mirage, unapplied shrinkage, Cochran violation, population cutoff discordance, logit linearity violation, descriptive mismatch, and genomics plot multipliers), final Posterior Credibility Percentage, and GRADE certainty rating.

## Supplementary Resources in This Skill

- `references/audit_paper_r.md`: Complete R forensic script (`statcheck`, `scrutiny::grim_map`, `rsprite2`, `benford.analysis`, Carlisle baseline check, `run_chart_density_audit`, `run_ci_consistency_and_width_audit`, `run_manhattan_volcano_audit`, `run_diagnostic_2x2_audit`, `run_bootstrap_resampling_audit`, `run_spectrum_truncation_audit`, `run_cochran_sparse_table_audit`, `run_logit_linearity_and_ratio_audit`, `run_population_phenotype_cutoff_audit`, and `run_descriptive_methods_table_audit`).
- `references/antigravity_kit.md`: Drop-in `AGENTS.md` Master Prompt for `gemini-3.8-flash` and `.agents/mcp_config.json` with all 10 MCP servers wired up.
- `references/example_42802996_audit.md`: Reference audit packet demonstrating Gate 1-4 evaluation including 95% CI width/consistency and scatterplot density auditing.
