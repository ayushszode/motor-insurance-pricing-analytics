# Data

This project uses the **freMTPL2 French Motor Third-Party Liability** benchmark dataset.

## Files

- `freMTPL2freq.csv` — policy-level claim counts, exposure and rating factors.
- `freMTPL2sev.csv` — claim-level claim amounts linked by `IDpol`.

Raw files are intentionally excluded from Git because the frequency file is large and the data remains subject to its source terms.

## Sources

Original dataset documentation / CASdatasets reference:
https://dutangc.github.io/CASdatasets/reference/freMTPL.html

Convenient Hugging Face mirror used by `src/download_data.py`:
https://huggingface.co/datasets/mabilton/fremtpl2

The mirror states that it mirrors the freMTPL2 frequency and severity data and is licensed GPL-2.0. Review the source terms before redistributing raw data.

## Download

From the project root:

```bash
python src/download_data.py
```

The script downloads the two CSV files into `data/raw/`.

## Verified portfolio snapshot included in this repository

The small CSVs under `data/processed/` are aggregated portfolio summaries derived from the full source data. They are included so the business analysis and Excel dashboard can be reviewed without committing the ~38 MB raw dataset.
