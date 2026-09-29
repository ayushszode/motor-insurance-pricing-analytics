# Interpretable Motor Insurance Pricing with Frequency–Severity Generalized Linear Models: Evidence from the freMTPL2 Portfolio

**Ayush Sanjay Zode**  
Independent Researcher, Liverpool, United Kingdom  
Corresponding author: ayushsanjayzode@gmail.com

**Manuscript version:** 29 September 2026

---

## Abstract

Motor-insurance pricing requires risk differentiation that is both predictive and interpretable. This study evaluates a frequency–severity Generalized Linear Model (GLM) framework using the public freMTPL2 French Motor Third-Party Liability portfolio. The analysis uses 678,013 policy records, 358,499.45 policy-years of exposure and 36,102 recorded claims; 26,444 positive severity records can be matched to policy records. Claim frequency is modelled using a Poisson GLM with log-exposure offset, and positive claim severity using a Gamma GLM with log link, under a common policy-level 80:20 train-test split. The frequency model is well balanced on held-out data (O/E 1.0065) but materially overdispersed (Pearson dispersion 2.6058). Bonus-Malus is the strongest adjusted frequency signal, while driver age is the clearest stable severity signal. The severity model is close to aggregate balance (O/E 0.9893) but shows substantial decile-level miscalibration and sensitivity to large claims. Combined pure-premium predictions overstate matched historical loss cost (O/E 0.7478), with interpretation constrained by known frequency–severity source inconsistency. The results support GLMs as an explainable actuarial baseline rather than a production-ready tariff.

**Keywords:** motor insurance pricing; generalized linear models; claim frequency; claim severity; pure premium; Poisson regression; Gamma regression; actuarial analytics; freMTPL2

---

# 1. Introduction

## 1.1 Background

Motor insurers must estimate the expected future claim cost associated with policyholders who differ in driver, vehicle and geographic characteristics. A pricing model therefore needs to translate observed historical experience into expected loss cost while distinguishing between risks in a way that can be understood, validated and governed. Generalized Linear Models (GLMs), introduced formally by Nelder and Wedderburn (1972), provide a flexible statistical framework for non-normal response distributions and remain widely applicable to insurance data. De Jong and Heller (2008) describe GLMs as particularly suited to actuarial problems involving claim counts, claim amounts and varying exposure periods.

A conventional actuarial approach decomposes expected claim cost into two components: claim frequency and claim severity. Claim frequency represents how often claims are expected to occur, while claim severity represents the expected cost of a positive claim. The two conditional expectations can then be combined to obtain an expected loss-cost or pure-premium indication. Schirmacher (2016) presents this frequency–severity construction as a core insurance-pricing workflow, while Tevet (2016) compares the approach with direct pure-premium modelling using Tweedie methods.

This decomposition has an important interpretability advantage. Two policy segments can have similar expected loss cost for very different reasons: one may generate many relatively small claims, while another may generate fewer but substantially larger claims. Modelling the components separately enables an analyst to identify the source of the risk difference rather than observing only the final aggregate expected cost.

## 1.2 Problem statement

Classical GLMs offer transparency, but their assumptions may be restrictive. A Poisson frequency model assumes a specific mean–variance relationship, while a Gamma severity model imposes a particular positive continuous response structure. Main-effects GLMs may also fail to capture nonlinear interactions that more flexible machine-learning models can learn automatically. Noll, Salzmann and Wüthrich (2020), using French motor third-party liability data, show that a relatively simple GLM can fail to represent interaction effects that tree-based and neural-network models can capture.

Model evaluation is another challenge. A model can appear balanced at portfolio level while being materially miscalibrated across subgroups. Denuit, Charpentier and Trufin (2021) show that predictive performance and actuarial balance are distinct considerations and motivate explicit calibration assessment. In addition, frequency and severity need not be conditionally independent; Garrido, Genest and Schulz (2016) demonstrate how dependence can be incorporated within a frequency–severity framework.

The present study therefore does not ask whether GLMs are universally superior to alternative methods. Instead, it asks how far an interpretable GLM framework can go on a large public motor-insurance portfolio when the analysis explicitly examines calibration, overdispersion, large-loss sensitivity and source-data quality.

## 1.3 Research question

The primary research question is:

> **To what extent can interpretable frequency–severity Generalized Linear Models estimate motor-insurance risk and produce differentiated pure-premium estimates across policyholder and vehicle characteristics in the freMTPL2 portfolio?**

The supporting questions are whether observed risk patterns persist under multivariate adjustment, how effectively Poisson and Gamma GLMs perform on held-out data, and what calibration emerges when the two components are combined.

## 1.4 Objectives and contribution

The study audits and describes the freMTPL2 portfolio, fits exposure-adjusted Poisson and Gamma GLMs, combines their predictions into annual pure-premium indications, evaluates calibration, examines Poisson overdispersion through a Negative Binomial sensitivity specification, assesses severity-tail sensitivity, and identifies source-data limitations affecting validation.

The contribution is empirical and methodological rather than theoretical. The study provides a reproducible application of the classical frequency–severity framework while integrating data-quality auditing, policy-level train-test separation, calibration diagnostics, overdispersion analysis, large-loss sensitivity and transparent interpretation of model relativities.

---

# 2. Literature Review

## 2.1 GLMs and insurance pricing

GLMs extend ordinary linear regression by combining an exponential-family response distribution with a link function connecting the conditional mean to a systematic component (Nelder & Wedderburn, 1972). This makes them appropriate for insurance outcomes that are not normally distributed. De Jong and Heller (2008) provide an insurance-oriented treatment covering count responses, continuous positive responses and varying policy exposure.

## 2.2 Frequency–severity decomposition

The classical framework models expected aggregate loss as the product of expected claim frequency and expected positive claim severity. Schirmacher (2016) presents separate frequency and severity GLMs as a fundamental pure-premium workflow. Tevet (2016) compares this with direct pure-premium modelling and highlights that both approaches have advantages.

The separate approach is especially useful when interpretation matters because the same total expected loss can arise through different combinations of frequency and severity.

## 2.3 Poisson frequency and exposure

For policy i with claim count N_i and exposure E_i, a Poisson GLM can be written as:

\[
\log(E[N_i]) = \log(E_i) + \beta_0 + \sum_k \beta_k X_{ki}.
\]

The log-exposure offset allows policies with different observation periods to be compared on an annualised basis.

A central limitation is overdispersion. If the conditional claim-count variance materially exceeds the Poisson mean, a Negative Binomial or other flexible count model may be preferable.

## 2.4 Severity and tail risk

Positive claim amounts are continuous and typically strongly right-skewed. A Gamma GLM with log link is therefore a common actuarial baseline. However, severity can be highly sensitive to extreme claims, motivating explicit tail analysis rather than reliance on average model fit alone.

## 2.5 Tweedie alternatives

Jørgensen and Paes de Souza (1994) establish the compound Poisson–Gamma connection underlying Tweedie modelling of insurance loss. Tevet (2016) discusses Tweedie direct pure-premium models as an alternative to separate frequency and severity models. Tweedie modelling is retained as a future challenger because the current study prioritises component-level interpretability.

## 2.6 Dependence, interactions and calibration

Garrido et al. (2016) show that frequency and severity need not be independent and demonstrate an extension in which claim count enters the severity model.

Noll et al. (2020) show that relatively simple GLMs may fail to capture interactions that tree-based and neural-network methods learn more naturally. This frames the present GLMs as interpretable baselines rather than universally optimal predictive models.

Denuit et al. (2021) emphasise calibration and actuarial balance. A model that is correct on average can still be materially wrong for groups receiving similar predictions. The present study therefore combines held-out deviance with observed-versus-predicted calibration.

## 2.7 Fairness and governance

Lindholm, Richman, Tsanakas and Wüthrich (2022) show that insurance pricing can raise direct and proxy-discrimination concerns even when protected variables are not explicitly used. The present study does not perform a complete fairness audit, but recognises fairness, governance and legal review as requirements for production use.

---

# 3. Data and Data Preparation

## 3.1 Dataset

The study uses the freMTPL2 French Motor Third-Party Liability benchmark dataset family distributed through public actuarial data resources associated with CASdatasets (Dutang & Charpentier, 2026). The exact public distribution analysed here contains 678,013 frequency-policy records and 26,639 positive-severity rows.

The research pipeline records SHA-256 checksums for the exact source files:

- Frequency: 66477b983cc81b23f75590ad72e00ad4cc4b92a956b22b93732adb6070f006fb
- Severity: 27bdce2d8628e06236afa5d1a174f5885148032f003cb635305e600c2fa922ad

This guards against silent differences between public/package versions.

## 3.2 Variables

The frequency data include policy identifier, claim count, exposure, area, vehicle power, vehicle age, driver age, Bonus-Malus, vehicle brand, fuel type, population density and region. The severity data include policy identifier and positive claim amount.

## 3.3 Data-quality audit

The final pipeline retains frequency rows with positive exposure and non-negative claim count and severity rows with positive claim amounts. All 678,013 frequency rows meet the implemented validity rules.

The frequency file contains 36,102 recorded claims. Of 26,639 positive severity rows, 26,444 match a policy identifier in the frequency table and 195 do not. A further 9,117 policies have a frequency claim count greater than the number of matched severity rows.

Because the two sources do not fully reconcile, the study distinguishes:

1. **Matched observed loss cost** — matched claim amount divided by exposure.
2. **Frequency × matched-severity benchmark** — annual observed frequency multiplied by average matched positive severity.

They are not treated as interchangeable.

## 3.4 Portfolio summary

| Metric | Value |
|---|---:|
| Frequency-policy records | 678,013 |
| Exposure | 358,499.45 policy-years |
| Frequency-table claims | 36,102 |
| Annual claim frequency | 0.100703 |
| Claims per 100 policy-years | 10.07 |
| Positive severity rows | 26,639 |
| Matched severity rows | 26,444 |
| Average matched severity | 2,265.51 |
| Matched observed loss cost | 167.11 |
| Frequency × matched-severity benchmark | 228.14 |

## 3.5 Feature engineering

Driver age is grouped into 18–25, 26–35, 36–45, 46–55, 56–65 and 66+. Vehicle age is grouped into 0–2, 3–5, 6–10 and 11+. Bonus-Malus is grouped into <=50, 51–75, 76–100 and >100. Vehicle power is grouped into 4–6, 7–9 and 10+.

Area, fuel type, region and vehicle brand remain categorical. Density is transformed using log(1 + Density).

## 3.6 Policy-level train-test split

A reproducible 80:20 split is created at policy level using random seed 42. All claims belonging to the same policy therefore remain in the same partition.

| Sample | Rows |
|---|---:|
| Frequency train | 542,410 |
| Frequency test | 135,603 |
| Severity train | 21,044 |
| Severity test | 5,400 |

A chronological split is not used because the dataset does not provide a suitable policy-level temporal variable for robust out-of-time validation.

---

# 4. Methodology

## 4.1 Descriptive analysis

For group g, annual claim frequency is:

\[
\hat f_g = \frac{\sum_{i \in g} ClaimNb_i}{\sum_{i \in g} Exposure_i}.
\]

Average matched severity is:

\[
\hat s_g = \frac{\sum_{j \in g} ClaimAmount_j}{n^{sev}_g}.
\]

The descriptive frequency–severity benchmark is:

\[
\widehat{PP}_g = \hat f_g \times \hat s_g.
\]

These are exploratory associations, not causal effects or final tariff factors.

## 4.2 Poisson frequency GLM

The primary frequency model assumes:

\[
N_i \sim Poisson(\mu_i),
\]

\[
\log(\mu_i) = \log(E_i) + \beta_0 + \sum_k \beta_k X_{ki}.
\]

Covariates are driver-age band, vehicle-age band, Bonus-Malus band, vehicle-power band, area, fuel, region, vehicle brand and log density.

## 4.3 Frequency validation

Held-out mean Poisson deviance is the primary distribution-specific test metric. Aggregate calibration is measured by:

\[
O/E = \frac{\sum_i N_i}{\sum_i \hat \mu_i}.
\]

The test sample is also divided into ten predicted-frequency groups. Training Pearson dispersion is:

\[
\phi = \frac{\chi^2_P}{df_{resid}}.
\]

## 4.4 Negative Binomial sensitivity

A Negative Binomial GLM is fitted as a sensitivity specification using a method-of-moments dispersion estimate. Because Poisson and Negative Binomial deviances arise under different variance functions, absolute deviance values are not treated as a direct like-for-like ranking.

## 4.5 Gamma severity GLM

Positive claim severity uses:

\[
Y_j \sim Gamma,
\]

\[
\log(E[Y_j]) = \alpha_0 + \sum_k \alpha_k X_{kj}.
\]

The same rating-factor structure is used, and the common policy split prevents same-policy severity leakage.

## 4.6 Severity validation

The severity model is evaluated using held-out mean Gamma deviance, MAE, aggregate observed-to-expected ratio and decile calibration.

## 4.7 Large-loss sensitivity

A sensitivity target caps positive claim amounts at the 99.5th percentile of the training severity sample. This is not interpreted as a conventional direct improvement over the uncapped model because the response definition changes.

## 4.8 Relativities

With log links, exponentiated coefficients are interpreted as multiplicative relativities:

\[
Relativity = e^\beta.
\]

The estimates are associations conditional on included factors and are not interpreted causally.

## 4.9 Pure premium

Annual technical pure premium is:

\[
\widehat{PP}_i = \widehat{Frequency}_i \times \widehat{Severity}_i.
\]

This represents expected technical claim cost, not a final commercial premium.

## 4.10 Reproducibility

The final execution records the source hashes, random seed, sample counts, Git commit and software versions. The final run used Python 3.11.16, pandas 3.0.6, NumPy 2.4.6, scikit-learn 1.9.1 and statsmodels 0.15.0.

---

# 5. Results

## 5.1 Descriptive risk patterns

Drivers aged 18–25 have observed annual claim frequency of 0.1751, or 17.51 claims per 100 policy-years. Their average matched severity is 5,121.62, giving a frequency × severity benchmark of 896.64. By comparison, drivers aged 56–65 have frequency 0.0917, severity 1,890.11 and a benchmark of 173.33.

Bonus-Malus shows a strong monotonic frequency pattern. Annual frequency rises from 0.0802 in the <=50 band to 0.1133, 0.1582 and 0.3758 across the higher bands. Corresponding frequency × severity benchmarks are 154.10, 226.24, 533.08 and 765.88.

## 5.2 Frequency model

The primary Poisson GLM achieves held-out mean Poisson deviance of **0.321852** and aggregate test O/E of **1.0065**. Frequency-decile O/E ranges from approximately 0.924 to 1.134.

Training Pearson dispersion is **2.6058**, indicating material overdispersion.

### Key adjusted frequency relativities

| Factor | Relativity | 95% CI | p-value |
|---|---:|---:|---:|
| Bonus-Malus 51–75 vs <=50 | 1.596 | 1.548–1.645 | <0.001 |
| Bonus-Malus 76–100 vs <=50 | 2.249 | 2.166–2.335 | <0.001 |
| Bonus-Malus >100 vs <=50 | 5.290 | 4.955–5.648 | <0.001 |
| Vehicle age 3–5 vs 0–2 | 0.714 | 0.689–0.739 | <0.001 |
| Vehicle age 6–10 vs 0–2 | 0.764 | 0.739–0.791 | <0.001 |
| Vehicle age 11+ vs 0–2 | 0.606 | 0.584–0.628 | <0.001 |
| Regular vs diesel | 1.049 | 1.024–1.074 | <0.001 |
| Log density, one-unit increase | 1.039 | 1.010–1.069 | 0.007 |

The adjusted driver-age frequency pattern differs from the simple one-factor ranking, demonstrating the importance of multivariate adjustment.

## 5.3 Negative Binomial sensitivity

The method-of-moments Negative Binomial sensitivity model estimates alpha = **0.8596**, held-out mean NB deviance = **0.285208**, and aggregate O/E = **0.9953**. The result supports the conclusion that overdispersion is relevant.

## 5.4 Severity model

The primary Gamma model achieves held-out mean Gamma deviance of **1.884029**, MAE of **2,221.54**, and aggregate O/E of **0.9893**.

However, grouped calibration is substantially weaker. The lowest predicted-severity decile has observed mean severity 2,858.16 versus 1,213.07 predicted (O/E 2.356), while the highest decile has 2,119.81 observed versus 4,796.31 predicted (O/E 0.442).

### Driver-age severity relativities

| Driver-age band | Relativity vs 18–25 | 95% CI | p-value |
|---|---:|---:|---:|
| 26–35 | 0.456 | 0.337–0.616 | <0.001 |
| 36–45 | 0.411 | 0.301–0.563 | <0.001 |
| 46–55 | 0.434 | 0.315–0.598 | <0.001 |
| 56–65 | 0.457 | 0.321–0.650 | <0.001 |
| 66+ | 0.527 | 0.365–0.761 | <0.001 |

Bonus-Malus severity effects are much weaker than their frequency effects. The 76–100 severity relativity is 1.243 with 95% CI 0.991–1.558 (p=0.060), and the >100 severity coefficient is not statistically distinguishable from the <=50 reference at the 5% level.

## 5.5 Large-loss sensitivity

The 99.5th percentile training severity threshold is **32,043.36**. Under this capped sensitivity target, held-out Gamma deviance is **1.189936** and aggregate O/E is **1.0157**. The result demonstrates material upper-tail influence rather than proving that capping is the preferred production treatment.

## 5.6 Combined pure-premium diagnostic

Compared with matched historical loss amounts, overall pure-premium O/E is **0.7478**. Across deciles, O/E ranges from approximately 0.443 to 1.342. The highest predicted-risk decile has matched observed loss cost of 323.82 per policy-year versus 731.00 predicted.

Restricting the test to policies with exact agreement between frequency count and matched severity-row count gives O/E = **0.7577**. Source mismatch is therefore important but not the only explanation for combined-model error.

## 5.7 Performance summary

| Component | Held-out metric | Aggregate O/E | Additional diagnostic |
|---|---:|---:|---|
| Poisson frequency | Deviance 0.321852 | 1.0065 | Dispersion 2.6058 |
| Negative Binomial sensitivity | Deviance 0.285208 | 0.9953 | Alpha 0.8596 |
| Gamma severity | Deviance 1.884029 | 0.9893 | MAE 2,221.54 |
| Capped-severity sensitivity | Deviance 1.189936 | 1.0157 | Cap 32,043.36 |
| Combined pure-premium diagnostic | — | 0.7478 | Exact-match O/E 0.7577 |

---

# 6. Discussion

## 6.1 Main findings

The framework produces meaningful and transparent risk differentiation, but performance differs substantially across frequency and severity.

Bonus-Malus is the strongest adjusted frequency signal. Its effect persists after simultaneous control for the other included factors, suggesting that the one-factor Bonus-Malus pattern is not merely a composition effect. By contrast, its severity effects are much weaker. In this portfolio, Bonus-Malus differentiation is primarily a frequency phenomenon.

Driver age behaves differently. The youngest group shows both elevated descriptive frequency and very high severity, while the Gamma model estimates materially lower severity for every older group. Separate component modelling therefore reveals risk mechanisms that would be obscured in a single aggregate loss-cost number.

## 6.2 Relationship to actuarial literature

The empirical structure is consistent with the frequency–severity workflow described by Schirmacher (2016) and Tevet (2016). The results reinforce the interpretability advantage of modelling components separately.

At the same time, the diagnostics illustrate limitations anticipated by Noll et al. (2020): main-effects GLMs may fail to capture interactions automatically. The adjusted driver-age frequency pattern differs from the univariate ranking, illustrating how correlated risk variables can change interpretation after multivariate adjustment.

## 6.3 Overdispersion

The Poisson model is close to aggregate balance but clearly overdispersed. Good O/E therefore does not imply that the Poisson variance assumption is adequate. The Negative Binomial sensitivity result supports the use of more flexible count variance structures in future work.

## 6.4 Calibration beyond averages

The Gamma model's aggregate O/E of 0.9893 conceals substantial decile-level error. This supports the calibration emphasis of Denuit et al. (2021): global balance is necessary but insufficient.

For pricing, subgroup miscalibration matters because policies receiving similar modelled prices should not systematically generate very different observed experience.

## 6.5 Severity tail

Large claims materially affect severity model behaviour. The capped sensitivity should not be read as evidence that extreme claims should simply be removed; instead it shows that production modelling would require explicit treatment of tail risk.

## 6.6 Source mismatch and pure premium

The combined pure-premium model is more weakly calibrated against matched historical loss. The public source mismatch explains part of this difference, but the exact-match subset still materially overpredicts matched loss. Other contributors likely include omitted interactions, heavy-tailed severity, possible frequency–severity dependence and structural model error.

## 6.7 Frequency–severity dependence

Garrido et al. (2016) demonstrate that frequency and severity dependence can be accommodated. The present study retains the conventional separate baseline, but the combined calibration result makes explicit dependence a natural future extension.

## 6.8 Interpretability versus flexibility

The GLMs are transparent: multiplicative effects can be directly examined and challenged. This is valuable for governance. The cost is structural rigidity from banding and main effects. More flexible challengers should therefore be compared not only on predictive loss but on calibration, stability, explainability and fairness.

## 6.9 Answer to the research question

The evidence supports frequency–severity GLMs as a transparent and practically useful baseline for motor-insurance risk differentiation, especially for frequency. They are not sufficient as a complete production tariff because overdispersion, tail-sensitive severity, local miscalibration, source inconsistency and model-structure limitations remain material.

---

# 7. Limitations

The study is limited by the historical and geographically specific nature of freMTPL2; incomplete reconciliation between the frequency and severity files; random rather than temporal validation; Poisson overdispersion; heavy-tailed severity; fixed banding of several continuous variables; limited interactions; the conditional independence structure; limited challenger-model comparison; and the absence of a complete fairness or regulatory analysis.

The reported effects are statistical associations, not causal conclusions. The model estimates technical expected claim cost and does not include expenses, commissions, reinsurance, capital, profit, tax, competitive strategy or regulatory adjustments needed for commercial customer pricing.

---

# 8. Conclusion

This study evaluates an interpretable frequency–severity GLM framework using the freMTPL2 motor-insurance portfolio. An exposure-adjusted Poisson model is used for claim frequency and a Gamma log-link model for positive severity, with a shared policy-level 80:20 split and explicit calibration diagnostics.

The analysis identifies strong, explainable risk differentiation. Bonus-Malus is the clearest adjusted frequency predictor, while driver age is particularly important for severity. The frequency model is well balanced in aggregate, but its Pearson dispersion of 2.6058 indicates substantial overdispersion. The severity model is also close to aggregate balance but displays important decile-level miscalibration and sensitivity to large losses. The combined pure-premium model overpredicts matched historical loss, and validation is further complicated by known source-file inconsistency.

The research question can therefore be answered as follows:

> **Interpretable frequency–severity GLMs provide a transparent and useful baseline for motor-insurance risk differentiation, but additional work on overdispersion, tail risk, interactions, calibration, data reconciliation, frequency–severity dependence and commercial pricing considerations is required before production use.**

The principal value of the approach is its decomposability and auditability: it produces risk estimates whose assumptions, strengths and weaknesses can be inspected directly.

---

# 9. Future Research

Future research should prioritise Negative Binomial count modelling; direct Tweedie pure-premium models following the compound Poisson–Gamma tradition; generalized additive models for nonlinear continuous effects; carefully selected interactions; machine-learning challenger models; explainability methods; separate large-loss treatment; explicit frequency–severity dependence; temporal validation; inflation and claim-development adjustment; fairness analysis; and external validation on an independent motor portfolio.

---

# Declarations

## Data availability

The study uses the public freMTPL2 dataset family. The repository includes scripts for obtaining the public source files and records SHA-256 checksums for the exact files analysed. Raw source data are not redistributed in the repository.

## Code availability

Reproducible analysis code, model diagnostics and processed research outputs are maintained at:

https://github.com/ayushszode/motor-insurance-pricing-analytics

The publication-grade pipeline is research/research_pipeline.py and generated outputs are stored under research_outputs/.

## Ethics statement

No new human participants were recruited and no intervention was conducted. The analysis uses an existing public benchmark insurance dataset and does not rely on direct personal identifiers.

## Competing Interest Statement

Competing Interest: The author declares none.

## Funding Statement

This work received no specific grant from any funding agency, commercial or not-for-profit sectors.

## Author contribution

Ayush Sanjay Zode: conceptualisation, data analysis, methodology, software, validation, visualisation, interpretation and manuscript preparation.

---

# References

de Jong, P., & Heller, G. Z. (2008). *Generalized Linear Models for Insurance Data*. Cambridge University Press. https://doi.org/10.1017/CBO9780511755408

Denuit, M., Charpentier, A., & Trufin, J. (2021). Autocalibration and Tweedie-dominance for insurance pricing with machine learning. *Insurance: Mathematics and Economics, 101*(Part B), 485–497. https://doi.org/10.1016/j.insmatheco.2021.09.001

Dutang, C., & Charpentier, A. (2026). *CASdatasets: Insurance datasets* (R package version 1.2-1). https://doi.org/10.57745/P0KHAG

Garrido, J., Genest, C., & Schulz, J. (2016). Generalized linear models for dependent frequency and severity of insurance claims. *Insurance: Mathematics and Economics, 70*, 205–215. https://doi.org/10.1016/j.insmatheco.2016.06.006

Jørgensen, B., & Paes de Souza, M. C. (1994). Fitting Tweedie's compound Poisson model to insurance claims data. *Scandinavian Actuarial Journal, 1994*(1), 69–93. https://doi.org/10.1080/03461238.1994.10413930

Lindholm, M., Richman, R., Tsanakas, A., & Wüthrich, M. V. (2022). Discrimination-free insurance pricing. *ASTIN Bulletin, 52*(1), 55–89. https://doi.org/10.1017/asb.2021.23

Nelder, J. A., & Wedderburn, R. W. M. (1972). Generalized linear models. *Journal of the Royal Statistical Society: Series A (General), 135*(3), 370–384. https://doi.org/10.2307/2344614

Noll, A., Salzmann, R., & Wüthrich, M. V. (2020). *Case Study: French Motor Third-Party Liability Claims*. SSRN. https://doi.org/10.2139/ssrn.3164764

Schirmacher, E. (2016). Pure premium modeling using generalized linear models. In E. W. Frees, G. Meyers, & R. A. Derrig (Eds.), *Predictive Modeling Applications in Actuarial Science* (pp. 1–38). Cambridge University Press. https://doi.org/10.1017/CBO9781139342681.002

Tevet, D. (2016). Applying generalized linear models to insurance data: Frequency/severity versus pure premium modeling. In E. W. Frees, G. Meyers, & R. A. Derrig (Eds.), *Predictive Modeling Applications in Actuarial Science* (pp. 39–59). Cambridge University Press. https://doi.org/10.1017/CBO9781139342681.003

---

# Supplementary Research Outputs

The reported empirical results are supported by the following generated files:

- research_outputs/data_audit.json
- research_outputs/model_metrics.json
- research_outputs/modelling_sample_counts.csv
- research_outputs/frequency_coefficients.csv
- research_outputs/severity_coefficients.csv
- research_outputs/frequency_calibration.csv
- research_outputs/severity_calibration.csv
- research_outputs/pure_premium_calibration.csv
- research_outputs/consistency_analysis.csv
- research_outputs/sensitivity_results.csv
- research_outputs/driver_age_descriptive.csv
- research_outputs/bonus_malus_descriptive.csv
- research_outputs/figures/
