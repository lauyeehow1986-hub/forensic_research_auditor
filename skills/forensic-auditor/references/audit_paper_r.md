# R Forensic Statistical, 95% CI, Diagnostic 2x2 & Resampling Script (`audit_paper.R`)

Save the R code below as `./scripts/audit_paper.R` in your Google Antigravity workspace for execution via `rstudio-mcp`:

```r
# ==============================================================================
# UNIVERSAL FORENSIC RESEARCH AUDIT SUITE (audit_paper.R)
# Metascience, 95% CI Forensics, Multi-Omics & Diagnostic Matrix Validation
# Compatible with Base R (>= 4.2.0) with automatic CRAN package enhancement
# ==============================================================================

# Safe package detection with graceful Base-R fallbacks
has_statcheck <- suppressWarnings(requireNamespace("statcheck", quietly = TRUE))
has_scrutiny  <- suppressWarnings(requireNamespace("scrutiny", quietly = TRUE))
has_rsprite2  <- suppressWarnings(requireNamespace("rsprite2", quietly = TRUE))
has_benford   <- suppressWarnings(requireNamespace("benford.analysis", quietly = TRUE))
has_tibble    <- suppressWarnings(requireNamespace("tibble", quietly = TRUE))

# ------------------------------------------------------------------------------
# 1. STATCHECK: Recalculate inline APA NHST p-values across text sections
# ------------------------------------------------------------------------------
run_statcheck_audit <- function(paper_text_or_pdf_path, is_pdf = FALSE) {
  if (has_statcheck) {
    res <- if (is_pdf) {
      statcheck::checkPDF(paper_text_or_pdf_path)
    } else {
      statcheck::statcheck(paper_text_or_pdf_path)
    }
    if (is.null(res) || nrow(res) == 0) {
      out <- data.frame(Status = "No APA NHST strings detected", stringsAsFactors = FALSE)
      return(if (has_tibble) tibble::as_tibble(out) else out)
    }
    out <- res[, c("Source", "Raw", "Computed", "Error", "DecisionError")]
    return(if (has_tibble) tibble::as_tibble(out) else out)
  }
  
  # --- Base R Fallback NHST Parser ---
  if (is_pdf) {
    warning("statcheck package not installed; PDF direct parsing requires pdftools and statcheck. Provide extracted text to paper_text_or_pdf_path.")
    return(data.frame(Status = "statcheck package not installed for direct PDF read", stringsAsFactors = FALSE))
  }
  
  text <- paste(paper_text_or_pdf_path, collapse = " ")
  # Pattern matches t, F, r, chi2, z
  pattern <- "(?:([tFFrrzZ]|chi2?|\u03c72?|X2)\\s*\\(?([0-9\\.,\\s]+)?\\)?\\s*=\\s*(-?[0-9\\.]+)\\s*,\\s*p\\s*([<>=])\\s*([0-9\\.]+))"
  matches <- gregexpr(pattern, text, perl = TRUE, ignore.case = TRUE)[[1]]
  
  if (length(matches) == 1 && matches[1] == -1) {
    out <- data.frame(Status = "No APA NHST strings detected (Base R fallback)", stringsAsFactors = FALSE)
    return(if (has_tibble) tibble::as_tibble(out) else out)
  }
  
  match_lens <- attr(matches, "match.length")
  raw_strings <- substring(text, matches, matches + match_lens - 1)
  
  parsed_list <- list()
  for (i in seq_along(raw_strings)) {
    raw <- raw_strings[i]
    clean_raw <- gsub("\\s+", "", raw)
    stat_type <- toupper(sub("^([A-Z0-9\u03c7]+).*", "\\1", clean_raw, perl = TRUE))
    
    df_part <- if (grepl("\\(", clean_raw)) sub(".*\\(([^)]+)\\).*", "\\1", clean_raw) else ""
    dfs <- as.numeric(strsplit(df_part, "[,;]")[[1]])
    dfs <- dfs[!is.na(dfs)]
    
    stat_val <- as.numeric(sub(".*=(-?[0-9\\.]+),.*", "\\1", clean_raw))
    op <- sub(".*,p([<>=]).*", "\\1", clean_raw)
    rep_p_str <- sub(".*,p[<>=]([0-9\\.]+).*", "\\1", clean_raw)
    rep_p_str <- sub("[^0-9]+$", "", rep_p_str)
    rep_p <- as.numeric(rep_p_str)
    
    comp_p <- NA_real_
    if (!is.na(stat_val)) {
      if (grepl("T", stat_type) && length(dfs) >= 1) {
        comp_p <- 2 * stats::pt(-abs(stat_val), df = dfs[1])
      } else if (grepl("F", stat_type) && length(dfs) >= 2) {
        comp_p <- 1 - stats::pf(stat_val, df1 = dfs[1], df2 = dfs[2])
      } else if (grepl("R", stat_type) && length(dfs) >= 1) {
        t_equiv <- stat_val * sqrt(dfs[1] / max(1e-9, 1 - stat_val^2))
        comp_p <- 2 * stats::pt(-abs(t_equiv), df = dfs[1])
      } else if (grepl("(CHI|\u03c7|X2)", stat_type) && length(dfs) >= 1) {
        comp_p <- 1 - stats::pchisq(stat_val, df = dfs[1])
      } else if (grepl("Z", stat_type)) {
        comp_p <- 2 * stats::pnorm(-abs(stat_val))
      }
    }
    
    err <- FALSE
    dec_err <- FALSE
    if (!is.na(comp_p) && !is.na(rep_p)) {
      err <- abs(comp_p - rep_p) > 0.01 && !(op == "<" && comp_p < rep_p)
      dec_err <- (rep_p <= 0.05 && comp_p > 0.05) || (rep_p > 0.05 && comp_p <= 0.05)
    }
    
    parsed_list[[i]] <- data.frame(
      Source = paste0("NHST_", sprintf("%02d", i)),
      Raw = raw,
      Computed = round(comp_p, 5),
      Error = err,
      DecisionError = dec_err,
      stringsAsFactors = FALSE
    )
  }
  
  out <- do.call(rbind, parsed_list)
  return(if (has_tibble) tibble::as_tibble(out) else out)
}

# ------------------------------------------------------------------------------
# 2. GRIM & DEBIT: Audit summary tables (Table 1, Table 2, Subgroups)
# ------------------------------------------------------------------------------
run_all_tables_audit <- function(named_tables_list) {
  if (has_scrutiny) {
    results <- lapply(names(named_tables_list), function(tbl_name) {
      df <- named_tables_list[[tbl_name]]
      grim_res <- scrutiny::grim_map(df)
      flagged <- subset(grim_res, consistency == FALSE)
      list(table_name = tbl_name, all_checks = grim_res, impossible_means = flagged)
    })
    names(results) <- names(named_tables_list)
    return(results)
  }
  
  # --- Base R GRIM Granularity Fallback ---
  results <- lapply(names(named_tables_list), function(tbl_name) {
    df <- named_tables_list[[tbl_name]]
    x_col <- if ("x" %in% names(df)) "x" else if ("mean" %in% names(df)) "mean" else names(df)[1]
    n_col <- if ("n" %in% names(df)) "n" else if ("N" %in% names(df)) "N" else names(df)[2]
    
    cons_vec <- logical(nrow(df))
    for (i in seq_len(nrow(df))) {
      x_val <- as.numeric(df[i, x_col])
      n_val <- as.numeric(df[i, n_col])
      x_str <- as.character(df[i, x_col])
      dec_places <- if (grepl("\\.", x_str)) nchar(strsplit(x_str, "\\.")[[1]][2]) else 0
      
      possible_sums <- round(x_val * n_val) + (-3:3)
      possible_means <- round(possible_sums / n_val, dec_places)
      
      possible_k <- round(x_val / 100 * n_val) + (-3:3)
      possible_k <- possible_k[possible_k >= 0 & possible_k <= n_val]
      possible_pcts <- round(possible_k / n_val * 100, dec_places)
      
      is_match <- any(sprintf(paste0("%.", dec_places, "f"), possible_means) == x_str) ||
                  any(sprintf(paste0("%.", dec_places, "f"), possible_pcts) == x_str)
      cons_vec[i] <- is_match
    }
    
    grim_res <- data.frame(
      x = df[[x_col]],
      n = df[[n_col]],
      consistency = cons_vec,
      stringsAsFactors = FALSE
    )
    flagged <- subset(grim_res, consistency == FALSE)
    list(table_name = tbl_name, all_checks = grim_res, impossible_means = flagged)
  })
  names(results) <- names(named_tables_list)
  return(results)
}

# ------------------------------------------------------------------------------
# 3. SPRITE: Scale boundary variance check
# ------------------------------------------------------------------------------
run_sprite_check <- function(mean_val, sd_val, n_obs, min_scale = 1, max_scale = 7) {
  if (has_rsprite2) {
    params <- rsprite2::set_parameters(
      mean = mean_val, sd = sd_val, n_obs = n_obs,
      min_val = min_scale, max_val = max_scale
    )
    possibilities <- rsprite2::find_possible_distributions(params, seed = 42, n_distributions = 5)
    return(possibilities)
  }
  
  # --- Base R Analytical SPRITE Variance Bounds Fallback ---
  obs_var <- sd_val^2
  max_var <- (max_scale - mean_val) * (mean_val - min_scale)
  variance_bounded <- (obs_var <= max_var + 1e-4) && (mean_val >= min_scale) && (mean_val <= max_scale)
  
  return(list(
    mean = mean_val,
    sd = sd_val,
    n = n_obs,
    min_scale = min_scale,
    max_scale = max_scale,
    observed_variance = round(obs_var, 4),
    max_theoretical_variance = round(max_var, 4),
    variance_bounded = variance_bounded,
    status = ifelse(variance_bounded, "PASS: Variance within boundary envelope", "FAIL: Mathematically impossible scale variance")
  ))
}

# ------------------------------------------------------------------------------
# 4. CARLISLE TABLE 1 BASELINE UNIFORMITY & IMBALANCE AUDIT
# ------------------------------------------------------------------------------
run_carlisle_baseline_audit <- function(baseline_p_values, is_randomized_trial = TRUE) {
  if (!isTRUE(is_randomized_trial)) {
    warning("Carlisle baseline uniformity audit is strictly valid ONLY for randomized controlled trials (RCTs). In observational cohorts, non-uniform baseline p-values reflect confounding by indication, not fraudulent allocation.")
    return(list(
      status = "REFUSED_NON_RCT",
      warning = "Carlisle baseline test refused: study is observational / non-randomized. Baseline differences are expected due to confounding by indication.",
      combined_p_value = NA_real_,
      severe_imbalance_risk = FALSE,
      kill_switch_tripped = FALSE
    ))
  }
  
  p_vals <- baseline_p_values[!is.na(baseline_p_values) & baseline_p_values > 0 & baseline_p_values <= 1]
  if (length(p_vals) == 0) {
    return(list(
      status = "EMPTY",
      warning = "No valid baseline p-values provided.",
      combined_p_value = NA_real_,
      severe_imbalance_risk = FALSE,
      kill_switch_tripped = FALSE
    ))
  }
  
  chisq_stat <- -2 * sum(log(p_vals))
  df <- 2 * length(p_vals)
  combined_p <- stats::pchisq(chisq_stat, df = df, lower.tail = FALSE)
  
  kill_switch <- (combined_p < 0.0001 || combined_p > 0.9999)
  imbalance_risk <- (combined_p < 0.05)
  
  return(list(
    status = "AUDITED",
    n_p_values = length(p_vals),
    chisq_stat = round(chisq_stat, 4),
    df = df,
    combined_p_value = round(combined_p, 6),
    severe_imbalance_risk = imbalance_risk,
    kill_switch_tripped = kill_switch
  ))
}

# ------------------------------------------------------------------------------
# 5. BENFORD'S LAW: Audit multi-magnitude numerical tables
# ------------------------------------------------------------------------------
run_comprehensive_benford_audit <- function(
  numeric_vector, 
  table_label = "Dataset", 
  data_type = c("unbounded_spanning_orders", "physiological_vitals", "regression_ratios", "bounded_percentages")
) {
  data_type <- match.arg(data_type)
  guardrail_warning <- NULL
  if (data_type != "unbounded_spanning_orders") {
    guardrail_warning <- sprintf(
      "Guardrail Triggered: '%s' is categorized as %s. Benford's Law strictly requires scale-invariant distributions spanning multiple orders of magnitude. Applying it to homeostatically bounded vitals or regression ratios generates artificial false-positive anomalies.",
      table_label, data_type
    )
    warning(guardrail_warning)
  }
  
  nums <- numeric_vector[!is.na(numeric_vector) & numeric_vector != 0]
  if (length(nums) < 10) {
    return(list(
      label = table_label,
      data_type = data_type,
      warning = "Sample size too small for Benford audit (N < 10).",
      guardrail_warning = guardrail_warning,
      mad_conformity = NA_character_,
      chisq_p_value = NA_real_,
      suspects = numeric(0)
    ))
  }
  
  if (has_benford && data_type == "unbounded_spanning_orders") {
    bfd <- benford.analysis::benford(nums, number.of.digits = 1, discrete = TRUE)
    return(list(
      label = table_label,
      data_type = data_type,
      guardrail_warning = guardrail_warning,
      mad_conformity = bfd$MAD.conformity,
      chisq_p_value = bfd$stats$chisq$p.value,
      suspects = benford.analysis::getSuspects(bfd, nums)
    ))
  }
  
  num_strs <- sprintf("%.10e", abs(nums))
  first_digits <- as.numeric(substr(num_strs, 1, 1))
  first_digits <- first_digits[first_digits >= 1 & first_digits <= 9]
  
  n_total <- length(first_digits)
  observed_counts <- table(factor(first_digits, levels = 1:9))
  observed_props <- observed_counts / n_total
  benford_props <- log10(1 + 1 / (1:9))
  expected_counts <- benford_props * n_total
  
  mad <- mean(abs(observed_props - benford_props))
  mad_conformity <- if (mad <= 0.006) {
    "Close conformity"
  } else if (mad <= 0.012) {
    "Acceptable conformity"
  } else if (mad <= 0.015) {
    "Marginally acceptable"
  } else {
    "Nonconformity"
  }
  
  chisq_res <- stats::chisq.test(x = observed_counts, p = benford_props)
  se_digits <- sqrt(benford_props * (1 - benford_props) / n_total)
  suspect_digits <- which(abs(observed_props - benford_props) > 2 * se_digits)
  
  return(list(
    label = table_label,
    data_type = data_type,
    guardrail_warning = guardrail_warning,
    mad = round(mad, 5),
    mad_conformity = mad_conformity,
    chisq_p_value = round(chisq_res$p.value, 6),
    suspect_digits = suspect_digits,
    suspects = nums[first_digits %in% suspect_digits]
  ))
}

# ------------------------------------------------------------------------------
# 6. SCATTERPLOT & SUBGROUP DENSITY AUDIT (Universal Chart Scrutiny)
# ------------------------------------------------------------------------------
run_chart_density_audit <- function(x_values, y_values, claimed_threshold_x) {
  total_points <- length(x_values)
  high_severity_mask <- x_values >= claimed_threshold_x
  count_high_sev <- sum(high_severity_mask, na.rm = TRUE)
  pct_high_sev <- (count_high_sev / total_points) * 100
  marginal_support <- pct_high_sev < 10.0
  
  return(list(
    total_observations = total_points,
    points_in_claimed_extreme_zone = count_high_sev,
    percentage_in_extreme_zone = round(pct_high_sev, 2),
    unsupported_extrapolation_risk = marginal_support,
    recommended_lr = ifelse(marginal_support, 0.20, 1.00)
  ))
}

# ------------------------------------------------------------------------------
# 7. 95% CONFIDENCE INTERVAL (CI) CONSISTENCY, VARIANCE COMPRESSION & GRADE IMPRECISION AUDIT
# ------------------------------------------------------------------------------
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
  
  implied_se <- (ul_trans - ll_trans) / (2 * stats::qnorm(0.975))
  implied_z  <- abs(est_trans - null_val) / implied_se
  recalculated_p <- 2 * stats::pnorm(-abs(implied_z))
  
  crosses_null <- (ll_trans <= null_val && ul_trans >= null_val)
  decision_error <- FALSE
  if (!is.na(reported_p)) {
    decision_error <- (reported_p < 0.05 && (recalculated_p > 0.05 || crosses_null)) ||
                      (reported_p >= 0.05 && recalculated_p < 0.01 && !crosses_null)
  }
  
  implied_sd <- if (!is.na(n_total) && !is_ratio) implied_se * sqrt(n_total) else NA
  too_narrow_ci_flag <- FALSE
  if (!is.na(implied_sd) && !is.na(reference_sd) && reference_sd > 0) {
    too_narrow_ci_flag <- (implied_sd / reference_sd) < 0.25
  }
  
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

# ------------------------------------------------------------------------------
# 8. MANHATTAN & VOLCANO PLOT FORENSIC AUDIT (Gate 3.5 Genomics Scrutiny)
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# 9. DIAGNOSTIC 2x2 CONTINGENCY MATRIX & HIGH SPECIFICITY MIRAGE AUDIT (Gate 3.6)
# ------------------------------------------------------------------------------
run_diagnostic_2x2_audit <- function(
  sensitivity, 
  specificity, 
  n_cases, 
  n_controls, 
  prevalence = NULL, 
  reported_ppv = NA, 
  reported_npv = NA
) {
  sens <- if (sensitivity > 1.0) sensitivity / 100.0 else sensitivity
  spec <- if (specificity > 1.0) specificity / 100.0 else specificity
  
  tp <- round(sens * n_cases)
  fn <- n_cases - tp
  tn <- round(spec * n_controls)
  fp <- n_controls - tn
  total_n <- n_cases + n_controls
  
  fpr <- if (n_controls > 0) fp / n_controls else (1 - spec)
  fnr <- if (n_cases > 0) fn / n_cases else (1 - sens)
  lr_pos <- if (fpr > 0) sens / fpr else Inf
  lr_neg <- if (spec > 0) fnr / spec else Inf
  dor <- if (fp * fn > 0) (tp * tn) / (fp * fn) else NA_real_
  
  prev_used <- if (!is.null(prevalence)) {
    if (prevalence > 1.0) prevalence / 100.0 else prevalence
  } else {
    n_cases / total_n
  }
  
  denom_ppv <- (sens * prev_used) + (fpr * (1 - prev_used))
  calc_ppv <- if (denom_ppv > 0) (sens * prev_used) / denom_ppv else NA_real_
  
  denom_npv <- (fnr * prev_used) + (spec * (1 - prev_used))
  calc_npv <- if (denom_npv > 0) (spec * (1 - prev_used)) / denom_npv else NA_real_
  
  high_spec_mirage <- (fnr > 0.50) || (!is.na(lr_neg) && lr_neg > 0.80)
  
  ppv_discrepancy <- FALSE
  if (!is.na(reported_ppv)) {
    norm_rep_ppv <- if (reported_ppv > 1.0) reported_ppv / 100.0 else reported_ppv
    ppv_discrepancy <- abs(calc_ppv - norm_rep_ppv) > 0.05
  }
  npv_discrepancy <- FALSE
  if (!is.na(reported_npv)) {
    norm_rep_npv <- if (reported_npv > 1.0) reported_npv / 100.0 else reported_npv
    npv_discrepancy <- abs(calc_npv - norm_rep_npv) > 0.05
  }
  
  rec_lr <- ifelse(high_spec_mirage, 0.20, 1.00)
  
  tbl_matrix <- matrix(
    c(tp, fp, fn, tn),
    nrow = 2,
    byrow = TRUE,
    dimnames = list(
      Test = c("Positive", "Negative"),
      Disease = c("Cases", "Controls")
    )
  )
  
  return(list(
    contingency_table = tbl_matrix,
    total_n = total_n,
    prevalence_applied = round(prev_used, 4),
    sensitivity = round(sens, 4),
    specificity = round(spec, 4),
    false_positive_rate = round(fpr, 4),
    false_negative_rate = round(fnr, 4),
    positive_likelihood_ratio = round(lr_pos, 4),
    negative_likelihood_ratio = round(lr_neg, 4),
    diagnostic_odds_ratio = round(dor, 4),
    reconstructed_ppv = round(calc_ppv, 4),
    reconstructed_npv = round(calc_npv, 4),
    reported_ppv = reported_ppv,
    reported_npv = reported_npv,
    ppv_discrepancy = ppv_discrepancy,
    npv_discrepancy = npv_discrepancy,
    high_specificity_mirage = high_spec_mirage,
    recommended_lr = rec_lr
  ))
}

# ------------------------------------------------------------------------------
# 10. BOOTSTRAP RESAMPLING & SHRINKAGE SIEVE AUDIT (Gate 3.7)
# ------------------------------------------------------------------------------
run_bootstrap_resampling_audit <- function(
  B_iterations, 
  n_sample = NA, 
  claimed_shrinkage = NA, 
  deployed_betas_match_raw = FALSE
) {
  iteration_insufficient <- (B_iterations < 500)
  sample_conflation <- FALSE
  if (!is.na(n_sample)) {
    ratio <- B_iterations / n_sample
    if ((ratio >= 0.4 && ratio <= 0.6) || (B_iterations <= n_sample && B_iterations < 100)) {
      sample_conflation <- TRUE
    }
  }
  unapplied_shrinkage <- isTRUE(deployed_betas_match_raw)
  penalty_triggered <- iteration_insufficient || sample_conflation || unapplied_shrinkage
  rec_lr <- ifelse(penalty_triggered, 0.60, 1.00)
  
  return(list(
    b_iterations = B_iterations,
    n_sample = n_sample,
    iteration_insufficient = iteration_insufficient,
    sample_conflation_risk = sample_conflation,
    claimed_shrinkage = claimed_shrinkage,
    deployed_betas_match_raw = deployed_betas_match_raw,
    unapplied_shrinkage_flag = unapplied_shrinkage,
    recommended_lr = rec_lr
  ))
}

# ------------------------------------------------------------------------------
# 11. SPECTRUM TRUNCATION & ETIOLOGICAL PURGING AUDIT (Gate 4.1)
# ------------------------------------------------------------------------------
run_spectrum_truncation_audit <- function(
  n_screened, 
  n_excluded, 
  excluded_primary_etiologies = character(0), 
  mcar_misused = FALSE
) {
  n_analyzed <- n_screened - n_excluded
  exclusion_rate <- if (n_screened > 0) n_excluded / n_screened else 0.0
  pct_excluded <- exclusion_rate * 100.0
  
  moderate_truncation <- (exclusion_rate > 0.30)
  severe_truncation <- (exclusion_rate > 0.50)
  etiological_paradox <- length(excluded_primary_etiologies) > 0
  penalty_triggered <- severe_truncation || etiological_paradox
  
  rec_lr <- if (penalty_triggered) {
    0.35
  } else if (moderate_truncation || mcar_misused) {
    0.60
  } else {
    1.00
  }
  
  return(list(
    n_screened = n_screened,
    n_excluded = n_excluded,
    n_analyzed = n_analyzed,
    exclusion_rate = round(exclusion_rate, 4),
    percentage_excluded = round(pct_excluded, 2),
    moderate_truncation_warning = moderate_truncation,
    severe_truncation_risk = severe_truncation,
    etiological_paradox_risk = etiological_paradox,
    excluded_primary_etiologies = excluded_primary_etiologies,
    mcar_misuse_flag = isTRUE(mcar_misused),
    recommended_lr = rec_lr
  ))
}
```
