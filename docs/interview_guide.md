# Interview Guide

## 30-second project explanation

“I built a motor insurance pricing and risk analytics project using the freMTPL2 French motor third-party liability dataset. I separated pricing into claim frequency and claim severity, analysed risk by factors such as driver age and Bonus-Malus, and combined the two into an indicated pure premium. I also prepared a Poisson GLM for frequency with an exposure offset and a Gamma GLM for severity, because those are interpretable approaches commonly used in non-life pricing. I then presented the results through an Excel pricing workbook and portfolio dashboard.”

## Why frequency × severity?

Frequency answers how often claims occur. Severity answers how expensive a claim is when it occurs. Multiplying the expected values gives the expected annual claim cost, or technical pure premium.

## Why Poisson GLM?

Claim counts are non-negative count data. A Poisson GLM with a log link allows expected claim counts to remain positive, while the exposure offset adjusts for different policy observation periods.

## Why Gamma GLM?

Positive claim amounts are continuous, right-skewed and heteroscedastic. A Gamma distribution with log link is a common interpretable starting point for severity modelling.

## Strong finding to discuss

The 18–25 driver-age segment had an indicated one-factor pure premium of 896.64, around 3.93x the portfolio benchmark. Bonus-Malus also showed a strong gradient, with the >100 band at 37.58 claims per 100 policy-years.

## Important limitation to mention

The one-factor segment tables are descriptive and can be confounded. They should not be used as final rate factors without multivariate modelling, validation and governance review.

## If asked about the severity/frequency row mismatch

The frequency table records 36,102 claims in total, while the severity file contains 26,639 claim rows and 26,444 matched rows after joining. I therefore report observed matched loss cost separately and use frequency × conditional average severity as the indicated pure-premium benchmark. The mismatch is made explicit rather than silently forcing the tables to agree.

## What would you improve next?

- Compare Poisson with Negative Binomial / quasi-Poisson for dispersion.
- Add continuous smooth terms or monotonic constraints.
- Compare GLM with gradient boosting while retaining explainability.
- Add calibration/lift charts and stability testing.
- Include commercial expense, commission, reinsurance and capital assumptions from a real insurer if available.
