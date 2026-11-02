# ==============================================================================
# TEST SUITE: test_audit_paper.R
# Comprehensive unit & edge-case test suite for scripts/audit_paper.R
# ==============================================================================

source("scripts/audit_paper.R")

test_failures <- 0
test_count <- 0

assert_true <- function(condition, test_name) {
  test_count <<- test_count + 1
  if (isTRUE(condition)) {
    cat(sprintf("[PASS] %s\n", test_name))
  } else {
    test_failures <<- test_failures + 1
    cat(sprintf("[FAIL] %s\n", test_name))
  }
}

assert_equal <- function(actual, expected, test_name, tol = 1e-5) {
  test_count <<- test_count + 1
  match <- if (is.numeric(actual) && is.numeric(expected)) {
    abs(actual - expected) < tol
  } else {
    identical(actual, expected)
  }
  if (isTRUE(match)) {
    cat(sprintf("[PASS] %s\n", test_name))
  } else {
    test_failures <<- test_failures + 1
    cat(sprintf("[FAIL] %s: expected %s, got %s\n", test_name, as.character(expected), as.character(actual)))
  }
}

cat("\n--- 1. STATCHECK AUDIT TESTS ---\n")
# Lowercase p
sc1 <- run_statcheck_audit("t(34) = 2.15, p = 0.038")
assert_true(nrow(sc1) == 1 && sc1$Computed[1] > 0.03 && sc1$Computed[1] < 0.04, "statcheck parses lowercase p")

# Uppercase P with decision error (prior bug)
sc2 <- run_statcheck_audit("t(34) = 1.0, P = 0.01")
assert_true(isTRUE(sc2$DecisionError[1]), "statcheck catches decision error with uppercase P")

# Semicolon separator
sc3 <- run_statcheck_audit("t(34) = 2.15; p = 0.038")
assert_true(nrow(sc3) == 1 && !is.na(sc3$Computed[1]), "statcheck parses semicolon separator")

# Non-APA text
sc4 <- run_statcheck_audit("No statistics reported here.")
assert_true(grepl("No APA", sc4$Status[1]), "statcheck handles text without APA NHST strings")


cat("\n--- 2. ALL TABLES (GRIM) AUDIT TESTS ---\n")
tbl_good <- data.frame(x = c(5.0, 4.0), n = c(10, 10))
tbl_res1 <- run_all_tables_audit(list(T1 = tbl_good))
assert_true(all(tbl_res1$T1$all_checks$consistency), "GRIM passes consistent integer means")

tbl_bad <- data.frame(x = c(5.13), n = c(10))
tbl_res2 <- run_all_tables_audit(list(T2 = tbl_bad))
assert_true(nrow(tbl_res2$T2$impossible_means) == 1, "GRIM flags mathematically impossible means")

# Empty table list
tbl_empty <- run_all_tables_audit(list())
assert_true(length(tbl_empty) == 0, "GRIM handles empty table list")

# Zero and NA sample size
tbl_zero <- data.frame(x = c(5.0, 4.0), n = c(0, NA))
tbl_res3 <- run_all_tables_audit(list(T3 = tbl_zero))
assert_true(nrow(tbl_res3$T3$impossible_means) == 2, "GRIM flags zero and NA sample sizes without crash")


cat("\n--- 3. SPRITE SCALE VARIANCE TESTS ---\n")
sp_good <- run_sprite_check(mean_val = 4.0, sd_val = 1.5, n_obs = 50, min_scale = 1, max_scale = 7)
assert_true(isTRUE(sp_good$variance_bounded), "SPRITE passes valid bounded variance")

sp_bad <- run_sprite_check(mean_val = 6.8, sd_val = 2.0, n_obs = 50, min_scale = 1, max_scale = 7)
assert_true(isFALSE(sp_bad$variance_bounded), "SPRITE catches impossible scale variance")

sp_na <- run_sprite_check(mean_val = NA, sd_val = 1.0, n_obs = 50)
assert_true(grepl("INVALID", sp_na$status), "SPRITE handles NA input safely")


cat("\n--- 4. CARLISLE BASELINE AUDIT TESTS ---\n")
# Refuse on observational cohorts
c_obs <- run_carlisle_baseline_audit(c(0.2, 0.4, 0.6), is_randomized_trial = FALSE)
assert_equal(c_obs$status, "REFUSED_NON_RCT", "Carlisle guardrail refuses non-RCTs")

# Audit on RCT
c_rct <- run_carlisle_baseline_audit(c(0.2, 0.4, 0.6, 0.8), is_randomized_trial = TRUE)
assert_equal(c_rct$status, "AUDITED", "Carlisle audits RCT baseline p-values")
assert_true(!isTRUE(c_rct$kill_switch_tripped), "Carlisle passes uniform p-values")

# Empty p-values
c_empty <- run_carlisle_baseline_audit(numeric(0), is_randomized_trial = TRUE)
assert_equal(c_empty$status, "EMPTY", "Carlisle handles empty input safely")


cat("\n--- 5. BENFORD AUDIT TESTS ---\n")
# Scale invariant multi-magnitude
bf_good <- run_comprehensive_benford_audit(
  numeric_vector = 10^(runif(100, 1, 5)), 
  table_label = "LogUniformCounts", 
  data_type = "unbounded_spanning_orders"
)
assert_true(!is.na(bf_good$mad), "Benford computes MAD on scale-invariant numbers")

# Guardrail warning on physiological vitals
suppressWarnings({
  bf_vitals <- run_comprehensive_benford_audit(
    numeric_vector = rnorm(50, 120, 10), 
    table_label = "SBP_Vitals", 
    data_type = "physiological_vitals"
  )
})
assert_true(!is.null(bf_vitals$guardrail_warning), "Benford triggers guardrail on physiological vitals")


cat("\n--- 6. SCATTERPLOT DENSITY AUDIT TESTS ---\n")
# Normal supported zone
cd_pass <- run_chart_density_audit(x_values = rep(c(150, 170), each = 50), y_values = 1:100, claimed_threshold_x = 160)
assert_equal(cd_pass$recommended_lr, 1.00, "Scatterplot passes when extreme zone has >= 10% density")

# Extreme zone under-represented
cd_fail <- run_chart_density_audit(x_values = c(rep(120, 95), rep(170, 5)), y_values = 1:100, claimed_threshold_x = 160)
assert_equal(cd_fail$recommended_lr, 0.20, "Scatterplot penalizes when extreme zone has < 10% density")

# Empty vectors
cd_empty <- run_chart_density_audit(numeric(0), numeric(0), 160)
assert_equal(cd_empty$total_observations, 0, "Scatterplot handles empty input without crash")
assert_equal(cd_empty$recommended_lr, 1.00, "Scatterplot empty returns clean LR")


cat("\n--- 7. 95% CI FORENSIC AUDIT TESTS ---\n")
# Decision error: crosses null while claiming p < 0.05
ci_dec <- run_ci_consistency_and_width_audit(point_est = 1.05, ci_lower = 0.95, ci_upper = 1.15, reported_p = 0.02, is_ratio = TRUE)
assert_true(isTRUE(ci_dec$decision_error_kill_switch), "95% CI catches decision error when CI crosses null")

# Ratio with non-positive lower bound (prior crash bug)
ci_neg <- run_ci_consistency_and_width_audit(point_est = 1.2, ci_lower = -0.1, ci_upper = 2.0, is_ratio = TRUE)
assert_true(isTRUE(ci_neg$decision_error_kill_switch), "95% CI catches impossible negative ratio bound without crash")
assert_equal(ci_neg$recommended_lr, 0.20, "95% CI assigns penalty for impossible ratio bounds")

# Asymmetric linear CI without decision error
ci_asym <- run_ci_consistency_and_width_audit(point_est = 5.0, ci_lower = 2.0, ci_upper = 12.0)
assert_true(isFALSE(ci_asym$is_symmetric), "95% CI catches linear asymmetry")
assert_equal(ci_asym$recommended_lr, 0.20, "95% CI penalizes asymmetry")

# Asymmetric linear CI with decision error
ci_dec_err <- run_ci_consistency_and_width_audit(point_est = 5.0, ci_lower = 2.0, ci_upper = 12.0, reported_p = 0.001)
assert_true(isTRUE(ci_dec_err$decision_error_kill_switch), "95% CI catches decision error")
assert_equal(ci_dec_err$recommended_lr, 0.05, "95% CI assigns LR = 0.05 for decision error")


cat("\n--- 8. MANHATTAN & VOLCANO AUDIT TESTS ---\n")
# Manhattan chimney
m_chimney <- run_manhattan_volcano_audit(plot_type = "manhattan", lead_p_values = c(1e-9), flanking_ld_snp_counts = c(0))
assert_equal(m_chimney$recommended_lr, 0.15, "Manhattan flags isolated LD chimney")

# Volcano FDR masquerade
v_fdr <- run_manhattan_volcano_audit(plot_type = "volcano", claimed_fdr_adjusted = TRUE, y_axis_uses_raw_p = TRUE)
assert_equal(v_fdr$recommended_lr, 0.20, "Volcano flags raw p masquerading as FDR")


cat("\n--- 9. DIAGNOSTIC 2x2 CONTINGENCY MATRIX & HIGH SPECIFICITY MIRAGE TESTS ---\n")
# High Specificity Mirage
d_mirage <- run_diagnostic_2x2_audit(sensitivity = 0.40, specificity = 0.90, n_cases = 100, n_controls = 100)
assert_true(isTRUE(d_mirage$high_specificity_mirage), "Diagnostic catches High Specificity Mirage")
assert_equal(d_mirage$recommended_lr, 0.20, "Diagnostic assigns LR = 0.20 for High Specificity Mirage")

# Clean diagnostic test
d_clean <- run_diagnostic_2x2_audit(sensitivity = 0.85, specificity = 0.92, n_cases = 100, n_controls = 100)
assert_true(isFALSE(d_clean$high_specificity_mirage), "Diagnostic passes high-sensitivity test")
assert_equal(d_clean$recommended_lr, 1.00, "Clean diagnostic has LR = 1.00")

# Boundary: n_cases = 0, n_controls = 0 (prior crash bug)
d_zero <- run_diagnostic_2x2_audit(sensitivity = 0.8, specificity = 0.9, n_cases = 0, n_controls = 0)
assert_equal(d_zero$total_n, 0, "Diagnostic handles zero cases and zero controls without crash")
assert_true(is.na(d_zero$reconstructed_ppv), "Reconstructed PPV is NA when total N is zero")

# Boundary: n_cases = 10, n_controls = 0
d_cases_only <- run_diagnostic_2x2_audit(sensitivity = 0.8, specificity = 0.9, n_cases = 10, n_controls = 0)
assert_equal(d_cases_only$total_n, 10, "Diagnostic handles zero controls safely")

# Boundary: n_cases = 0, n_controls = 10
d_ctrl_only <- run_diagnostic_2x2_audit(sensitivity = 0.8, specificity = 0.9, n_cases = 0, n_controls = 10)
assert_equal(d_ctrl_only$total_n, 10, "Diagnostic handles zero cases safely")

# Specificity = 0
d_spec0 <- run_diagnostic_2x2_audit(sensitivity = 0.8, specificity = 0, n_cases = 10, n_controls = 10)
assert_true(isFALSE(d_spec0$high_specificity_mirage), "Specificity = 0 does not trigger High Specificity Mirage")


cat("\n--- 10. BOOTSTRAP RESAMPLING & SHRINKAGE SIEVE TESTS ---\n")
# Insufficient iterations (B < 500)
b_few <- run_bootstrap_resampling_audit(B_iterations = 300)
assert_true(isTRUE(b_few$iteration_insufficient), "Bootstrap flags B < 500 as insufficient")
assert_equal(b_few$recommended_lr, 0.60, "Insufficient B assigns LR = 0.60")

# Sample conflation (B = 50% of N)
b_conflate <- run_bootstrap_resampling_audit(B_iterations = 50, n_sample = 100)
assert_true(isTRUE(b_conflate$sample_conflation_risk), "Bootstrap flags sample size vs iteration conflation")
assert_equal(b_conflate$recommended_lr, 0.60, "Conflation assigns LR = 0.60")

# Unapplied shrinkage (deployed betas match raw)
b_unapplied <- run_bootstrap_resampling_audit(B_iterations = 1000, deployed_betas_match_raw = TRUE)
assert_true(isTRUE(b_unapplied$unapplied_shrinkage_flag), "Bootstrap flags unapplied shrinkage")
assert_equal(b_unapplied$recommended_lr, 0.60, "Unapplied shrinkage assigns LR = 0.60")

# Clean bootstrap
b_clean <- run_bootstrap_resampling_audit(B_iterations = 1000, deployed_betas_match_raw = FALSE)
assert_equal(b_clean$recommended_lr, 1.00, "Clean bootstrap assigns LR = 1.00")

# Missing / NA / NULL B
b_na <- run_bootstrap_resampling_audit(B_iterations = NA)
assert_true(isTRUE(b_na$iteration_insufficient), "Bootstrap flags NA iterations")
assert_equal(b_na$recommended_lr, 0.60, "Missing B returns numeric LR = 0.60")

b_null <- run_bootstrap_resampling_audit(B_iterations = NULL)
assert_true(isTRUE(b_null$iteration_insufficient), "Bootstrap flags NULL iterations")
assert_equal(b_null$recommended_lr, 0.60, "NULL B returns numeric LR = 0.60")


cat("\n--- 11. SPECTRUM TRUNCATION & ETIOLOGICAL PURGING TESTS ---\n")
# Severe truncation (> 50% excluded)
st_sev <- run_spectrum_truncation_audit(n_screened = 1000, n_excluded = 550)
assert_true(isTRUE(st_sev$severe_truncation_risk), "Spectrum flags > 50% exclusion as severe")
assert_equal(st_sev$recommended_lr, 0.35, "Severe truncation assigns LR = 0.35")

# Moderate truncation (> 30% excluded)
st_mod <- run_spectrum_truncation_audit(n_screened = 1000, n_excluded = 350)
assert_true(isTRUE(st_mod$moderate_truncation_warning), "Spectrum flags > 30% exclusion as moderate")
assert_equal(st_mod$recommended_lr, 0.60, "Moderate truncation assigns LR = 0.60")

# Etiological paradox
st_etio <- run_spectrum_truncation_audit(
  n_screened = 1000, 
  n_excluded = 100, 
  excluded_primary_etiologies = c("Ischemic Cardiomyopathy")
)
assert_true(isTRUE(st_etio$etiological_paradox_risk), "Spectrum flags purged primary etiologies")
assert_equal(st_etio$recommended_lr, 0.35, "Etiological paradox assigns LR = 0.35")

# Clean cohort flow
st_clean <- run_spectrum_truncation_audit(n_screened = 1000, n_excluded = 100)
assert_equal(st_clean$recommended_lr, 1.00, "Clean cohort assigns LR = 1.00")

# Inverted / impossible counts (n_excluded > n_screened)
st_inv <- run_spectrum_truncation_audit(n_screened = 100, n_excluded = 120)
assert_equal(st_inv$n_analyzed, 0, "Spectrum caps n_analyzed at 0 for impossible exclusions")
assert_equal(st_inv$exclusion_rate, 1.0, "Spectrum caps exclusion rate at 1.0")

# Zero screened
st_zero <- run_spectrum_truncation_audit(n_screened = 0, n_excluded = 0)
assert_equal(st_zero$n_analyzed, 0, "Spectrum handles zero screened cohort safely")


cat("\n======================================================\n")
cat(sprintf("TEST SUMMARY: %d passed, %d failed out of %d total tests.\n", test_count - test_failures, test_failures, test_count))
if (test_failures > 0) {
  stop(sprintf("FAILED %d test(s)!", test_failures))
} else {
  cat("ALL TESTS PASSED WITH 100% SUCCESS!\n")
}
cat("======================================================\n")
