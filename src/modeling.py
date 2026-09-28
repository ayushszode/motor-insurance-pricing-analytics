"""Frequency-severity GLMs for motor insurance pricing."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_poisson_deviance, mean_gamma_deviance

from analysis import add_bands


FREQ_FORMULA = (
    "ClaimNb ~ C(DriverAgeBand) + C(VehicleAgeBand) + C(BonusMalusBand) + "
    "C(VehiclePowerBand) + C(Area) + C(VehGas) + C(Region)"
)
SEV_FORMULA = (
    "ClaimAmount ~ C(DriverAgeBand) + C(VehicleAgeBand) + C(BonusMalusBand) + "
    "C(VehiclePowerBand) + C(Area) + C(VehGas) + C(Region)"
)


@dataclass
class ModelBundle:
    frequency: object
    severity: object
    metrics: dict


def fit_models(freq: pd.DataFrame, sev: pd.DataFrame, random_state: int = 42) -> ModelBundle:
    freq_b = add_bands(freq)
    train_f, test_f = train_test_split(freq_b, test_size=0.20, random_state=random_state)

    freq_model = smf.glm(
        formula=FREQ_FORMULA,
        data=train_f,
        family=sm.families.Poisson(),
        offset=np.log(train_f["Exposure"].clip(lower=1e-6)),
    ).fit()
    pred_count = np.clip(
        np.asarray(freq_model.predict(test_f, offset=np.log(test_f["Exposure"].clip(lower=1e-6)))),
        1e-9, None
    )
    freq_deviance = mean_poisson_deviance(test_f["ClaimNb"], pred_count)

    sev_m = sev.merge(freq_b.drop(columns=["ClaimNb"]), on="IDpol", how="inner")
    sev_m = sev_m.loc[sev_m["ClaimAmount"].gt(0)].copy()
    train_s, test_s = train_test_split(sev_m, test_size=0.20, random_state=random_state)
    sev_model = smf.glm(
        formula=SEV_FORMULA,
        data=train_s,
        family=sm.families.Gamma(link=sm.families.links.Log()),
    ).fit()
    pred_sev = np.clip(np.asarray(sev_model.predict(test_s)), 1e-9, None)
    sev_deviance = mean_gamma_deviance(test_s["ClaimAmount"], pred_sev)

    metrics = {
        "frequency_poisson_deviance": float(freq_deviance),
        "severity_gamma_deviance": float(sev_deviance),
        "frequency_train_rows": int(len(train_f)),
        "frequency_test_rows": int(len(test_f)),
        "severity_train_rows": int(len(train_s)),
        "severity_test_rows": int(len(test_s)),
    }
    return ModelBundle(freq_model, sev_model, metrics)


def score_portfolio(bundle: ModelBundle, freq: pd.DataFrame) -> pd.DataFrame:
    x = add_bands(freq)
    # Predict annual claim frequency at exposure = 1 policy-year.
    x["PredictedFrequency"] = np.clip(np.asarray(bundle.frequency.predict(x, offset=np.zeros(len(x)))), 0, None)
    x["PredictedSeverity"] = np.clip(np.asarray(bundle.severity.predict(x)), 0, None)
    x["PurePremium"] = x["PredictedFrequency"] * x["PredictedSeverity"]
    x["RiskTier"] = pd.qcut(
        x["PurePremium"].rank(method="first"), 5,
        labels=["Very Low", "Low", "Medium", "High", "Very High"]
    )
    return x


def save_bundle(bundle: ModelBundle, model_dir: Path) -> None:
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle.frequency, model_dir / "frequency_poisson_glm.pkl")
    joblib.dump(bundle.severity, model_dir / "severity_gamma_glm.pkl")
    with (model_dir / "model_metrics.json").open("w") as f:
        json.dump(bundle.metrics, f, indent=2)
