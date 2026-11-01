# Twitter/X Audit Disclosure Thread

**Audited Paper:** The Singapore Heart Failure Risk Score: Prediction of Survival in Southeast Asian Patients  
**Authors:** Jonathan Yap et al. (2019), *Ann Acad Med Singapore* 48(3):86–94  
**DOI:** https://doi.org/10.47102/annals-acadmedsg.V48N3p86  
**PMID:** 30997477  
**Verdict:** SKEPTICAL CAUTION (Posterior Credibility: 17.65%, GRADE Low Certainty)

---

### Tweet 1: Hook & Finding (275 chars)
🚨 Forensic Research Audit:
"The Singapore Heart Failure Risk Score: Prediction of Survival in Southeast Asian Patients" (Ann Acad Med Singap 2019)

⚠️ Verdict: SKEPTICAL CAUTION (17.65% Credibility)
DOI: https://doi.org/10.47102/annals-acadmedsg.V48N3p86

Key metascience findings below 🧵👇

---

### Tweet 2: The Receipts & Mathematical Forensics (272 chars)
🔍 Forensic Receipts:
• Exact HL calibration match: χ²(8)=14.36, p=0.073 (recalc: 0.07285).
• Zero statcheck decision errors across 10 Cox HRs.
• Outperformed global MAGGIC (C=0.731 vs 0.620).
• BUT temporal validation C-index drops to 0.648 (95% CI 0.606-0.690) with +2.5-3.8% survival overprediction.

---

### Tweet 3: Community & Sleuth Routing (228 chars)
Calling paper-mill sleuths, clinical trialists & metascience researchers:
@PubPeer @MicrobiomDigest @gcabanac @NickWise82 @SholtoDavid

#AcademicTwitter #PaperMill #CardioTwitter #HeartFailure #StatisticalIntegrity #OpenScience

---

### Tweet 4: Code & Full Report (243 chars)
💻 Reproduce & audit in your own terminal:
```r
pchisq(14.36, df=8, lower.tail=FALSE) # 0.07285
run_ci_consistency_and_width_audit(0.648, 0.606, 0.690)
```

Full open report & reproducible pipeline:
https://github.com/lauyeehow1986-hub/forensic_audit
