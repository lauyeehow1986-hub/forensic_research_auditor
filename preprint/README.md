# Autonomous Forensic Auditing Pipeline: arXiv Preprint Submission Kit

This directory contains the ready-to-compile LaTeX source code for the scholarly preprint manuscript describing the Autonomous Forensic Research Auditing Pipeline.

---

## 📄 Files Included
- **`main.tex`**: Complete LaTeX manuscript formatted for arXiv submission (`article`, `amsmath`, `hyperref`, `booktabs`).
- **`references.bib`**: BibTeX bibliography including your permanent Zenodo software record (`doi:10.5281/zenodo.23861362`), GitHub repository, and core metascience citations (GRIM, statcheck, Carlisle, SPRITE, PROBAST, RoB 2, Cabanac et al.).

---

## 🎯 Recommended arXiv Subject Classifications
When submitting to [arXiv.org](https://arxiv.org/submit), select from these categories:
1. **Primary:** `stat.AP` (Statistics - Applications) or `stat.ME` (Statistics - Methodology)
2. **Secondary / Cross-list:**
   - `cs.SE` (Computer Science - Software Engineering)
   - `cs.AI` (Computer Science - Artificial Intelligence / Agentic Systems)
   - `q-bio.QM` (Quantitative Biology - Quantitative Methods)

---

## 🚀 How to Submit to arXiv

### Option A: Via Overleaf (Simplest)
1. Zip the `preprint/` directory (`main.tex` and `references.bib`).
2. Go to [Overleaf.com](https://www.overleaf.com) and click **New Project** $\rightarrow$ **Upload Project**.
3. Verify that it compiles cleanly with pdfLaTeX.
4. Click **Submit** $\rightarrow$ **arXiv** to directly transfer or download the compiled `.tar.gz` bundle for arXiv submission.

### Option B: Local Compilation
Using standard TeX Live, MiKTeX, or MacTeX:
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## 🔗 Creating the Bidirectional Citation Loop (Zenodo $\leftrightarrow$ arXiv)

1. **Submit to arXiv:** Submit `main.tex` and `references.bib`. Within 24–48 hours, arXiv will assign an identifier: `arXiv:YYMM.NNNNN`.
2. **Update Zenodo Record:**
   - Go to your Zenodo deposit: `https://doi.org/10.5281/zenodo.23861362`.
   - Click **Edit** (or create a new version `v2.0.1` if deposit is locked).
   - Under **Related works**, add:
     - **Identifier:** `arXiv:YYMM.NNNNN`
     - **Relationship:** `Is supplemented by this upload` or `Is cited by this upload`.
   - Click **Save** and **Publish**.
3. Now, anyone finding the code on GitHub or Zenodo is directed to the arXiv paper, and readers of the arXiv paper can directly access and cite the software DOI!
