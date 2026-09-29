# Step 8 — Limitations, Conclusion and Future Research

## 8.1 Limitations

This study has several limitations that are important when interpreting the results.

### 8.1.1 Historical and geographically specific dataset

The analysis is based on the freMTPL2 French Motor Third-Party Liability dataset. The portfolio is historical and reflects a specific insurance market, underwriting environment and regulatory context. The findings therefore should not be interpreted as directly representative of a current UK motor-insurance portfolio or of present-day commercial pricing conditions.

Risk relationships can change over time because of changes in vehicle technology, road use, inflation, claims management, repair costs, legislation, underwriting practice and customer behaviour. The estimated relativities in this paper should therefore be interpreted as empirical relationships within the analysed dataset rather than universally transferable tariff factors.

### 8.1.2 Frequency and severity source-data inconsistency

The frequency and severity source files are not perfectly reconciled. The frequency table contains **36,102** recorded claims, while only **26,444** positive severity records can be matched to policies in the frequency table. In addition, **195** positive severity rows have no matching policy record, and **9,117 policies** have a frequency claim count greater than the number of matched severity rows.

This prevents a complete reconstruction of observed historical portfolio loss cost from the two source files. Consequently, the study reports both a matched historical loss-cost diagnostic and a separate frequency × severity benchmark. The latter should be interpreted as an actuarial indication rather than an exact reproduction of all realised losses.

### 8.1.3 Random rather than temporal validation

The dataset does not provide a suitable policy-level temporal variable that supports a robust chronological train-test split. The study therefore uses a reproducible **80:20 policy-level random split** with a fixed random seed.

Although the split prevents the same policy from appearing in both training and test sets, it does not test performance under genuine temporal drift. A production pricing model should ideally be validated on future periods because risk relationships, inflation and portfolio composition may change over time.

### 8.1.4 Poisson overdispersion

The primary frequency model uses a Poisson GLM because of its transparency and established actuarial interpretation. However, the estimated Pearson dispersion statistic was approximately **2.61**, indicating that claim-count variance is materially larger than the Poisson assumption allows.

The Negative Binomial sensitivity analysis partially addresses this limitation by allowing additional variance. Nevertheless, the primary model should be understood as an interpretable baseline rather than a complete representation of the claim-count distribution.

### 8.1.5 Heavy-tailed claim severity

Positive claim amounts are strongly right-skewed and include extreme losses. The severity model is therefore sensitive to the upper tail of the distribution. A 99.5th-percentile capping sensitivity analysis materially changed model fit, demonstrating the influence of extreme claims.

Large losses should not automatically be removed because they represent genuine insurance risk. A more advanced actuarial application may require explicit large-loss modelling, alternative severity distributions, robust estimation, reinsurance treatment or separate attritional and large-loss components.

### 8.1.6 Limited interaction modelling

The fitted GLMs primarily use main effects. Although the model controls for several rating factors simultaneously, it does not systematically model interactions such as:

- driver age × vehicle power
- driver age × Bonus-Malus
- region × population density
- vehicle age × vehicle brand
- Bonus-Malus × area

If such relationships are important, the current specification may average across materially different subgroups and contribute to the observed calibration error.

### 8.1.7 Banded continuous variables

Driver age, vehicle age, Bonus-Malus and vehicle power are grouped into interpretable bands. This improves clarity and can stabilise estimation, but it also creates artificial boundaries and discards within-band information.

For example, two drivers immediately either side of an age-band threshold may receive different model effects despite having very similar underlying risk characteristics. Alternative approaches such as splines, polynomial terms or monotonic smooth functions may capture continuous relationships more naturally.

### 8.1.8 Frequency–severity independence assumption

The study models frequency and severity separately and combines their conditional expectations through multiplication. This conventional approach implicitly assumes that the two components can be treated independently conditional on the included rating factors.

Previous actuarial research has shown that claim frequency and severity may be dependent in some portfolios. The present study does not estimate a joint dependence structure, so unmodelled dependence may contribute to pure-premium calibration error.

### 8.1.9 Calibration limitations

The Poisson model is well balanced in aggregate, while the Gamma severity model has an aggregate O/E ratio close to 1. However, grouped calibration reveals materially larger deviations across risk deciles, particularly in the severity and combined pure-premium models.

This means that a favourable portfolio-level calibration statistic should not be interpreted as evidence that every subgroup is accurately priced.

### 8.1.10 No direct comparison with a full set of challenger models

The paper focuses deliberately on interpretable GLMs. Apart from the Negative Binomial frequency sensitivity analysis, the study does not benchmark the final framework against a broad set of alternative models such as:

- Tweedie GLMs
- gradient boosting
- random forests
- neural networks
- generalized additive models
- zero-inflated or hurdle models

The study therefore cannot conclude that the selected GLMs are the most accurate possible predictive models. Their value in this work lies primarily in transparency, interpretability and actuarial relevance.

### 8.1.11 Pure premium is not commercial premium

The models estimate expected technical claim cost. They do not estimate the final premium that an insurer would charge a customer.

A commercial premium may also incorporate:

- acquisition costs
- administration expenses
- commission
- reinsurance
- capital requirements
- profit margin
- insurance premium tax
- underwriting strategy
- competitive positioning
- regulatory constraints
- fairness considerations
- credibility adjustments

The results should therefore not be interpreted as customer-facing prices.

### 8.1.12 No causal interpretation

The relationships identified by the models are statistical associations. For example, a higher Bonus-Malus band being associated with greater claim frequency does not imply that Bonus-Malus itself causes claims. Similarly, observed differences across driver-age, vehicle or geographic groups should not be interpreted as causal effects.

The study is designed for predictive risk segmentation rather than causal inference.

### 8.1.13 Fairness and governance are outside the primary empirical scope

Insurance rating variables may raise legal, ethical and fairness considerations. The current research focuses on statistical modelling and does not conduct a complete fairness audit, regulatory assessment or protected-characteristic analysis.

A production implementation would require formal governance, legal review, fairness testing, documentation and ongoing monitoring in the relevant jurisdiction.

---

# 8.2 Conclusion

This study investigated whether an interpretable frequency–severity Generalized Linear Model framework could estimate motor-insurance risk and produce differentiated pure-premium indications using the freMTPL2 portfolio.

The analysis combined descriptive portfolio segmentation with an exposure-adjusted **Poisson GLM for claim frequency** and a **Gamma GLM with log link for positive claim severity**. Expected annual pure premium was then calculated as the product of predicted annual claim frequency and predicted conditional severity.

The empirical results demonstrate that the framework is useful for identifying and explaining meaningful differences in insurance risk. Bonus-Malus emerged as the clearest adjusted frequency predictor. Relative to the <=50 group, the estimated frequency relativity increased to approximately **1.60** for Bonus-Malus 51–75, **2.25** for 76–100 and **5.29** for values above 100. Driver age showed a different pattern: the youngest drivers displayed particularly high observed severity, and the multivariate Gamma model estimated materially lower severity for all older age categories relative to the 18–25 reference group.

The primary Poisson model achieved strong aggregate frequency calibration, with a held-out O/E ratio close to **1.01**. However, a Pearson dispersion statistic of approximately **2.61** demonstrated substantial overdispersion, justifying the Negative Binomial sensitivity analysis. The severity model was also close to aggregate balance, with an O/E ratio near **0.99**, but decile-level diagnostics revealed significant local miscalibration and strong sensitivity to large losses.

The combined pure-premium analysis was more challenging. Predicted pure premiums did not reconcile closely with matched historical loss cost, and this difference was influenced by both model limitations and known inconsistency between the public frequency and severity source files. The results therefore reinforce the importance of separating modelled actuarial indications from observed matched loss-cost diagnostics.

Overall, the research question can be answered as follows:

> **Interpretable frequency–severity GLMs can provide a transparent and practically useful baseline for motor-insurance risk differentiation, particularly for identifying and explaining claim-frequency and claim-severity drivers. However, the framework should not be treated as a complete production pricing solution without additional treatment of overdispersion, severity tails, interaction effects, frequency–severity dependence, local calibration, data quality and commercial pricing considerations.**

The principal contribution of the study is therefore not a claim that classical GLMs outperform all alternatives. Instead, it demonstrates how a reproducible actuarial frequency–severity workflow can convert a large public motor-insurance dataset into transparent risk estimates while simultaneously exposing the limitations that would need to be addressed before operational use.

---

# 8.3 Future Research

The limitations identified in this study provide several clear directions for future work.

### 8.3.1 Negative Binomial and alternative frequency distributions

The observed overdispersion suggests that future work should examine the Negative Binomial model more extensively as a primary rather than sensitivity specification. Additional count models could include:

- quasi-Poisson
- zero-inflated Poisson
- zero-inflated Negative Binomial
- hurdle models

These approaches could be evaluated using held-out calibration, deviance and stability across risk groups.

### 8.3.2 Direct Tweedie pure-premium modelling

A natural extension is to model aggregate loss cost directly using a Tweedie GLM. The Tweedie distribution can accommodate the mixture of zero losses and positive continuous claim costs within one modelling framework.

Future research could compare:

1. separate Poisson + Gamma frequency–severity models;
2. direct Tweedie pure-premium modelling.

The comparison should consider not only predictive accuracy but also calibration, interpretability and stability.

### 8.3.3 Generalized Additive Models

Generalized Additive Models could reduce the need to impose fixed bands on variables such as:

- driver age
- vehicle age
- Bonus-Malus
- population density

Smooth functions could capture nonlinear relationships while remaining more interpretable than many black-box machine-learning models.

### 8.3.4 Interaction effects

Future work should test whether meaningful interactions improve calibration without creating an excessively complex tariff.

Priority interactions could include:

- DriverAge × BonusMalus
- DriverAge × VehiclePower
- VehicleAge × VehicleBrand
- Area × LogDensity
- BonusMalus × Region

Interaction selection should be based on actuarial reasoning and out-of-sample evidence rather than data-mining alone.

### 8.3.5 Machine-learning challenger models

The GLM framework can serve as an interpretable benchmark against which more flexible models are evaluated.

Possible challengers include:

- Gradient Boosting Machines
- XGBoost / LightGBM
- Random Forests
- Explainable Boosting Machines
- Neural Networks

The goal should not simply be to maximise a single predictive metric. Models should be compared on:

- out-of-sample deviance
- calibration
- ranking/discrimination
- stability
- interpretability
- operational complexity

### 8.3.6 Explainable machine learning

If machine-learning models improve predictive performance, methods such as:

- SHAP values
- partial dependence
- accumulated local effects
- feature importance
- individual prediction explanations

could be used to compare their implied risk relationships with traditional GLM relativities.

This would create a useful bridge between actuarial interpretability and modern predictive modelling.

### 8.3.7 Large-loss modelling

Because severity results are highly sensitive to the upper tail, future research could separate claims into:

1. attritional claims;
2. large losses.

Potential methods include:

- threshold-based models
- Generalized Pareto distributions
- extreme-value methods
- separate large-loss frequency/severity models
- reinsurance-adjusted loss modelling

This may provide a more realistic treatment of severe claims than simple capping.

### 8.3.8 Frequency–severity dependence

Future work should explicitly test whether claim frequency and conditional severity are dependent after controlling for policy characteristics.

Possible approaches include:

- including claim count in the severity model;
- copula-based joint modelling;
- shared random-effects models;
- hierarchical frequency–severity models.

This could help determine whether the conventional independence assumption contributes materially to pure-premium miscalibration.

### 8.3.9 Temporal validation

If a dataset containing reliable policy inception, renewal or accident dates becomes available, the modelling framework should be re-evaluated using a chronological validation design.

For example:

> Train on earlier underwriting periods → Test on later periods.

This would provide stronger evidence of model robustness under portfolio and economic change.

### 8.3.10 Inflation and claim-cost development

A modern pricing study should consider whether historical claims need adjustment for:

- claims inflation
- repair-cost inflation
- wage inflation
- medical inflation
- settlement delay
- claims development

Incorporating such adjustments would make severity estimates more relevant to future expected claim cost.

### 8.3.11 Fairness and responsible pricing

Future research should evaluate whether model outcomes differ systematically across sensitive or potentially proxy-related groups and whether any differences are legally and ethically appropriate.

Possible analyses include:

- group calibration
- error-rate comparisons
- disparate-impact diagnostics
- proxy-variable assessment
- fairness-constrained modelling

Such work would need to be interpreted within the applicable insurance regulatory environment.

### 8.3.12 External validation

The most valuable extension would be to test the same modelling framework on a second independent motor-insurance portfolio.

External validation would help determine which findings are specific to freMTPL2 and which relationships remain stable across different insurers, markets and time periods.

---

# 8.4 Final Research Position

The completed analysis supports a clear final position:

> **The classical frequency–severity GLM framework remains highly useful when transparency, decomposability and actuarial interpretation are priorities. Its value is greatest as an explainable baseline and governance-friendly benchmark. For production pricing, however, it should be complemented by stronger treatment of overdispersion, heavy-tailed severity, interactions, calibration, data reconciliation, fairness and alternative predictive models.**

This conclusion is deliberately narrower than claiming that the fitted model is a complete insurance-pricing engine. It reflects the actual empirical evidence generated in this study and provides a defensible foundation for both academic publication and future model development.
