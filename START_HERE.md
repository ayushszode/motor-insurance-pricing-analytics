# Start Here

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Download the raw data

```bash
python src/download_data.py
```

## 3. Run the full analysis and models

```bash
python src/run_pipeline.py
```

This creates portfolio summaries, fitted Poisson/Gamma GLM metrics and model artifacts.

## 4. Open the notebook

```bash
jupyter notebook notebooks/Motor_Insurance_Pricing_Risk_Analytics.ipynb
```

## 5. Review the business output

- `excel/Motor_Insurance_Pricing_Model.xlsx`
- `images/insurance_pricing_dashboard.png`
- `docs/case_study.md`
- `docs/interview_guide.md`

The Excel workbook and included summary CSVs use verified full-dataset aggregate results. The GLM model results are generated locally when the pipeline is run because the raw data is intentionally not stored in this repository.
