# Step 7 — Discussion

## 7.1 Interpretation of the main findings

This study examined whether an interpretable frequency–severity Generalized Linear Model framework could produce useful motor-insurance risk estimates and differentiated pure-premium indications from the freMTPL2 portfolio. The results support the value of this classical actuarial structure, but they also show clearly where a relatively simple GLM framework becomes limited.

The strongest and most stable result was found in the claim-frequency component. The Poisson model was close to aggregate balance on the held-out test sample, with an observed-to-expected claim ratio of approximately 1.01. In addition, Bonus-Malus showed a strong adjusted gradient after controlling for driver age, vehicle age, vehicle power, area, fuel type, region, vehicle brand and log-transformed population density. Relative to the <=50 category, the adjusted claim-frequency relativity increased to approximately 1.60 for Bonus-Malus 51–75, 2.25 for 76–100 and 5.29 for values above 100.

This result is substantively important because it indicates that Bonus-Malus is not merely associated with higher observed loss cost in a one-factor table; it remains strongly associated with expected claim frequency after simultaneous adjustment for the other included rating characteristics. In this portfolio, the Bonus-Malus effect appears to operate primarily through frequency rather than severity, because the corresponding Gamma-model severity coefficients were materially weaker and in some higher Bonus-Malus categories were not statistically distinguishable from the reference category at the conventional 5% level.

Driver age showed a different pattern. The descriptive analysis identified the 18–25 group as having both high claim frequency and very high average matched severity. In the multivariate Gamma model, every older driver-age category had materially lower expected severity relative to the 18–25 reference group. This supports the interpretation that young-driver risk in this portfolio is not only a question of how often claims occur, but also of the expected size of a positive claim. At the same time, the adjusted frequency relativities by age did not reproduce the simple one-factor ranking exactly. This difference reinforces the need to distinguish descriptive segmentation from multivariate model effects, since driver age is correlated with other policy and vehicle characteristics.

## 7.2 Relationship to established actuarial pricing practice

The overall modelling structure is consistent with the established actuarial frequency–severity approach in which claim counts and positive claim amounts are modelled separately and subsequently combined to form a pure-premium indication. Schirmacher describes this as a fundamental building block of insurance pricing and emphasises the complete modelling cycle from exploratory analysis through multivariate modelling, combination of frequency and severity, and validation. Tevet likewise describes the separate frequency/severity approach as a traditional actuarial method, while noting that direct pure-premium approaches such as Tweedie models provide an alternative formulation.

The present results support the continued usefulness of the separate-model approach because the two components behave differently. Bonus-Malus produced a very strong frequency effect but a much weaker severity pattern, while driver age showed a particularly strong severity signal. A single aggregate model would combine these mechanisms into one expected loss-cost estimate, whereas the frequency–severity structure makes it possible to see which component is driving the risk differentiation.

This interpretability is useful in actuarial work because the same overall pure-premium difference can arise through different mechanisms. A segment may be more expensive because claims occur more often, because claims are more severe, or because both components are elevated. The current results provide examples of all three possibilities and therefore illustrate one of the practical advantages of modelling the components separately.

## 7.3 Overdispersion and the limits of the Poisson assumption

Although the primary Poisson model was close to aggregate calibration, the training Pearson dispersion statistic was approximately 2.61, well above the value of 1 associated with the equidispersion assumption of the Poisson distribution. This indicates that the observed variance of claim counts is larger than the simple Poisson model assumes.

The Negative Binomial sensitivity analysis produced an aggregate observed-to-expected ratio close to 1.00 and explicitly allowed for additional variance through an estimated overdispersion parameter. These results do not invalidate the Poisson GLM as an interpretable baseline, but they do show that its distributional assumptions are restrictive for this portfolio.

The appropriate interpretation is therefore that the Poisson model provides a useful and transparent benchmark, while the evidence of overdispersion justifies considering a Negative Binomial or other more flexible count model in future development. The absolute Poisson and Negative Binomial deviances should not be treated as directly interchangeable model-selection scores because they arise from different assumed variance structures. Instead, the sensitivity model is evidence that overdispersion is a genuine feature of the data that should be considered in pricing-model specification and uncertainty assessment.

## 7.4 Calibration matters beyond a single headline metric

The results also demonstrate why insurance models should not be judged using only one portfolio-wide performance measure. The primary Gamma severity model achieved an aggregate observed-to-expected ratio close to 0.99, which would appear satisfactory if viewed in isolation. However, decile-level analysis revealed substantial local miscalibration: the model underpredicted severity in the lowest predicted-risk group and materially overpredicted severity in the highest predicted-risk group.

This is consistent with the broader actuarial literature on calibration. Denuit, Charpentier and Trufin emphasise that strong predictive performance does not automatically guarantee that fitted values remain balanced against observed experience, particularly across local regions of the portfolio. The current study reaches a similar practical conclusion from a classical GLM setting: aggregate balance can conceal meaningful subgroup-level miscalibration.

For pricing applications, this is important because a model that is correct on average can still create inappropriate relativities between risk groups. A portfolio-level O/E ratio near 1 should therefore be treated as a necessary but insufficient diagnostic. Grouped observed-versus-predicted analysis remains essential when deciding whether a model is suitable for tariff construction, portfolio monitoring or further refinement.

## 7.5 Severity tail risk

The severity analysis was substantially more difficult than the frequency analysis. Positive motor claim amounts are highly right-skewed, and the sensitivity analysis showed that the upper tail materially affected model fit. Capping claim amounts at the 99.5th percentile of the training severity sample produced a much lower Gamma deviance and an aggregate O/E ratio close to balance.

This finding should not be interpreted as evidence that large claims should simply be removed from a real insurance pricing model. Large claims are economically important and form part of genuine insurance risk. Instead, the sensitivity analysis demonstrates that a small number of extreme claims can have a disproportionate influence on severity modelling and that tail treatment needs to be an explicit modelling decision.

In production actuarial work, possible responses could include alternative severity distributions, robust modelling procedures, separate large-loss modelling, credibility approaches or reinsurance-aware treatment. The present study does not attempt to identify a definitive production solution. Its contribution is to show that tail behaviour is a material source of uncertainty in the freMTPL2 severity component and that conclusions based only on average model fit would understate this issue.

## 7.6 Pure-premium calibration and source-data inconsistency

The combined frequency × severity model produced a materially lower observed-to-expected ratio when compared against matched historical claim amounts than either component did in isolation. This result requires careful interpretation because the public frequency and severity files are not perfectly reconciled.

The frequency file contains 36,102 recorded claims, whereas only 26,444 positive severity rows could be matched to policies in the frequency table. In addition, 9,117 policies had a frequency claim count greater than the number of matched severity rows. The matched historical loss-cost diagnostic is therefore based on incomplete severity information relative to the frequency claim count.

For this reason, the frequency × severity result in this paper should be interpreted as an actuarial pure-premium indication rather than as an exact reconstruction of historical aggregate losses. The separate observed matched loss-cost measure is retained as a transparency diagnostic. Importantly, the consistent-subset sensitivity analysis still showed material overprediction, indicating that source inconsistency is not the only explanation. Model specification, severity-tail behaviour, unmodelled interactions and the independence assumption between frequency and severity are also plausible contributors.

## 7.7 Frequency–severity independence

The classical pure-premium calculation used in the study assumes that the expected frequency and expected positive severity can be modelled separately and then multiplied. This assumption is convenient and interpretable, but it is not guaranteed to hold in every insurance portfolio.

Garrido, Genest and Schulz show that claim frequency and severity may be dependent and present an extension in which the number of claims enters the severity model to capture this relationship. Their work demonstrates that the standard independence assumption can be relaxed within a GLM framework.

The current paper deliberately retains the simpler independent frequency–severity structure because the objective is to evaluate an interpretable baseline framework. However, the pure-premium calibration results indicate that dependence deserves consideration in future work. Testing whether policyholders with higher claim counts also have systematically different conditional claim severities would be a natural extension of the present analysis.

## 7.8 Interactions and model complexity

The use of grouped rating factors makes the fitted GLMs relatively easy to interpret, but this simplicity also constrains the relationships the models can represent. Noll, Salzmann and Wüthrich, using French motor third-party liability data, show that a simple GLM can fail to capture interactions between feature components that are more naturally handled by tree-based boosting or neural-network methods.

This is relevant to the present study because several risk variables are likely to interact. For example, the effect of driver age may differ by vehicle power, Bonus-Malus, region or vehicle age. The current specification models only main effects. Consequently, some of the grouped calibration error may arise because the same rating relativity is being applied across subgroups where the underlying relationship differs.

This does not make the GLM approach inappropriate. Rather, it defines the role of the model used here: an interpretable actuarial baseline whose assumptions and residual limitations can be investigated directly. More flexible machine-learning models could be used as challenger models in future work, but any predictive improvement would need to be weighed against interpretability, calibration and governance requirements.

## 7.9 Practical implications for insurance pricing

The findings have several practical implications.

First, frequency and severity should not be treated as interchangeable sources of loss-cost variation. The strong Bonus-Malus frequency effect and strong young-driver severity effect show that the source of pricing differentiation can vary materially by rating factor.

Second, aggregate model balance should always be supplemented with local calibration analysis. A model that appears well calibrated at portfolio level may still materially overprice or underprice particular risk groups.

Third, overdispersion in claim frequency and heavy-tailed severity are not minor technical details. They directly affect uncertainty, model fit and the stability of pricing indications.

Fourth, a technical pure premium is only one component of a commercial insurance price. A production tariff would additionally need to reflect expenses, commissions, reinsurance, capital requirements, profit margin, competitive positioning, underwriting strategy, regulation, fairness and governance. The models developed in this paper therefore represent expected claim-cost modelling rather than a complete commercial pricing system.

## 7.10 Answer to the research question

The main research question asked to what extent interpretable frequency–severity GLMs can estimate motor-insurance risk and produce differentiated pure-premium estimates across policyholder and vehicle characteristics in the freMTPL2 portfolio.

The results indicate that the framework is effective as an interpretable baseline for identifying and quantifying major risk differences, particularly in claim frequency. Bonus-Malus produced a strong and coherent adjusted frequency gradient, and the Gamma model identified substantial severity differences by driver age. The framework therefore succeeds in translating portfolio characteristics into transparent component-level risk estimates.

However, its performance is less convincing when judged as a complete pure-premium pricing system. The Poisson model exhibits material overdispersion, the severity model shows substantial decile-level miscalibration and sensitivity to large losses, and the combined pure-premium diagnostic overpredicts matched historical loss cost. The source frequency/severity mismatch further limits direct validation of aggregate historical loss cost.

Accordingly, the study supports frequency–severity GLMs as a transparent and useful actuarial starting point rather than as a final production tariff. Their principal strength lies in interpretability and decomposition of risk, while their principal limitations arise from distributional assumptions, tail behaviour, interaction structure, possible frequency–severity dependence and source-data quality.

## 7.11 Overall discussion

Taken together, the findings support a balanced view of classical actuarial GLMs. They are neither obsolete nor sufficient on their own for every modern pricing problem. In this study they provide clear risk relativities, strong aggregate frequency calibration and an explainable decomposition of loss cost. At the same time, the diagnostics expose important weaknesses that would be easy to miss if evaluation stopped at portfolio averages.

This is consistent with the role of GLMs in contemporary insurance analytics: they remain valuable interpretable benchmarks against which more flexible models can be assessed. The present study therefore contributes not by demonstrating that GLMs are universally superior, but by showing how a reproducible frequency–severity framework can be used to identify meaningful risk structure, diagnose its own limitations and establish a transparent baseline for further actuarial and machine-learning development.
