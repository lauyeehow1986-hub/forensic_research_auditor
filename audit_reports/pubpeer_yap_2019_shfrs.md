# PubPeer Submission Brief

**Title:** Methodological and Statistical Inquiries: *The Singapore Heart Failure Risk Score: Prediction of Survival in Southeast Asian Patients*  
**Paper URL / DOI:** [10.47102/annals-acadmedsg.V48N3p86](https://doi.org/10.47102/annals-acadmedsg.V48N3p86)  
**PubMed ID:** [30997477](https://pubmed.ncbi.nlm.nih.gov/30997477/)  
**Authors:** Jonathan Yap, Shaw Yang Chia, Fang Yi Lim, John C Allen, Louis Teo, David Sim, Yun Yun Go, Fazlur Rehman Jaufeerally, Matthew Seow, Bernard Kwok, Reginald Liew, Carolyn SP Lam, Chi Keong Ching  
**Journal:** *Annals of the Academy of Medicine, Singapore* (2019; 48:86–94)  

---

### Methodological Observations & Discussion

We conducted an automated reproducibility and consistency review of this publication using the open-source Antigravity Forensic Research Auditing Suite. We commend the authors for deriving a regional risk calculator tailored to Southeast Asian heart failure cohorts, which demonstrated superior discrimination in the derivation cohort ($C = 0.731$) compared to the international MAGGIC score ($C = 0.620$).

We would appreciate clarification or further context from the authors regarding the following technical and clinical observations:

1. **Temporal Validation Discrimination Attenuation:**
   In Table 3, the 2-year mortality concordance index decreases from $0.726$ [95% CI, 0.697–0.754] in the derivation cohort to $0.681$ [95% CI, 0.640–0.722] in concurrent Validation Cohort 1, and further to **$0.648$ [95% CI, 0.606–0.690]** in temporal Validation Cohort 2 (2013 admissions). Could the authors discuss whether this shrinkage reflects unmeasured temporal changes in medical therapy or baseline comorbidity burden, and how this affects the score's standalone utility for clinical triaging?

2. **Directional Risk Calibration Drift in Older Cohorts:**
   Across both validation cohorts, the model systematically overpredicts survival (underestimates mortality) by $+2.5\%$ to $+3.8\%$ (e.g., in Validation 1, actual 2-year survival was $64.1\%$ vs predicted $67.9\%$). Given that the validation cohorts were slightly older (mean age $71.4$ vs $68.2$ years) with higher hypertension prevalence ($79.1\%$ vs $70.8\%$), is an updated age-recalibrated baseline hazard function planned?

3. **Inclusion of Contemporary Biomarkers:**
   Baseline natriuretic peptides (e.g., NT-proBNP or BNP) and modern guideline-directed medical therapies (GDMT, such as ARNI or SGLT2 inhibitors) were not available during the 2008–2013 registry period. Would incorporating NT-proBNP into the online Duke-NUS risk calculator restore validation discrimination above the $0.70$ threshold?

#### Mathematical Verification Snippet (Base R)
```r
# 1. Exact Hosmer-Lemeshow Goodness-of-Fit Recalculation (Derivation Cohort)
pchisq(14.36, df = 8, lower.tail = FALSE)
# Output: 0.07285143 (Confirms reported p = 0.073)

# 2. Validation Cohort 2 Discrimination 95% CI Symmetry Check
est <- 0.648; ll <- 0.606; ul <- 0.690
midpoint <- (ll + ul) / 2 # 0.648 (Perfect linear symmetry)
se_implied <- (ul - ll) / (2 * qnorm(0.975)) # 0.02143
```

*This brief is submitted in the spirit of scientific transparency, reproducible metascience, and post-publication peer review.*
