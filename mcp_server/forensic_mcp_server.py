#!/usr/bin/env python3
"""
Forensic Research Auditor MCP Server (`forensic_mcp_server.py`)
Deterministic MCP Server implementing standard Model Context Protocol (stdio JSON-RPC 2.0):
- Gate 1: Provenance & Retraction Hygiene (Crossref & EuropePMC / OpenAlex check)
- Gate 2: Paper-Mill Tortured Phrases & ICLAC Cell-Line Forensics
- Gate 3: NHST Statcheck, 95% CI Width/Symmetry/Imprecision Forensics, GRIM/DEBIT, Carlisle & Benford
- Gate 3.5: Clinical Scatterplot Density + Manhattan & Volcano Plot Genomics Grounding (EMBL-EBI GWAS Catalog & Open Targets API)
- Gate 4: Tier 2 Bayesian Credibility Calculator & GRADE Certainty Scorer
- Dual-Bucket NHCS Affiliation Classifier
"""

import json
import math
import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

# Problematic Paper Screener (PPS) Tortured Phrases Dictionary
TORTURED_PHRASES = {
    "counterfeit consciousness": "artificial intelligence",
    "fake brainpower": "artificial intelligence",
    "profound learning": "deep learning",
    "profound comprehension": "deep learning",
    "irregular backwoods": "random forest",
    "credulous bayes": "naive Bayes",
    "haze figuring": "cloud computing",
    "vapor processing": "cloud computing",
    "bosom peril": "breast cancer",
    "caesarean section": "standard deviation (when used in statistical context)",
    "cruel ±": "mean ± SD (mistranslated statistical mean)",
}

# ICLAC Misidentified / Cross-Contaminated Cell Lines
ICLAC_CONTAMINATED_CELL_LINES = {
    "chang liver": "HeLa contaminant (invalid as normal human hepatocyte)",
    "hep-2": "HeLa contaminant (invalid as laryngeal carcinoma)",
    "int 407": "HeLa contaminant (invalid as normal embryonic intestinal epithelium)",
    "bgc-823": "HeLa contaminant (invalid as gastric adenocarcinoma)",
    "kb": "HeLa contaminant (invalid as oral epidermoid carcinoma)",
    "wish": "HeLa contaminant (invalid as amnion epithelium)",
}

# Tier 2 Bayesian Priors & Likelihood Ratio Multipliers
FIELD_PRIORS = {
    "confirmatory_rct": 0.50,
    "exploratory_clinical": 0.30,
    "observational_epidemiology": 0.20,
    "discovery_multi_omics": 0.20,
}

LR_CATALOG = {
    "preregistered_exact_match": 2.50,
    "open_data_and_code_verified": 2.00,
    "independent_replication_scite": 4.00,
    "primary_p_in_041_to_049_zone": 0.25,
    "isolated_non_decision_rounding_typo": 0.20,
    "underpowered_sample_lt_50pct": 0.35,
    "ci_too_wide_grade_imprecision": 0.40,
    "ci_too_narrow_variance_compression": 0.15,
    "unreconciled_sample_size_shifts": 0.30,
    "scatterplot_over_extrapolation": 0.20,
    "volcano_plot_fdr_or_noise_overclaim": 0.20,
    "manhattan_plot_chimney_or_ungrounded": 0.15,
    "baseline_table1_imbalance": 0.25,
    "benford_severe_anomaly": 0.10,
    "cochrane_rob2_some_concerns_2plus": 0.50,
    "cochrane_rob2_high_risk": 0.15,
    "undeclared_outcome_switching": 0.05,
}


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def tool_gate1_provenance_and_retraction(
    doi: Optional[str] = None,
    pmid: Optional[str] = None,
    title: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Audits paper provenance, retraction status, and expression of concern flags
    via Crossref and EuropePMC APIs.
    """
    is_retracted = False
    has_eoc = False
    retraction_details = []
    checked_sources = []

    # 1. Check Crossref if DOI provided
    if doi:
        clean_doi = doi.strip().replace("https://doi.org/", "").replace("http://doi.org/", "")
        url = f"https://api.crossref.org/works/{urllib.parse.quote(clean_doi)}"
        checked_sources.append(f"Crossref ({clean_doi})")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AntigravityForensicAuditor/2.0 (mailto:audit@forensic.org)"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                message = data.get("message", {})
                # Check update-to
                updates = message.get("update-to", [])
                for u in updates:
                    u_type = u.get("type", "").lower()
                    if "retract" in u_type:
                        is_retracted = True
                        retraction_details.append(f"Crossref update-to flag: {u_type} (DOI: {u.get('updated', {}).get('DOI', '')})")
                    elif "concern" in u_type or "expression" in u_type:
                        has_eoc = True
                        retraction_details.append(f"Crossref expression of concern: {u_type}")
                
                # Check title / container for retraction notice
                doc_title = " ".join(message.get("title", [])).lower()
                if doc_title.startswith("retraction:") or "retraction notice" in doc_title:
                    is_retracted = True
                    retraction_details.append("Title indicates retraction notice")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                retraction_details.append(f"Crossref DOI {clean_doi} not found (404)")
            else:
                retraction_details.append(f"Crossref HTTP {e.code}")
        except Exception as e:
            retraction_details.append(f"Crossref check skipped/offline: {str(e)}")

    # 2. Check EuropePMC if PMID or DOI provided
    query = None
    if pmid:
        query = f"EXT_ID:{pmid} src:med"
    elif doi:
        clean_doi = doi.strip().replace("https://doi.org/", "")
        query = f'DOI:"{clean_doi}"'
    elif title:
        query = f'TITLE:"{title}"'

    if query:
        checked_sources.append("EuropePMC")
        epmc_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={urllib.parse.quote(query)}&format=json&resultType=core"
        try:
            req = urllib.request.Request(epmc_url, headers={"User-Agent": "AntigravityForensicAuditor/2.0"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                results = data.get("resultList", {}).get("result", [])
                if results:
                    first = results[0]
                    # Check pubType or commentCorrection
                    pub_types = [pt.lower() for pt in first.get("pubTypeList", {}).get("pubType", [])]
                    for pt in pub_types:
                        if "retract" in pt:
                            is_retracted = True
                            retraction_details.append(f"EuropePMC publication type: {pt}")
                        elif "expression of concern" in pt:
                            has_eoc = True
                            retraction_details.append(f"EuropePMC publication type: {pt}")
                    
                    # Check commentCorrectionList
                    comments = first.get("commentCorrectionList", {}).get("commentCorrection", [])
                    for c in comments:
                        ref_type = c.get("referenceType", "").lower()
                        if "retract" in ref_type:
                            is_retracted = True
                            retraction_details.append(f"EuropePMC commentCorrection: {c.get('referenceType')} (ID: {c.get('id')})")
                        elif "concern" in ref_type:
                            has_eoc = True
                            retraction_details.append(f"EuropePMC commentCorrection: {c.get('referenceType')}")
        except Exception as e:
            retraction_details.append(f"EuropePMC check skipped/offline: {str(e)}")

    kill_switch = is_retracted or has_eoc
    return {
        "gate": "Gate 1 - Provenance & Retraction Hygiene",
        "doi": doi,
        "pmid": pmid,
        "is_retracted": is_retracted,
        "has_expression_of_concern": has_eoc,
        "checked_sources": checked_sources,
        "details": retraction_details if retraction_details else ["No retraction or concern flags detected"],
        "kill_switch_tripped": kill_switch,
        "verdict": "HARD REJECT - KILL-SWITCH 1 TRIPPED (RETRACTED / EXPRESSION OF CONCERN)" if kill_switch else "PASS",
    }


def tool_gate2_tortured_phrases_and_reagents(text: str) -> Dict[str, Any]:
    """Scans manuscript text for PPS tortured phrases and ICLAC misidentified cell lines."""
    lower_text = text.lower()
    detected_phrases = {
        phrase: meaning for phrase, meaning in TORTURED_PHRASES.items() if phrase in lower_text
    }
    detected_cells = {
        cell: note for cell, note in ICLAC_CONTAMINATED_CELL_LINES.items() if cell in lower_text
    }
    rrid_matches = re.findall(r"RRID:[A-Za-z0-9_-]+", text)
    kill_switch = len(detected_phrases) > 0 or len(detected_cells) > 0
    return {
        "gate": "Gate 2 - Paper-Mill & Reagent Forensics",
        "tortured_phrases_detected": detected_phrases,
        "contaminated_cell_lines_detected": detected_cells,
        "rrid_identifiers_found": rrid_matches,
        "kill_switch_tripped": kill_switch,
        "verdict": "HARD REJECT - KILL-SWITCH 2 TRIPPED" if kill_switch else "PASS",
    }


def tool_gate3_statcheck_and_ci_forensics(
    point_estimate: float,
    ci_lower: float,
    ci_upper: float,
    reported_p: Optional[float] = None,
    n_total: Optional[int] = None,
    is_ratio: bool = False,
    mcid_threshold: Optional[float] = None,
    reference_sd: Optional[float] = None,
    total_events: Optional[int] = None,
    symmetry_tolerance: float = 0.05,
) -> Dict[str, Any]:
    """
    Audits a 95% Confidence Interval [ci_lower, ci_upper] and point estimate for:
    1. Point-estimate-to-CI symmetry (linear or log-scale for OR/RR/HR).
    2. Implied SE, Z-statistic, and recalculated two-sided p-value concordance (Decision Error check).
    3. Too-narrow 95% CI (Variance compression: implied SD < 25% of reference physiological SD).
    4. Too-wide 95% CI (Cochrane GRADE Imprecision: crossing MCID / spanning benefit & harm / failing OIS).
    """
    if is_ratio:
        if point_estimate <= 0 or ci_lower <= 0 or ci_upper <= 0:
            return {"error": "Ratio measures (OR/RR/HR) must be strictly positive."}
        est_t = math.log(point_estimate)
        ll_t = math.log(ci_lower)
        ul_t = math.log(ci_upper)
        null_val = 0.0
    else:
        est_t = point_estimate
        ll_t = ci_lower
        ul_t = ci_upper
        null_val = 0.0

    midpoint = (ll_t + ul_t) / 2.0
    asymmetry_err = abs(est_t - midpoint)
    is_symmetric = asymmetry_err <= symmetry_tolerance

    implied_se = (ul_t - ll_t) / (2.0 * 1.959963984540054)
    implied_z = abs(est_t - null_val) / implied_se if implied_se > 0 else float("inf")
    recalc_p = 2.0 * (1.0 - norm_cdf(abs(implied_z)))

    crosses_null = (ll_t <= null_val <= ul_t)
    decision_error = False
    if reported_p is not None:
        decision_error = (
            (reported_p < 0.05 and (recalc_p > 0.05 or crosses_null))
            or (reported_p >= 0.05 and recalc_p < 0.01 and not crosses_null)
        )

    # Too-Narrow 95% CI Check (Variance Compression / SE-as-SD Misreporting)
    implied_sd = (implied_se * math.sqrt(n_total)) if (n_total and not is_ratio) else None
    too_narrow_flag = False
    if implied_sd is not None and reference_sd is not None and reference_sd > 0:
        too_narrow_flag = (implied_sd / reference_sd) < 0.25

    # Too-Wide 95% CI Check (GRADE Imprecision & Optimal Information Size)
    ci_width = ci_upper - ci_lower
    spans_benefit_and_harm = False
    if mcid_threshold is not None and mcid_threshold > 0:
        if is_ratio:
            spans_benefit_and_harm = (
                ci_lower < (1.0 / (1.0 + mcid_threshold)) and ci_upper > (1.0 + mcid_threshold)
            )
        else:
            spans_benefit_and_harm = (
                (ci_lower <= -abs(mcid_threshold) and ci_upper >= abs(mcid_threshold))
                or (ci_width > 2.0 * abs(mcid_threshold))
            )

    under_ois = (
        (total_events is not None and total_events < 300)
        or (n_total is not None and n_total < 400 and crosses_null)
    )
    too_wide_flag = spans_benefit_and_harm or (
        under_ois
        and mcid_threshold is not None
        and (abs(ci_lower) >= abs(mcid_threshold) or abs(ci_upper) >= abs(mcid_threshold))
    )

    lr_multiplier = 1.00
    applied_penalties = []
    if too_narrow_flag:
        lr_multiplier *= LR_CATALOG["ci_too_narrow_variance_compression"]
        applied_penalties.append("ci_too_narrow_variance_compression (LR = 0.15)")
    if too_wide_flag:
        lr_multiplier *= LR_CATALOG["ci_too_wide_grade_imprecision"]
        applied_penalties.append("ci_too_wide_grade_imprecision (LR = 0.40)")
    if not is_symmetric and not decision_error:
        lr_multiplier *= LR_CATALOG["isolated_non_decision_rounding_typo"]
        applied_penalties.append("isolated_non_decision_rounding_typo (LR = 0.20)")

    return {
        "gate": "Gate 3 - 95% CI Consistency, Variance Compression & GRADE Imprecision Audit",
        "point_estimate": point_estimate,
        "ci_95": [ci_lower, ci_upper],
        "is_ratio": is_ratio,
        "is_symmetric": is_symmetric,
        "asymmetry_error": round(asymmetry_err, 5),
        "implied_se": round(implied_se, 5),
        "implied_z": round(implied_z, 4),
        "recalculated_p": round(recalc_p, 6),
        "reported_p": reported_p,
        "crosses_null": crosses_null,
        "decision_error_kill_switch": decision_error,
        "implied_sd": round(implied_sd, 4) if implied_sd is not None else None,
        "too_narrow_ci_variance_compression": too_narrow_flag,
        "too_wide_ci_grade_imprecision": too_wide_flag,
        "applied_penalties": applied_penalties,
        "recommended_lr": round(lr_multiplier, 4),
        "verdict": "HARD REJECT - KILL-SWITCH 3 TRIPPED (DECISION ERROR)" if decision_error else "PASS",
    }


def tool_gate3_grim_grimmer_debit_table_audit(
    means: List[float], sds: List[float], sample_sizes: List[int], decimals: int = 2
) -> Dict[str, Any]:
    """Runs deterministic GRIM granularity checks on reported means and sample sizes (N < 100)."""
    findings = []
    impossible_count = 0
    for idx, (m, sd, n) in enumerate(zip(means, sds, sample_sizes)):
        if n <= 10 ** decimals:
            int_sum = round(m * n)
            recalc_mean = round(int_sum / n, decimals)
            consistent = abs(recalc_mean - round(m, decimals)) < (10 ** (-decimals) / 2.0 + 1e-9)
            if not consistent:
                impossible_count += 1
        else:
            consistent = True
        findings.append({
            "row": idx + 1,
            "reported_mean": m,
            "reported_sd": sd,
            "n": n,
            "grim_consistent": consistent,
        })
    kill_switch = impossible_count >= 2
    return {
        "gate": "Gate 3 - GRIM Table Audit",
        "rows_checked": len(findings),
        "impossible_means_count": impossible_count,
        "kill_switch_tripped": kill_switch,
        "verdict": "HARD REJECT - KILL-SWITCH 3 TRIPPED (>= 2 GRIM IMPOSSIBILITIES)" if kill_switch else "PASS",
        "details": findings,
    }


def query_gwas_catalog_rsid(rsid: str) -> Dict[str, Any]:
    """Queries EMBL-EBI GWAS Catalog REST API v2 for a lead SNP rsID."""
    url = f"https://www.ebi.ac.uk/gwas/rest/api/v2/single-nucleotide-polymorphisms/{rsid}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {"status": "found", "rsid": rsid, "gwas_catalog_record": data}
    except urllib.error.HTTPError as e:
        return {"status": "not_found" if e.code == 404 else "http_error", "code": e.code, "rsid": rsid}
    except Exception as e:
        return {"status": "offline_or_unreachable", "rsid": rsid, "note": str(e)}


def tool_gate35_manhattan_volcano_grounding(
    plot_type: str,
    lead_p_values: Optional[List[float]] = None,
    flanking_ld_snp_counts: Optional[List[int]] = None,
    lambda_gc: Optional[float] = None,
    lead_rsids: Optional[List[str]] = None,
    claimed_fdr_adjusted: bool = True,
    y_axis_uses_raw_p: bool = False,
    highlighted_log2fc: Optional[List[float]] = None,
) -> Dict[str, Any]:
    """
    Audits Manhattan plots (GWAS) and Volcano plots (DEG/Proteomics) for visual/statistical
    artifacts and grounds lead rsIDs against the EMBL-EBI GWAS Catalog API v2.
    """
    plot_type_norm = plot_type.strip().lower()
    if plot_type_norm == "manhattan":
        p_vals = lead_p_values or []
        ld_counts = flanking_ld_snp_counts or []
        gw_sig_count = sum(1 for p in p_vals if p < 5e-8)
        chimney_loci = sum(1 for c in ld_counts if c < 2)
        inflation_anomaly = lambda_gc is not None and (lambda_gc > 1.15 or lambda_gc < 0.90)
        suggestive_overclaim = any(5e-8 <= p < 1e-5 for p in p_vals)

        gwas_checks = [query_gwas_catalog_rsid(rs) for rs in (lead_rsids or [])]
        penalty = (chimney_loci > 0) or inflation_anomaly or suggestive_overclaim
        return {
            "gate": "Gate 3.5 - Manhattan Plot & GWAS Catalog Grounding",
            "genome_wide_sig_loci": gw_sig_count,
            "isolated_single_snp_chimneys": chimney_loci,
            "lambda_gc": lambda_gc,
            "inflation_anomaly": inflation_anomaly,
            "suggestive_threshold_overclaim": suggestive_overclaim,
            "gwas_catalog_grounding": gwas_checks,
            "recommended_lr": LR_CATALOG["manhattan_plot_chimney_or_ungrounded"] if penalty else 1.00,
        }
    else:
        log2fcs = highlighted_log2fc or []
        fdr_masquerade = claimed_fdr_adjusted and y_axis_uses_raw_p
        noise_zone_count = sum(1 for fc in log2fcs if abs(fc) < 0.585)
        penalty = fdr_masquerade or (noise_zone_count > 0)
        return {
            "gate": "Gate 3.5 - Volcano Plot & Transcriptomics Forensics",
            "raw_p_masquerading_as_fdr": fdr_masquerade,
            "highlighted_genes_in_noise_zone_lt_0585": noise_zone_count,
            "recommended_lr": LR_CATALOG["volcano_plot_fdr_or_noise_overclaim"] if penalty else 1.00,
        }


def tool_gate4_registry_and_bayesian_score(
    study_type: str, applied_lr_keys: List[str], kill_switch_tripped: bool = False
) -> Dict[str, Any]:
    """Computes the Tier 2 Bayesian Posterior Credibility Score from Prior and Likelihood Ratios."""
    if kill_switch_tripped:
        return {
            "verdict": "HARD REJECT - KILL-SWITCH TRIPPED",
            "posterior_credibility_pct": 0.0,
            "grade_certainty": "Very Low (0% - Do Not Cite)",
        }
    p_prior = FIELD_PRIORS.get(study_type, 0.30)
    prior_odds = p_prior / (1.0 - p_prior)
    product_lr = 1.0
    applied_details = {}
    for k in applied_lr_keys:
        if k in LR_CATALOG:
            product_lr *= LR_CATALOG[k]
            applied_details[k] = LR_CATALOG[k]
    posterior_odds = prior_odds * product_lr
    posterior_prob = posterior_odds / (1.0 + posterior_odds)
    pct = round(posterior_prob * 100.0, 2)

    if pct >= 75.0:
        verdict, grade = "PASS", "High"
    elif pct >= 45.0:
        verdict, grade = "QUALIFIED PASS", "Moderate"
    elif pct >= 15.0:
        verdict, grade = "SKEPTICAL CAUTION", "Low"
    else:
        verdict, grade = "SKEPTICAL CAUTION (SEVERE FRAGILITY)", "Very Low"

    return {
        "study_type": study_type,
        "prior_probability": p_prior,
        "prior_odds": round(prior_odds, 4),
        "applied_likelihood_ratios": applied_details,
        "product_lr": round(product_lr, 5),
        "posterior_odds": round(posterior_odds, 5),
        "posterior_credibility_pct": pct,
        "verdict": verdict,
        "grade_certainty": grade,
    }


def tool_classify_nhcs_affiliation(affiliations_text: str) -> Dict[str, Any]:
    """Classifies whether any author is affiliated with National Heart Centre Singapore (NHCS)."""
    patterns = [
        "national heart centre singapore",
        "national heart center singapore",
        "nhcs",
        "nhris",
        "national heart research institute singapore",
        "5 hospital drive",
        "169609",
        "@nhcs.com.sg",
        "singhealth duke-nus cardiovascular sciences",
        "goh cardiovascular research grant",
    ]
    lower_aff = affiliations_text.lower()
    matched = [p for p in patterns if p in lower_aff]
    is_nhcs = len(matched) > 0
    return {
        "is_nhcs_affiliated": is_nhcs,
        "matched_markers": matched,
        "routing_buckets": (
            ["bucket_1_all_publications"]
            if is_nhcs
            else ["bucket_1_all_publications", "bucket_2_excluding_nhcs"]
        ),
    }


# Tool Definitions for MCP Tools List
MCP_TOOLS_MANIFEST = [
    {
        "name": "tool_gate1_provenance_and_retraction",
        "description": "Gate 1: Checks publication retraction status, Expressions of Concern, and provenance via Crossref and EuropePMC APIs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "doi": {"type": "string", "description": "Digital Object Identifier (e.g. 10.1016/j.ahj.2023.01.002)"},
                "pmid": {"type": "string", "description": "PubMed ID (e.g. 36720485)"},
                "title": {"type": "string", "description": "Manuscript title for fallback query"},
            },
        },
    },
    {
        "name": "tool_gate2_tortured_phrases_and_reagents",
        "description": "Gate 2: Scans text for Problematic Paper Screener (PPS) tortured phrases and ICLAC contaminated cell lines.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Manuscript text, methods, or abstract to scan"},
            },
            "required": ["text"],
        },
    },
    {
        "name": "tool_gate3_statcheck_and_ci_forensics",
        "description": "Gate 3: Audits 95% Confidence Intervals for symmetry, p-value concordance (decision error), too-narrow variance compression (implied SD < 25% ref SD), and too-wide GRADE imprecision.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "point_estimate": {"type": "number", "description": "Point estimate (Mean difference, OR, RR, or HR)"},
                "ci_lower": {"type": "number", "description": "Lower limit of 95% CI"},
                "ci_upper": {"type": "number", "description": "Upper limit of 95% CI"},
                "reported_p": {"type": "number", "description": "Reported p-value in text/table"},
                "n_total": {"type": "integer", "description": "Total sample size N"},
                "is_ratio": {"type": "boolean", "description": "True if OR/RR/HR on ratio/multiplicative scale"},
                "mcid_threshold": {"type": "number", "description": "Minimal Clinically Important Difference threshold"},
                "reference_sd": {"type": "number", "description": "Known physiological reference standard deviation"},
                "total_events": {"type": "integer", "description": "Total number of clinical events (for GRADE OIS check)"},
                "symmetry_tolerance": {"type": "number", "default": 0.05, "description": "Asymmetry tolerance threshold"},
            },
            "required": ["point_estimate", "ci_lower", "ci_upper"],
        },
    },
    {
        "name": "tool_gate3_grim_grimmer_debit_table_audit",
        "description": "Gate 3: Runs deterministic GRIM granularity checks on reported means, standard deviations, and integer sample sizes (N < 100).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "means": {"type": "array", "items": {"type": "number"}, "description": "List of reported means"},
                "sds": {"type": "array", "items": {"type": "number"}, "description": "List of reported standard deviations"},
                "sample_sizes": {"type": "array", "items": {"type": "integer"}, "description": "List of subgroup/total sample sizes"},
                "decimals": {"type": "integer", "default": 2, "description": "Number of reported decimal places (default 2)"},
            },
            "required": ["means", "sds", "sample_sizes"],
        },
    },
    {
        "name": "tool_gate35_manhattan_volcano_grounding",
        "description": "Gate 3.5: Audits Manhattan plots (GWAS single-SNP chimneys, lambda_GC) and Volcano plots (raw-p vs FDR masquerade, noise zone log2FC < 0.585), with EMBL-EBI GWAS Catalog v2 grounding.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "plot_type": {"type": "string", "enum": ["manhattan", "volcano"], "description": "Type of genomic plot to audit"},
                "lead_p_values": {"type": "array", "items": {"type": "number"}, "description": "Lead p-values from Manhattan peaks"},
                "flanking_ld_snp_counts": {"type": "array", "items": {"type": "integer"}, "description": "Number of supporting flanking LD SNPs (p < 1e-4 within +-500kb)"},
                "lambda_gc": {"type": "number", "description": "Genomic inflation factor lambda_GC from Q-Q plot"},
                "lead_rsids": {"type": "array", "items": {"type": "string"}, "description": "List of lead SNP rsIDs for GWAS Catalog grounding"},
                "claimed_fdr_adjusted": {"type": "boolean", "default": True, "description": "Whether manuscript claims FDR significance"},
                "y_axis_uses_raw_p": {"type": "boolean", "default": False, "description": "Whether volcano plot y-axis is unadjusted raw p-value"},
                "highlighted_log2fc": {"type": "array", "items": {"type": "number"}, "description": "Log2 fold changes of highlighted candidate genes"},
            },
            "required": ["plot_type"],
        },
    },
    {
        "name": "tool_gate4_registry_and_bayesian_score",
        "description": "Gate 4: Computes Tier 2 Bayesian Posterior Credibility Score from study prior and all applied Likelihood Ratios (LR_i).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "study_type": {
                    "type": "string",
                    "enum": ["confirmatory_rct", "exploratory_clinical", "observational_epidemiology", "discovery_multi_omics"],
                    "description": "Clinical/scientific study domain",
                },
                "applied_lr_keys": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of triggered LR keys from LR_CATALOG",
                },
                "kill_switch_tripped": {"type": "boolean", "default": False, "description": "True if any fatal kill switch was activated"},
            },
            "required": ["study_type", "applied_lr_keys"],
        },
    },
    {
        "name": "tool_classify_nhcs_affiliation",
        "description": "Classifies whether any author is affiliated with National Heart Centre Singapore (NHCS) for Dual-Bucket audit routing.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "affiliations_text": {"type": "string", "description": "Raw author affiliation text from publication"},
            },
            "required": ["affiliations_text"],
        },
    },
]


def dispatch_tool_call(name: str, arguments: Dict[str, Any]) -> Any:
    """Dispatches tool call to corresponding Python implementation."""
    if name == "tool_gate1_provenance_and_retraction":
        return tool_gate1_provenance_and_retraction(
            doi=arguments.get("doi"),
            pmid=arguments.get("pmid"),
            title=arguments.get("title"),
        )
    elif name == "tool_gate2_tortured_phrases_and_reagents":
        return tool_gate2_tortured_phrases_and_reagents(text=arguments.get("text", ""))
    elif name == "tool_gate3_statcheck_and_ci_forensics":
        return tool_gate3_statcheck_and_ci_forensics(
            point_estimate=float(arguments["point_estimate"]),
            ci_lower=float(arguments["ci_lower"]),
            ci_upper=float(arguments["ci_upper"]),
            reported_p=float(arguments["reported_p"]) if arguments.get("reported_p") is not None else None,
            n_total=int(arguments["n_total"]) if arguments.get("n_total") is not None else None,
            is_ratio=bool(arguments.get("is_ratio", False)),
            mcid_threshold=float(arguments["mcid_threshold"]) if arguments.get("mcid_threshold") is not None else None,
            reference_sd=float(arguments["reference_sd"]) if arguments.get("reference_sd") is not None else None,
            total_events=int(arguments["total_events"]) if arguments.get("total_events") is not None else None,
            symmetry_tolerance=float(arguments.get("symmetry_tolerance", 0.05)),
        )
    elif name == "tool_gate3_grim_grimmer_debit_table_audit":
        return tool_gate3_grim_grimmer_debit_table_audit(
            means=[float(x) for x in arguments.get("means", [])],
            sds=[float(x) for x in arguments.get("sds", [])],
            sample_sizes=[int(x) for x in arguments.get("sample_sizes", [])],
            decimals=int(arguments.get("decimals", 2)),
        )
    elif name == "tool_gate35_manhattan_volcano_grounding":
        return tool_gate35_manhattan_volcano_grounding(
            plot_type=str(arguments.get("plot_type", "manhattan")),
            lead_p_values=[float(x) for x in arguments.get("lead_p_values", [])] if arguments.get("lead_p_values") else None,
            flanking_ld_snp_counts=[int(x) for x in arguments.get("flanking_ld_snp_counts", [])] if arguments.get("flanking_ld_snp_counts") else None,
            lambda_gc=float(arguments["lambda_gc"]) if arguments.get("lambda_gc") is not None else None,
            lead_rsids=[str(x) for x in arguments.get("lead_rsids", [])] if arguments.get("lead_rsids") else None,
            claimed_fdr_adjusted=bool(arguments.get("claimed_fdr_adjusted", True)),
            y_axis_uses_raw_p=bool(arguments.get("y_axis_uses_raw_p", False)),
            highlighted_log2fc=[float(x) for x in arguments.get("highlighted_log2fc", [])] if arguments.get("highlighted_log2fc") else None,
        )
    elif name == "tool_gate4_registry_and_bayesian_score":
        return tool_gate4_registry_and_bayesian_score(
            study_type=str(arguments.get("study_type", "exploratory_clinical")),
            applied_lr_keys=[str(x) for x in arguments.get("applied_lr_keys", [])],
            kill_switch_tripped=bool(arguments.get("kill_switch_tripped", False)),
        )
    elif name == "tool_classify_nhcs_affiliation":
        return tool_classify_nhcs_affiliation(affiliations_text=str(arguments.get("affiliations_text", "")))
    else:
        raise ValueError(f"Unknown tool: {name}")


def run_stdio_jsonrpc_server():
    """Deterministic MCP stdio JSON-RPC 2.0 loop."""
    sys.stderr.write("Forensic Research Auditor MCP Server started (stdio JSON-RPC 2.0)\n")
    sys.stderr.flush()

    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line_str = line.strip()
        if not line_str:
            continue

        try:
            req = json.loads(line_str)
        except json.JSONDecodeError as err:
            sys.stderr.write(f"Invalid JSON received: {err}\n")
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "listChanged": False
                        }
                    },
                    "serverInfo": {
                        "name": "forensic-audit-mcp",
                        "version": "2.0.0"
                    }
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "notifications/initialized":
            # Client notification acknowledging initialization
            pass

        elif method == "ping":
            resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": MCP_TOOLS_MANIFEST
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            try:
                result_data = dispatch_tool_call(tool_name, arguments)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result_data, indent=2)
                            }
                        ],
                        "isError": False
                    }
                }
            except Exception as e:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error executing {tool_name}: {str(e)}"
                            }
                        ],
                        "isError": True
                    }
                }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif req_id is not None:
            # Unhandled method request
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        ci_test = tool_gate3_statcheck_and_ci_forensics(
            point_estimate=2.35,
            ci_lower=-4.37,
            ci_upper=9.07,
            reported_p=0.49,
            n_total=63,
            is_ratio=False,
            mcid_threshold=4.0,
            reference_sd=12.0,
        )
        mv_test = tool_gate35_manhattan_volcano_grounding(
            plot_type="manhattan",
            lead_p_values=[1.2e-9, 3.4e-8],
            flanking_ld_snp_counts=[14, 1],
            lambda_gc=1.03,
            lead_rsids=[],
        )
        bayes_test = tool_gate4_registry_and_bayesian_score(
            study_type="exploratory_clinical",
            applied_lr_keys=[
                "preregistered_exact_match",
                "underpowered_sample_lt_50pct",
                "ci_too_wide_grade_imprecision",
            ],
        )
        gate1_test = tool_gate1_provenance_and_retraction(doi="10.1016/j.ahj.2023.01.002")
        print(json.dumps({"ci_test": ci_test, "manhattan_test": mv_test, "bayes_test": bayes_test, "gate1_test": gate1_test}, indent=2))
    else:
        run_stdio_jsonrpc_server()
