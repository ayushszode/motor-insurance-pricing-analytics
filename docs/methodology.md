# Methodology

## 1. Data validation

- Confirm required columns.
- Remove non-positive exposure rows from modelling.
- Restrict severity modelling to positive claim amounts.
- Link claim amounts to policy attributes through `IDpol`.

## 2. Feature engineering

Interpretable bands are used for portfolio reporting and GLM stability:

- Driver age: 18–25, 26–35, 36–45, 46–55, 56–65, 66+
- Vehicle age: 0–2, 3–5, 6–10, 11+
- Bonus-Malus: <=50, 51–75, 76–100, >100
- Vehicle power: 4–6, 7–9, 10+

Area, fuel type and region remain categorical.

## 3. Frequency

Annualised observed frequency:

`sum(ClaimNb) / sum(Exposure)`

Model:

- Poisson GLM
- log link
- offset = `log(Exposure)`

## 4. Severity

Observed severity:

`sum(ClaimAmount) / number of severity claim rows`

Model:

- Gamma GLM
- log link
- positive claims only

## 5. Pure premium

`Expected Frequency × Expected Severity`

The project distinguishes this actuarial indicated pure premium from the simple observed matched loss cost `matched claim amount / exposure` because the severity table contains fewer claim rows than the total frequency claim count.

## 6. Model evaluation

The Python pipeline reports:

- mean Poisson deviance on a held-out frequency set
- mean Gamma deviance on a held-out severity set
- risk-tier summaries based on predicted pure premium

## 7. Commercial premium

The Excel calculator optionally demonstrates commercial loadings. These assumptions are deliberately separated from the technical pure premium and are not presented as observed insurer inputs.
