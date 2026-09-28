# Case Study — Motor Insurance Pricing & Risk Analytics

## Situation

Motor insurers need prices that reflect expected claims while remaining explainable and operationally usable. The freMTPL2 dataset provides policy exposure, claims, driver/vehicle characteristics and claim amounts suitable for a frequency-severity pricing study.

## Task

Build an interpretable pricing workflow that:

1. measures portfolio claim frequency and severity,
2. identifies higher- and lower-risk rating-factor segments,
3. calculates an indicated pure-premium benchmark,
4. supports a multivariate Poisson/Gamma modelling workflow,
5. communicates results through Excel and concise management outputs.

## Approach

- Validated policy and claim tables and linked them through `IDpol`.
- Created transparent bands for driver age, vehicle age, Bonus-Malus and vehicle power.
- Calculated exposure-weighted claim frequency.
- Calculated conditional claim severity from positive claims.
- Combined frequency and severity to estimate indicated pure premium.
- Prepared a Poisson GLM with exposure offset for frequency and Gamma GLM with log link for severity.
- Built portfolio segment tables and an Excel management workbook.

## Verified portfolio results

- 678,013 policies and 358,499.45 policy-years of exposure.
- 36,102 frequency claims, equivalent to 10.07 claims per 100 policy-years.
- Average matched claim severity: 2,265.51.
- Portfolio indicated pure premium: 228.14 per policy-year.
- Driver age 18–25: indicated pure premium 896.64, or 3.93x the portfolio benchmark.
- Bonus-Malus >100: 37.58 claims per 100 policy-years and indicated pure premium 765.88.

## Business interpretation

The portfolio shows strong differentiation by driver age and Bonus-Malus. These factors would merit particular attention in multivariate pricing and underwriting review. However, one-factor tables do not isolate causal effects; the GLM stage is therefore important for estimating relativities after controlling for other rating factors.

## Recommendation

Use the portfolio segmentation as an initial diagnostic, then base technical pricing decisions on validated multivariate models. Add commercial loadings only after reviewing expenses, commission, reinsurance, capital requirements, competitive position and governance constraints.
