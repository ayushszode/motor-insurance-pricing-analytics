# Step 5 Research Execution Summary

Generated automatically from the publication-grade research pipeline.

## Dataset audit

- Valid frequency policies: **678,013**
- Total exposure: **358,499.45 policy-years**
- Frequency-table claims: **36,102**
- Positive severity rows: **26,639**
- Matched positive severity rows: **26,444**
- Unmatched positive severity rows: **195**
- Policies with frequency/severity count mismatch: **9,117**

## Held-out models

- Poisson test mean deviance: **0.321852**
- Poisson test O/E: **1.0065**
- Poisson training Pearson dispersion: **2.6058**
- Negative Binomial sensitivity alpha: **0.859609**
- Negative Binomial test mean deviance: **0.285208**
- Gamma severity test mean deviance: **1.884029**
- Gamma severity test MAE: **2,221.54**
- Gamma severity test O/E: **0.9893**
- 99.5% training large-loss cap: **32,043.36**
- Capped Gamma test mean deviance: **1.189936**

## Portfolio benchmarks

- Claim frequency: **0.100703** (10.07 per 100 policy-years)
- Matched average severity: **2,265.51**
- Matched observed loss cost: **167.11 per policy-year**
- Frequency × matched-severity benchmark: **228.14 per policy-year**

## Research integrity note

The source frequency and severity files are not perfectly aligned. The paper must keep
the matched observed loss-cost diagnostic separate from the frequency × severity benchmark
and must not describe either as a final commercial premium.
