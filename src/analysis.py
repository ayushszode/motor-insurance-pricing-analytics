"""Data preparation and actuarial portfolio summaries for freMTPL2."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

FREQ_REQUIRED = {
    "IDpol", "ClaimNb", "Exposure", "Area", "VehPower", "VehAge", "DrivAge",
    "BonusMalus", "VehBrand", "VehGas", "Density", "Region",
}
SEV_REQUIRED = {"IDpol", "ClaimAmount"}


def load_data(freq_path: Path, sev_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    freq = pd.read_csv(freq_path)
    sev = pd.read_csv(sev_path)
    missing_f = FREQ_REQUIRED - set(freq.columns)
    missing_s = SEV_REQUIRED - set(sev.columns)
    if missing_f or missing_s:
        raise ValueError(f"Missing columns. Frequency={missing_f}; Severity={missing_s}")

    freq = freq.copy()
    sev = sev.copy()
    freq["IDpol"] = freq["IDpol"].astype(str)
    sev["IDpol"] = sev["IDpol"].astype(str)
    freq = freq.loc[freq["Exposure"].gt(0) & freq["ClaimNb"].ge(0)].copy()
    sev = sev.loc[sev["ClaimAmount"].gt(0)].copy()
    return freq, sev


def add_bands(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["DriverAgeBand"] = pd.cut(
        out["DrivAge"], bins=[17, 25, 35, 45, 55, 65, np.inf],
        labels=["18-25", "26-35", "36-45", "46-55", "56-65", "66+"],
    )
    out["VehicleAgeBand"] = pd.cut(
        out["VehAge"], bins=[-1, 2, 5, 10, np.inf],
        labels=["0-2", "3-5", "6-10", "11+"],
    )
    out["BonusMalusBand"] = pd.cut(
        out["BonusMalus"], bins=[-np.inf, 50, 75, 100, np.inf],
        labels=["<=50", "51-75", "76-100", ">100"],
    )
    out["VehiclePowerBand"] = pd.cut(
        out["VehPower"], bins=[-np.inf, 6, 9, np.inf],
        labels=["4-6", "7-9", "10+"],
    )
    return out


def attach_claim_amounts(freq: pd.DataFrame, sev: pd.DataFrame) -> pd.DataFrame:
    sev_by_policy = (
        sev.groupby("IDpol", as_index=False)
        .agg(ClaimAmountTotal=("ClaimAmount", "sum"), SeverityClaims=("ClaimAmount", "size"))
    )
    out = freq.merge(sev_by_policy, on="IDpol", how="left")
    out[["ClaimAmountTotal", "SeverityClaims"]] = out[["ClaimAmountTotal", "SeverityClaims"]].fillna(0)
    return out


def portfolio_summary(freq: pd.DataFrame, sev: pd.DataFrame) -> pd.DataFrame:
    total_exposure = float(freq["Exposure"].sum())
    total_claims = float(freq["ClaimNb"].sum())
    avg_severity = float(sev["ClaimAmount"].mean())
    annual_frequency = total_claims / total_exposure
    indicated_pp = annual_frequency * avg_severity
    matched = sev["IDpol"].isin(set(freq["IDpol"]))
    matched_amount = float(sev.loc[matched, "ClaimAmount"].sum())
    observed_loss_cost = matched_amount / total_exposure
    return pd.DataFrame([{
        "policies": len(freq),
        "total_exposure": total_exposure,
        "claims": int(total_claims),
        "claim_policies": int((freq["ClaimNb"] > 0).sum()),
        "claim_frequency": annual_frequency,
        "claim_rate_per_100": annual_frequency * 100,
        "claim_policy_pct": (freq["ClaimNb"] > 0).mean() * 100,
        "severity_rows": len(sev),
        "matched_severity_claims": int(matched.sum()),
        "total_claim_amount": matched_amount,
        "avg_severity": avg_severity,
        "observed_loss_cost": observed_loss_cost,
        "indicated_pure_premium": indicated_pp,
    }])


def segment_summary(enriched: pd.DataFrame, segment_col: str, overall_pp: float) -> pd.DataFrame:
    g = enriched.groupby(segment_col, observed=True, dropna=False).agg(
        policies=("IDpol", "size"),
        exposure=("Exposure", "sum"),
        claims=("ClaimNb", "sum"),
        claim_policies=("ClaimNb", lambda s: int((s > 0).sum())),
        severity_claims=("SeverityClaims", "sum"),
        total_claim_amount=("ClaimAmountTotal", "sum"),
    ).reset_index().rename(columns={segment_col: "segment"})

    g["claim_frequency"] = g["claims"] / g["exposure"]
    g["claim_rate_per_100"] = g["claim_frequency"] * 100
    g["claim_policy_pct"] = g["claim_policies"] / g["policies"] * 100
    g["avg_severity"] = np.where(
        g["severity_claims"].gt(0), g["total_claim_amount"] / g["severity_claims"], np.nan
    )
    g["observed_loss_cost"] = g["total_claim_amount"] / g["exposure"]
    g["indicated_pure_premium"] = g["claim_frequency"] * g["avg_severity"]
    g["relativity"] = g["indicated_pure_premium"] / overall_pp
    return g


def build_segment_outputs(freq: pd.DataFrame, sev: pd.DataFrame) -> dict[str, pd.DataFrame]:
    banded = add_bands(freq)
    enriched = attach_claim_amounts(banded, sev)
    overall = portfolio_summary(freq, sev)
    overall_pp = float(overall.loc[0, "indicated_pure_premium"])
    mapping = {
        "driver_age": "DriverAgeBand",
        "vehicle_age": "VehicleAgeBand",
        "bonus_malus": "BonusMalusBand",
        "area": "Area",
        "fuel": "VehGas",
        "vehicle_power": "VehiclePowerBand",
    }
    return {name: segment_summary(enriched, col, overall_pp) for name, col in mapping.items()}
