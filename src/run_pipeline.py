"""Run the complete freMTPL2 pricing analytics workflow."""
from __future__ import annotations

import json
import pandas as pd

from config import FREQ_PATH, SEV_PATH, PROCESSED_DIR, MODEL_DIR, RANDOM_STATE
from download_data import main as download_data
from analysis import load_data, portfolio_summary, build_segment_outputs
from modeling import fit_models, score_portfolio, save_bundle


def main() -> None:
    if not FREQ_PATH.exists() or not SEV_PATH.exists():
        download_data()

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    freq, sev = load_data(FREQ_PATH, SEV_PATH)

    summary = portfolio_summary(freq, sev)
    summary.to_csv(PROCESSED_DIR / "portfolio_summary_rebuilt.csv", index=False)

    for name, table in build_segment_outputs(freq, sev).items():
        table.to_csv(PROCESSED_DIR / f"{name}_pricing_rebuilt.csv", index=False)

    bundle = fit_models(freq, sev, random_state=RANDOM_STATE)
    save_bundle(bundle, MODEL_DIR)

    scored = score_portfolio(bundle, freq)
    scored[[
        "IDpol", "Exposure", "Area", "VehPower", "VehAge", "DrivAge", "BonusMalus",
        "VehGas", "Region", "PredictedFrequency", "PredictedSeverity", "PurePremium", "RiskTier"
    ]].sample(n=min(20000, len(scored)), random_state=RANDOM_STATE).to_csv(
        PROCESSED_DIR / "pricing_predictions_sample.csv", index=False
    )

    tier_summary = scored.groupby("RiskTier", observed=True).agg(
        policies=("IDpol", "size"),
        avg_frequency=("PredictedFrequency", "mean"),
        avg_severity=("PredictedSeverity", "mean"),
        avg_pure_premium=("PurePremium", "mean"),
    ).reset_index()
    tier_summary.to_csv(PROCESSED_DIR / "model_risk_tiers.csv", index=False)

    print("Pipeline complete")
    print(json.dumps(bundle.metrics, indent=2))


if __name__ == "__main__":
    main()
