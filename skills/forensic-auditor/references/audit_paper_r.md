# R Forensic Statistical, 95% CI & Multi-Omics Chart Auditing Script (`audit_paper.R`)

Save the R code below as `./scripts/audit_paper.R` in your Google Antigravity workspace for execution via `rstudio-mcp`:

```r
library(statcheck)
library(scrutiny)
library(rsprite2)
library(benford.analysis)
library(tibble)

# 1. STATCHECK: Recalculate inline APA NHST p-values across all text sections
run_statcheck_audit <- function(paper_text_or_pdf_path, is_pdf = FALSE) {
  res <- if (is_pdf) {
    statcheck::checkPDF(paper_text_or_pdf_path)
  } else {
    statcheck::statcheck(paper_text_or_pdf_path)
  }
  if (is.null(res) || nrow(res) == 0) {
    return(tibble::tibble(Status = "No APA NHST strings detected"))
  }
  return(res[, c("Source", "Raw", "Computed", "Error", "DecisionError")])
}

# 2. GRIM & DEBIT (scrutiny): Audit ALL summary tables (Table 1, Table 2, Subgroups)
run_all_tables_audit <- function(named_tables_list) {
  results <- lapply(names(named_tables_list), function(tbl_name) {
    df <- named_tables_list[[tbl_name]]
    grim_res <- scrutiny::grim_map(df)
    flagged <- subset(grim_res, consistency == FALSE)
    list(table_name = tbl_name, all_checks = grim_res, impossible_means = flagged)
  })
  names(results) <- names(named_tables_list)
  return(results)
}

# 3. SPRITE (rsprite2): Reconstruct distributions to check scale boundary variance
run_sprite_check <- function(mean_val, sd_val, n_obs, min_scale = 1, max_scale = 7) {
  params <- rsprite2::set_parameters(
    mean = mean_val, sd = sd_val, n_obs = n_obs,
    min_val = min_scale, max_val = max_scale
  )
  possibilities <- rsprite2::find_possible_distributions(params, seed = 42, n_distributions = 5)
  return(possibilities)
}

# 4. CARLISLE TABLE 1 BASELINE UNIFORMITY & IMBALANCE AUDIT
run_carlisle_baseline_audit <- function(baseline_p_values) {
  chisq_stat <- -2 * sum(log(baseline_p_values))
  df <- 2 * length(baseline_p_values)
  combined_p <- pchisq(chisq_stat, df = df, lower.tail = FALSE)
  return(list(
    combined_p_value = combined_p,
    severe_imbalance_risk = (combined_p < 0.05),
    kill_switch_tripped = (combined_p < 0.0001 || combined_p > 0.9999)
  ))
}

# 5. BENFORD'S LAW: Audit ALL multi-magnitude numerical tables
run_comprehensive_benford_audit <- function(numeric_vector, table_label = "Dataset") {
  bfd <- benford.analysis::benford(numeric_vector, number.of.digits = 1, discrete = TRUE)
  return(list(
    label = table_label,
    mad_conformity = bfd$MAD.conformity,
    chisq_p_value  = bfd$stats$chisq$p.value,
    suspects       = benford.analysis::getSuspects(bfd, numeric_vector)
  ))
}

# 6. SCATTERPLOT & SUBGROUP DENSITY AUDIT (Universal Chart Scrutiny)
run_chart_density_audit <- function(x_values, y_values, claimed_threshold_x) {
  total_points <- length(x_values)
  high_severity_mask <- x_values >= claimed_threshold_x
  count_high_sev <- sum(high_severity_mask, na.rm = TRUE)
  pct_high_sev <- (count_high_sev / total_points) * 100
  marginal_support <- pct_high_sev < 10.0
  
  return(list(
    total_observations = total_points,
    points_in_claimed_extreme_zone = count_high_sev,
    percentage_in_extreme_zone = pct_high_sev,
    unsupported_extrapolation_risk = marginal_support,
    recommended_lr = ifelse(marginal_support, 0.20, 1.00)
  ))
}

# 7. 95% CONFIDENCE INTERVAL (CI) CONSISTENCY, VARIANCE COMPRESSION & GRADE IMPRECISION AUDIT
run_ci_consistency_and_width_audit <- function(
  point_est, ci_lower, ci_upper, reported_p = NA, n_total = NA,
  is_ratio = FALSE, mcid_threshold = NA, reference_sd = NA, total_events = NA,
  symmetry_tol = 0.05
) {
  if (is_ratio) {
    est_trans <- log(point_est)
    ll_trans  <- log(ci_lower)
    ul_trans  <- log(ci_upper)
    null_val  <- 0.0
  } else {
    est_trans <- point_est
    ll_trans  <- ci_lower
    ul_trans  <- ci_upper
    null_val  <- 0.0
  }
  
  midpoint <- (ll_trans + ul_trans) / 2.0
  asymmetry_error <- abs(est_trans - midpoint)
  is_symmetric <- asymmetry_error <= symmetry_tol
  
  implied_se <- (ul_trans - ll_trans) / (2 * qnorm(0.975))
  implied_z  <- abs(est_trans - null_val) / implied_se
  recalculated_p <- 2 * pnorm(-abs(implied_z))
  
  crosses_null <- (ll_trans <= null_val && ul_trans >= null_val)
  decision_error <- FALSE
  if (!is.na(reported_p)) {
    decision_error <- (reported_p < 0.05 && (recalculated_p > 0.05 || crosses_null)) ||
                      (reported_p >= 0.05 && recalculated_p < 0.01 && !crosses_null)
  }
  
  # Too-Narrow CI Check (Variance Compression / SE-as-SD Misreporting)
  implied_sd <- if (!is.na(n_total) && !is_ratio) implied_se * sqrt(n_total) else NA
  too_narrow_ci_flag <- FALSE
  if (!is.na(implied_sd) && !is.na(reference_sd) && reference_sd > 0) {
    too_narrow_ci_flag <- (implied_sd / reference_sd) < 0.25
  }
  
  # Too-Wide CI Check (GRADE Imprecision & Optimal Information Size)
  ci_width <- ci_upper - ci_lower
  spans_benefit_and_harm <- FALSE
  if (!is.na(mcid_threshold) && mcid_threshold > 0) {
    if (is_ratio) {
      spans_benefit_and_harm <- (ci_lower < (1 / (1 + mcid_threshold))) && (ci_upper > (1 + mcid_threshold))
    } else {
      spans_benefit_and_harm <- (ci_lower <= -abs(mcid_threshold) && ci_upper >= abs(mcid_threshold)) ||
                                (ci_width > 2.0 * abs(mcid_threshold))
    }
  }
  under_ois <- (!is.na(total_events) && total_events < 300) || (!is.na(n_total) && n_total < 400 && crosses_null)
  too_wide_ci_imprecision <- spans_benefit_and_harm || (under_ois && !is.na(mcid_threshold) && (abs(ci_lower) >= abs(mcid_threshold) || abs(ci_upper) >= abs(mcid_threshold)))
  
  lr_ci <- 1.00
  if (too_narrow_ci_flag) lr_ci <- lr_ci * 0.15
  if (too_wide_ci_imprecision) lr_ci <- lr_ci * 0.40
  if (!is_symmetric && !decision_error) lr_ci <- lr_ci * 0.20
  
  return(list(
    point_estimate = point_est,
    ci_95 = c(ci_lower, ci_upper),
    is_symmetric = is_symmetric,
    asymmetry_error = round(asymmetry_error, 4),
    implied_se = round(implied_se, 4),
    implied_z = round(implied_z, 4),
    recalculated_p = round(recalculated_p, 6),
    reported_p = reported_p,
    decision_error_kill_switch = decision_error,
    implied_sd = round(implied_sd, 4),
    too_narrow_ci_variance_compression = too_narrow_ci_flag,
    too_wide_ci_grade_imprecision = too_wide_ci_imprecision,
    recommended_lr = round(lr_ci, 4)
  ))
}

# 8. MANHATTAN & VOLCANO PLOT FORENSIC AUDIT (Gate 3.5 Genomics Scrutiny)
run_manhattan_volcano_audit <- function(
  plot_type = c("manhattan", "volcano"),
  lead_p_values = numeric(0),
  flanking_ld_snp_counts = integer(0),
  lambda_gc = NA,
  claimed_fdr_adjusted = TRUE,
  y_axis_uses_raw_p = FALSE,
  highlighted_log2fc = numeric(0),
  gwas_or_opentargets_grounded = TRUE
) {
  plot_type <- match.arg(plot_type)
  if (plot_type == "manhattan") {
    gw_sig_mask <- lead_p_values < 5e-8
    chimney_loci <- sum(flanking_ld_snp_counts < 2, na.rm = TRUE)
    inflation_anomaly <- !is.na(lambda_gc) && (lambda_gc > 1.15 || lambda_gc < 0.90)
    suggestive_overclaim <- any(lead_p_values >= 5e-8 & lead_p_values < 1e-5)
    
    penalty_triggered <- (chimney_loci > 0) || inflation_anomaly || !gwas_or_opentargets_grounded
    return(list(
      plot_type = "manhattan",
      genome_wide_sig_count = sum(gw_sig_mask),
      isolated_chimney_loci_count = chimney_loci,
      lambda_gc = lambda_gc,
      inflation_anomaly = inflation_anomaly,
      suggestive_threshold_overclaim = suggestive_overclaim,
      mcp_grounding_verified = gwas_or_opentargets_grounded,
      recommended_lr = ifelse(penalty_triggered, 0.15, 1.00)
    ))
  } else {
    fdr_masquerade <- claimed_fdr_adjusted && y_axis_uses_raw_p
    noise_zone_genes <- sum(abs(highlighted_log2fc) < 0.585, na.rm = TRUE)
    penalty_triggered <- fdr_masquerade || (noise_zone_genes > 0) || !gwas_or_opentargets_grounded
    return(list(
      plot_type = "volcano",
      raw_p_masquerading_as_fdr = fdr_masquerade,
      highlighted_genes_in_noise_zone = noise_zone_genes,
      mcp_grounding_verified = gwas_or_opentargets_grounded,
      recommended_lr = ifelse(penalty_triggered, 0.20, 1.00)
    ))
  }
}
```
