# Step 10 — Quality Control Report

## Overall status

The manuscript has passed a structured internal quality-control review covering:

- numerical consistency against generated research outputs;
- model-definition consistency;
- citation/reference cross-checking;
- journal-scope and formatting review;
- research-integrity language;
- reproducibility documentation;
- figure/table planning;
- wording/originality risk review.

The manuscript is suitable to move into journal-specific formatting, but it should not be submitted until the remaining items in the final checklist are completed.

## 1. Numerical consistency

The following headline values in the manuscript were checked against the generated research outputs and are consistent:

- 678,013 valid frequency policies;
- 358,499.45 policy-years of exposure;
- 36,102 frequency claims;
- 26,639 positive severity rows;
- 26,444 matched positive severity rows;
- 195 unmatched positive severity rows;
- 9,117 policies with frequency/severity count mismatch;
- annual claim frequency 0.100703;
- average matched positive severity 2,265.51;
- matched observed loss cost 167.11;
- frequency × matched-severity benchmark 228.14;
- Poisson test mean deviance 0.321852;
- Poisson test O/E 1.0065;
- Pearson dispersion 2.6058;
- Negative Binomial alpha 0.8596;
- Negative Binomial test O/E 0.9953;
- Gamma test mean deviance 1.884029;
- Gamma test MAE 2,221.54;
- Gamma test O/E 0.9893;
- 99.5% training severity threshold 32,043.36;
- capped-severity Gamma deviance 1.189936;
- capped-severity O/E 1.0157;
- combined matched-loss O/E 0.7478;
- exact-match subset O/E 0.7577.

The driver-age, Bonus-Malus, frequency-calibration, severity-calibration and pure-premium-calibration values used in the manuscript also agree with their generated CSV outputs.

## 2. Research-integrity checks

The manuscript correctly keeps the following concepts separate:

- matched observed loss cost versus frequency × severity benchmark;
- technical pure premium versus final commercial customer premium;
- univariate segment associations versus multivariate adjusted effects;
- association versus causation;
- primary models versus sensitivity analyses;
- aggregate calibration versus local/decile calibration.

The manuscript does not claim that the fitted models are production-ready.

The public frequency/severity reconciliation problem is disclosed rather than hidden.

## 3. Model-definition checks

The final publication pipeline uses:

- one common policy-level 80:20 split;
- random seed 42;
- Poisson GLM with log-exposure offset;
- Gamma GLM with log link;
- driver-age, vehicle-age, Bonus-Malus and vehicle-power bands;
- area, fuel, region and vehicle brand as categorical predictors;
- log(1 + density) as a continuous predictor;
- held-out deviance and O/E calibration;
- frequency and severity decile diagnostics;
- Negative Binomial frequency sensitivity;
- 99.5th-percentile training-only severity sensitivity.

The policy-level split prevents claims from the same policy entering both train and test severity samples.

## 4. Additional exposure/extreme-value audit

The data audit identified 1,224 policies with Exposure > 1 and a maximum exposure of 2.01. Because some public freMTPL2 modelling examples use exposure capping, the research pipeline has been extended to run an exposure-capped-at-1 sensitivity analysis while retaining uncapped exposure as the primary specification.

The completed rerun shows that capping Exposure at 1.0 leaves the frequency result essentially unchanged: held-out Poisson deviance is 0.321827 versus 0.321852 in the primary model, and O/E remains 1.0065. The exposure-above-one records therefore do not materially drive the main frequency conclusions.

The extended audit also records 9 policies with ClaimNb > 4 (maximum 16), 20 matched severity rows above 200,000, a maximum matched severity of 4,075,400.56, matched severity p99 of 16,451.22 and p99.5 of 34,376.96. These are quality-control diagnostics, not automatic deletion rules.

## 5. Reference audit

All references currently listed in the manuscript are cited in the text, and the cited literature is relevant to the claims it supports.

The core bibliography covers:

- foundational GLMs;
- insurance GLMs;
- frequency–severity pure-premium modelling;
- Tweedie modelling;
- frequency–severity dependence;
- French MTPL benchmarking;
- calibration/autocalibration;
- discrimination-free insurance pricing;
- CASdatasets provenance.

The bibliography is sufficient to support the current claims, but the literature review remains relatively compact. For a journal submission, expanding the bibliography with several recent non-life pricing and explainable-ML papers would strengthen the positioning of the contribution.

## 6. Abstract and manuscript style

The abstract has been reduced to 168 words so that it fits the Annals of Actuarial Science requirement of 150–200 words.

The manuscript uses UK English conventions and concise academic wording.

Current manuscript length is approximately 4,000 words excluding supplementary output files, comfortably below the Annals of Actuarial Science 35-page ceiling once normally typeset.

## 7. Figures and tables

Recommended main-paper figures:

1. Study workflow.
2. Observed claim frequency by driver-age band.
3. Bonus-Malus frequency/pure-premium pattern.
4. Frequency observed-versus-predicted calibration by decile.
5. Severity observed-versus-predicted calibration by decile.
6. Combined pure-premium calibration by decile.
7. Selected GLM relativities with 95% confidence intervals.

Recommended main-paper tables:

1. Dataset audit and modelling samples.
2. Portfolio descriptive summary.
3. Key one-factor risk segments.
4. Selected Poisson frequency relativities.
5. Selected Gamma severity relativities.
6. Model-validation and sensitivity summary.

Full coefficient tables should remain supplementary rather than occupy the main manuscript.

## 8. Similarity / plagiarism-risk review

A manual wording review found no deliberate long quotations or copied blocks in the manuscript. The prose is predominantly original synthesis of the analysis and literature.

This is not a substitute for a formal similarity service such as iThenticate or Turnitin. A percentage similarity score cannot be truthfully supplied without running such a service. Before submission, the final formatted manuscript should be checked using an institutionally available similarity tool if available.

## 9. Target-journal working choice

The best working formatting target is **Annals of Actuarial Science (AAS)** because the manuscript is an empirical non-life insurance study with direct actuarial application, transparent statistical modelling and reproducible Python analysis.

AAS explicitly accepts empirical original research, requires the actuarial contribution and practical relevance to be clear, permits papers up to 35 pages, requires UK English, a 150–200-word abstract, Harvard-style references, required competing-interest/data-availability/funding statements and an ORCID for the corresponding author.

ASTIN Bulletin is also thematically relevant, but its stated emphasis on significant original theoretical developments or significant original applications makes it a more demanding target for novelty. It can remain a possible alternative after the final novelty positioning is strengthened.

## 10. Remaining submission checklist

Before submission:

- exposure/extreme-value sensitivity run — completed and incorporated; it does not materially change the main frequency interpretation;
- create publication-quality figures from the generated CSVs;
- consecutively number displayed equations in the journal-formatted version;
- number and caption every table and figure;
- expand the literature review with recent relevant actuarial-pricing papers;
- create or confirm the author's ORCID;
- confirm the preferred author affiliation wording;
- convert the manuscript to the Cambridge/AAS template;
- run spelling/grammar and formal similarity checks;
- prepare a cover letter;
- verify all supplementary files open correctly;
- do a final reference DOI check;
- submit only to one journal at a time.

## QC conclusion

The underlying empirical analysis is reproducible and the manuscript's current headline claims are supported by the generated outputs. The largest remaining work is presentation and publication positioning, not rebuilding the core analysis.
