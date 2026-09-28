# Motor Insurance Pricing & Risk Analytics

End-to-end actuarial pricing portfolio project using **Python, Excel and statistical modelling** on the French Motor Third-Party Liability **freMTPL2** dataset.

The project separates insurance pricing into the two classical components:

- **Claim frequency** — how often claims are expected to occur.
- **Claim severity** — how expensive a claim is expected to be when it occurs.

The pricing relationship is:

> **Indicated Pure Premium = Expected Claim Frequency × Expected Claim Severity**

The repository combines full-portfolio descriptive analysis, rating-factor segmentation, an Excel pricing workbook and reproducible Python code for Poisson/Gamma GLMs.

## Business objective

A motor insurer needs to charge prices that reflect expected risk while remaining explainable to underwriters and commercial stakeholders. This project asks:

1. Which customer and vehicle characteristics are associated with higher claim frequency?
2. Which segments have higher claim severity?
3. How can frequency and severity be combined into a pure-premium benchmark?
4. How can an interpretable actuarial model support portfolio segmentation and pricing decisions?

## Dataset

**freMTPL2 French Motor Third-Party Liability**

- Frequency table: **678,013 policy records**
- Severity table: **26,639 claim rows**
- Key frequency fields: `IDpol`, `ClaimNb`, `Exposure`, `VehPower`, `VehAge`, `DrivAge`, `BonusMalus`, `VehBrand`, `VehGas`, `Area`, `Density`, `Region`
- Severity fields: `IDpol`, `ClaimAmount`

Source documentation:
https://dutangc.github.io/CASdatasets/reference/freMTPL.html

Convenient mirror:
https://huggingface.co/datasets/mabilton/fremtpl2

Raw data is not committed to this repository. See `data/README.md`.

## Verified full-dataset portfolio snapshot

The aggregate tables under `data/processed/` were computed from the complete frequency and severity files.

| Metric | Result |
|---|---:|
| Policies | 678,013 |
| Total exposure | 358,499.45 policy-years |
| Frequency claims | 36,102 |
| Claim frequency | 0.1007 claims per policy-year |
| Claims per 100 policy-years | 10.07 |
| Policies with >=1 claim | 5.02% |
| Severity rows | 26,639 |
| Matched severity rows | 26,444 |
| Average matched claim severity | 2,265.51 dataset currency units |
| Observed loss cost from matched severity rows | 167.11 per policy-year |
| **Indicated pure premium** | **228.14 per policy-year** |

> The indicated pure premium uses the classical frequency × severity relationship. The severity file has fewer claim rows than the total `ClaimNb` count in the frequency table, so `total matched claim amount / exposure` is shown separately as an observed loss-cost diagnostic rather than treated as the actuarial pure premium.

## Key portfolio insights

### Driver age

The **18–25** segment has the strongest observed risk signal in the age analysis:

- Claim frequency: **17.51 per 100 policy-years**
- Average severity: **5,121.62**
- Indicated pure premium: **896.64**
- Pure-premium relativity: **3.93x** the portfolio benchmark

By comparison, the 56–65 band has an indicated pure premium of **173.33**.

### Bonus-Malus

Risk rises materially as Bonus-Malus increases:

| Bonus-Malus band | Claim rate / 100 | Avg severity | Indicated pure premium | Relativity |
|---|---:|---:|---:|---:|
| <=50 | 8.02 | 1,922.22 | 154.10 | 0.68x |
| 51–75 | 11.33 | 1,997.27 | 226.24 | 0.99x |
| 76–100 | 15.82 | 3,369.93 | 533.08 | 2.34x |
| >100 | 37.58 | 2,038.16 | 765.88 | 3.36x |

### Other signals

- Newer vehicles aged **0–2** show higher frequency than older vehicle groups.
- Area-level risk varies: Area B has the highest indicated pure premium in the one-factor area view, driven primarily by higher observed severity.
- Regular-fuel vehicles show a higher one-factor pure-premium benchmark than diesel vehicles in this portfolio.

These are **univariate portfolio signals**, not causal conclusions. The GLM pipeline is included to control for multiple rating factors simultaneously.

## Modelling approach

### Frequency model

- Poisson GLM
- Log link
- `log(Exposure)` offset
- Rating factors: driver-age band, vehicle-age band, Bonus-Malus band, vehicle-power band, area, fuel and region

### Severity model

- Gamma GLM
- Log link
- Positive claims only
- Same interpretable rating-factor set

### Pure premium

For each policy:

```text
Predicted Pure Premium = Predicted Annual Claim Frequency × Predicted Claim Severity
```

The models are deliberately interpretable because pricing teams often need to explain rate relativities and model behaviour to underwriters, governance teams and regulators.

## Repository structure

```text
motor_insurance_pricing_analytics/
├── README.md
├── START_HERE.md
├── requirements.txt
├── LICENSE
├── DATA_LICENSE_NOTICE.md
├── data/
│   ├── README.md
│   ├── raw/                     # downloaded locally; excluded from Git
│   └── processed/               # verified aggregate portfolio outputs
├── notebooks/
│   └── Motor_Insurance_Pricing_Risk_Analytics.ipynb
├── src/
│   ├── config.py
│   ├── download_data.py
│   ├── analysis.py
│   ├── modeling.py
│   └── run_pipeline.py
├── sql/
│   └── portfolio_analysis.sql
├── excel/
│   └── Motor_Insurance_Pricing_Model.xlsx
├── images/
│   └── insurance_pricing_dashboard.png
├── docs/
│   ├── case_study.md
│   ├── methodology.md
│   ├── data_dictionary.md
│   ├── interview_guide.md
│   ├── linkedin_entry.md
│   └── cv_bullets.md
└── models/                      # generated locally
```

## How to run

```bash
pip install -r requirements.txt
python src/download_data.py
python src/run_pipeline.py
```

Or open the notebook after downloading the data:

```bash
jupyter notebook notebooks/Motor_Insurance_Pricing_Risk_Analytics.ipynb
```

## Excel deliverable

The workbook contains:

- portfolio KPI summary
- rating-factor segment analysis
- pure-premium relativity tables
- an **illustrative pricing calculator** based on portfolio relativities
- transparent assumptions for expenses/profit loadings

The calculator is an educational benchmark and is intentionally labelled as such; the fitted GLMs are the more appropriate multivariate pricing method.

## Limitations

- freMTPL2 is historical French motor TPL data and should not be treated as representative of a current UK insurance book.
- One-factor relativities can be confounded by other rating factors.
- The severity file contains fewer rows than the claim count in the frequency table, so observed loss cost and frequency × severity are both reported transparently.
- Commercial pricing requires expenses, commission, reinsurance, capital, competitive positioning, governance and regulatory review beyond pure premium.
- This project is for portfolio and educational purposes, not a production pricing engine.

## Skills demonstrated

**Insurance Pricing | Actuarial Analytics | Python | Excel | SQL | Poisson GLM | Gamma GLM | Risk Segmentation | Model Validation | Data Analysis | Business Communication**
