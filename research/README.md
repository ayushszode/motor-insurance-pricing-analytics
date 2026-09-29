# Research pipeline

This directory contains the publication-grade modelling workflow for the research paper:

**Interpretable Motor Insurance Pricing with Frequency-Severity Generalized Linear Models: Evidence from the freMTPL2 Portfolio**

## What this pipeline changes relative to the portfolio model

- Uses one reproducible **policy-level 80:20 split** for both frequency and severity data.
- Prevents multiple claims from the same policy from being split across train and test.
- Adds **vehicle brand** and **log-transformed population density** to the GLMs.
- Fits the primary **Poisson frequency GLM** with log-exposure offset.
- Fits the primary **Gamma severity GLM** with log link.
- Reports held-out deviance, observed/expected calibration and decile calibration.
- Estimates frequency overdispersion and fits a method-of-moments **Negative Binomial sensitivity model**.
- Performs a **99.5th-percentile large-loss sensitivity** for severity.
- Audits the known frequency/severity source-data inconsistencies.
- Produces descriptive tables, model coefficients, confidence intervals and calibration figures.
- Records dataset checksums, package versions, random seed and Git commit for reproducibility.

## Run locally

```bash
python src/download_data.py
python research/research_pipeline.py
```

Outputs are written to `research_outputs/`.

## Important interpretation

The matched observed loss cost and the frequency × severity benchmark are kept separate because the public frequency and severity source files are not perfectly aligned. Neither is presented as a final commercial customer premium.
