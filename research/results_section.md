# Step 6 — Results

## 6.1 Data audit and modelling samples

The publication-grade pipeline retained all **678,013** valid frequency-policy records, representing **358,499.45 policy-years** of exposure and **36,102** claims in the frequency table. The severity source contained **26,639** positive claim rows, of which **26,444** could be matched to a policy in the frequency table; **195** severity rows had no matching policy identifier. The source files also contained a material count inconsistency: **9,117 policies** had a frequency claim count greater than the number of matched severity rows.

A single policy-level 80:20 split was used for both components of the frequency–severity framework. This produced **542,410 frequency training policies** and **135,603 frequency test policies**. The corresponding matched severity samples contained **21,044 training claim rows** and **5,400 test claim rows**. Because the split was performed at policy level, all claims belonging to the same policy remained in the same partition.

The portfolio-level annual claim frequency was **0.100703 claims per policy-year**, equivalent to **10.07 claims per 100 policy-years**. Average matched positive claim severity was **2,265.51** dataset currency units. The matched historical loss-cost diagnostic was **167.11 per policy-year**, while the frequency × matched-severity benchmark was **228.14 per policy-year**. These two quantities are reported separately because the frequency and severity source files are not perfectly aligned.

## 6.2 Descriptive risk patterns

### Driver age

The one-factor driver-age analysis showed substantial differences across age groups. Drivers aged **18–25** had the highest observed annual claim frequency at **0.1751**, or **17.51 claims per 100 policy-years**, compared with values of approximately 9–10 claims per 100 policy-years across most older groups. Their matched average severity was also considerably higher at **5,121.62**, producing a frequency × severity benchmark of **896.64 per policy-year**.

By comparison, the 56–65 group had an observed frequency of **0.0917**, matched average severity of **1,890.11**, and an indicated frequency × severity benchmark of **173.33**. These descriptive results identify a strong age-related risk signal, although the one-factor estimates do not isolate age from correlated rating characteristics.

### Bonus-Malus

Bonus-Malus displayed the clearest monotonic frequency pattern in the descriptive analysis. Annual claim frequency increased from **0.0802** for the <=50 group to **0.1133** for 51–75, **0.1582** for 76–100, and **0.3758** for >100. The corresponding frequency × severity benchmarks were **154.10**, **226.24**, **533.08**, and **765.88**, respectively.

The >100 segment therefore had substantially higher observed frequency and indicated pure-premium risk than the <=50 reference group, although its exposure base was much smaller.

## 6.3 Claim-frequency model

The primary Poisson GLM achieved a held-out **mean Poisson deviance of 0.321852**. Overall test-set calibration was close to balance, with an observed-to-expected (O/E) claim ratio of **1.0065**.

Calibration by predicted-frequency decile was generally reasonable but not perfect. O/E values ranged from approximately **0.924** to **1.134** across the ten risk groups. The highest predicted-risk decile had an observed annual frequency of **0.2100** compared with a predicted frequency of **0.2272**, indicating some overprediction at the extreme high-risk end. The eighth decile showed the reverse pattern, with observed frequency of **0.1442** versus predicted frequency of **0.1271**.

The estimated Pearson dispersion statistic on the training sample was **2.6058**, materially above 1. This indicates overdispersion relative to the Poisson variance assumption and provides a clear reason to examine an alternative count distribution.

### Frequency relativities

Relative to the <=50 Bonus-Malus reference category, the adjusted Poisson frequency relativities were:

- **51–75:** 1.596 (95% CI 1.548–1.645; p < 0.001)
- **76–100:** 2.249 (95% CI 2.166–2.335; p < 0.001)
- **>100:** 5.290 (95% CI 4.955–5.648; p < 0.001)

This indicates that Bonus-Malus remained a strong frequency predictor after controlling for the other included rating factors.

Relative to vehicles aged 0–2 years, adjusted frequency relativities were lower for older vehicle groups:

- **3–5 years:** 0.714 (95% CI 0.689–0.739; p < 0.001)
- **6–10 years:** 0.764 (95% CI 0.739–0.791; p < 0.001)
- **11+ years:** 0.606 (95% CI 0.584–0.628; p < 0.001)

For driver age, the 18–25 group was the reference category. The 26–35 group had a lower adjusted frequency relativity of **0.730** (95% CI 0.693–0.769; p < 0.001). The 46–55 and 66+ categories had relativities above 1 relative to the 18–25 baseline after simultaneous adjustment, demonstrating that the multivariate age pattern differs from the simple one-factor ranking and should be interpreted jointly with the remaining covariates.

Regular fuel was associated with a modestly higher frequency relativity of **1.049** relative to diesel (95% CI 1.024–1.074; p < 0.001). The coefficient on log-transformed density corresponded to a relativity of **1.039** per one-unit increase in log(1 + density) (95% CI 1.010–1.069; p = 0.007).

## 6.4 Negative Binomial frequency sensitivity

The method-of-moments Negative Binomial sensitivity model estimated an overdispersion parameter of **0.8596**. Its held-out mean Negative Binomial deviance was **0.285208**, with an O/E ratio of **0.9953**.

Because Poisson and Negative Binomial deviances are defined under different variance functions, their absolute deviance values are not treated as a direct like-for-like model-selection score. Nevertheless, the dispersion estimate and balanced O/E result support the conclusion that overdispersion is a relevant feature of the claim-count data and should be acknowledged when interpreting the primary Poisson model.

## 6.5 Claim-severity model

The primary Gamma GLM achieved a held-out **mean Gamma deviance of 1.884029** and a test-set **MAE of 2,221.54**. At the aggregate test-set level, severity calibration was close to balance, with an O/E ratio of **0.9893**.

However, grouped calibration revealed substantial heterogeneity. In the lowest predicted-severity decile, observed mean severity was **2,858.16** compared with a prediction of **1,213.07** (O/E = **2.356**). In the highest predicted-severity decile, observed mean severity was **2,119.81** compared with **4,796.31** predicted (O/E = **0.442**). The middle deciles were considerably closer to balance.

These results show that satisfactory aggregate calibration can conceal meaningful miscalibration across the predicted-risk distribution.

### Severity relativities

Driver age was the clearest stable signal in the Gamma model. Relative to the 18–25 reference category, all older driver-age groups had materially lower predicted severity:

- **26–35:** relativity 0.456 (95% CI 0.337–0.616; p < 0.001)
- **36–45:** 0.411 (95% CI 0.301–0.563; p < 0.001)
- **46–55:** 0.434 (95% CI 0.315–0.598; p < 0.001)
- **56–65:** 0.457 (95% CI 0.321–0.650; p < 0.001)
- **66+:** 0.527 (95% CI 0.365–0.761; p < 0.001)

By contrast, the primary Bonus-Malus severity coefficients were much weaker than the corresponding frequency effects. For example, the 76–100 group had a severity relativity of **1.243**, but its 95% confidence interval included 1 (0.991–1.558; p = 0.060). The >100 coefficient was also not statistically distinguishable from the reference category at the 5% level.

This suggests that the strong Bonus-Malus pure-premium gradient in this portfolio is driven primarily by claim frequency rather than a stable monotonic severity effect.

## 6.6 Large-loss sensitivity

Claim severity was strongly influenced by the upper tail. A sensitivity analysis capped claim amounts at the **99.5th percentile of the training severity sample**, equal to **32,043.36**. Under this capped target definition, held-out Gamma deviance was **1.189936** and aggregate O/E was **1.0157**.

The capped result is not directly comparable with the uncapped model as a conventional model-selection test because the response variable itself is altered. Instead, the sensitivity analysis demonstrates that extreme claims materially affect severity-model fit and calibration. This tail dependence should therefore be recognised explicitly in the interpretation of the severity model.

## 6.7 Combined pure-premium diagnostic

Predicted annual pure premium was calculated as predicted annual claim frequency multiplied by predicted positive claim severity.

When this prediction was compared with matched historical claim amounts in the test sample, the overall matched-loss O/E ratio was **0.7478**. In other words, the matched historical losses represented about 74.8% of the model-implied loss amount under this diagnostic.

Calibration across pure-premium deciles was uneven. O/E ranged from approximately **0.443** to **1.342**, with the highest predicted-risk decile showing an observed matched loss cost of **323.82** per policy-year compared with a predicted loss cost of **731.00**.

This combined calibration result must be interpreted in the context of the known source-data inconsistency: the frequency file reports more claims than can be reconstructed from the severity file. The pure-premium model is therefore treated as an actuarial frequency–severity indication rather than as a perfectly reconciled reconstruction of historical portfolio loss cost.

A sensitivity check restricted to policies with exact agreement between frequency claim count and matched severity-row count produced an O/E ratio of **0.7577**, indicating that the mismatch is not the only source of combined-model calibration error. The remaining difference reflects model specification, severity-tail behaviour, and the distinction between separate conditional frequency/severity models and realised matched historical losses.

## 6.8 Summary of empirical findings

Four results are particularly important.

First, **Bonus-Malus is the strongest adjusted frequency signal** in the primary GLM, with frequency relativity increasing sharply across higher bands.

Second, **young-driver risk is expressed strongly through claim severity**. The descriptive analysis shows elevated frequency and severity for drivers aged 18–25, while the multivariate Gamma model estimates materially lower severity for every older age group relative to this baseline.

Third, **the Poisson frequency model is well balanced in aggregate but overdispersed**, supporting the use of a Negative Binomial specification as an important sensitivity analysis.

Fourth, **severity and combined pure-premium calibration are more challenging than frequency calibration**. Aggregate severity O/E is close to 1, but decile-level results reveal substantial miscalibration, especially in the tails. The combined pure-premium diagnostic also materially overpredicts matched historical loss cost. These results argue against interpreting the fitted models as a production-ready commercial tariff and instead support their use as a transparent empirical pricing framework whose strengths and limitations can be examined explicitly.
