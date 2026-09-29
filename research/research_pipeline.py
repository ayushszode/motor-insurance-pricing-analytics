"""Publication-grade research pipeline for the freMTPL2 motor-pricing paper.

Outputs small, reviewable research artifacts under research_outputs/.
The raw source data is downloaded by src/download_data.py and is not committed.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import mean_absolute_error, mean_gamma_deviance, mean_poisson_deviance
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "research_outputs"
FIG = OUT / "figures"
FREQ_PATH = RAW / "freMTPL2freq.csv"
SEV_PATH = RAW / "freMTPL2sev.csv"

SEED = 42
TEST_SIZE = 0.20

FREQ_REQUIRED = {
    "IDpol", "ClaimNb", "Exposure", "Area", "VehPower", "VehAge", "DrivAge",
    "BonusMalus", "VehBrand", "VehGas", "Density", "Region",
}
SEV_REQUIRED = {"IDpol", "ClaimAmount"}

CAT_VARS = [
    "DriverAgeBand", "VehicleAgeBand", "BonusMalusBand", "VehiclePowerBand",
    "Area", "VehGas", "Region", "VehBrand",
]
FORMULA_RHS = (
    "C(DriverAgeBand) + C(VehicleAgeBand) + C(BonusMalusBand) + "
    "C(VehiclePowerBand) + C(Area) + C(VehGas) + C(Region) + "
    "C(VehBrand) + LogDensity"
)
FREQ_FORMULA = f"ClaimNb ~ {FORMULA_RHS}"
SEV_FORMULA = f"ClaimAmount ~ {FORMULA_RHS}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        return os.environ.get("GITHUB_SHA", "unknown")


def clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.select_dtypes(include=["object", "string"]).columns:
        out[col] = out[col].astype(str).str.strip("'").str.strip()
    return out


def add_features(df: pd.DataFrame, category_levels: dict[str, list[str]] | None = None) -> pd.DataFrame:
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
    out["LogDensity"] = np.log1p(pd.to_numeric(out["Density"], errors="coerce"))

    if category_levels:
        for col, levels in category_levels.items():
            out[col] = pd.Categorical(out[col].astype(str), categories=levels)
    return out


def make_levels(freq: pd.DataFrame) -> dict[str, list[str]]:
    temp = add_features(freq)
    levels: dict[str, list[str]] = {}
    for col in CAT_VARS:
        if isinstance(temp[col].dtype, pd.CategoricalDtype):
            levels[col] = [str(x) for x in temp[col].cat.categories]
        else:
            levels[col] = sorted(temp[col].dropna().astype(str).unique().tolist())
    return levels


def coefficient_table(model, model_name: str) -> pd.DataFrame:
    ci = model.conf_int()
    out = pd.DataFrame({
        "term": model.params.index,
        "coefficient": model.params.values,
        "std_error": model.bse.values,
        "p_value": model.pvalues.values,
        "ci_lower": ci.iloc[:, 0].values,
        "ci_upper": ci.iloc[:, 1].values,
    })
    out["relativity"] = np.exp(out["coefficient"])
    out["relativity_ci_lower"] = np.exp(out["ci_lower"])
    out["relativity_ci_upper"] = np.exp(out["ci_upper"])
    out.insert(0, "model", model_name)
    return out


def assign_deciles(values: pd.Series, q: int = 10) -> pd.Series:
    ranked = values.rank(method="first")
    return pd.qcut(ranked, q=q, labels=list(range(1, q + 1)))


def frequency_calibration(test: pd.DataFrame, pred_count: np.ndarray, pred_annual: np.ndarray) -> pd.DataFrame:
    x = test[["IDpol", "Exposure", "ClaimNb"]].copy()
    x["pred_count"] = pred_count
    x["pred_annual_frequency"] = pred_annual
    x["risk_decile"] = assign_deciles(x["pred_annual_frequency"], 10)
    g = x.groupby("risk_decile", observed=True).agg(
        policies=("IDpol", "size"),
        exposure=("Exposure", "sum"),
        observed_claims=("ClaimNb", "sum"),
        predicted_claims=("pred_count", "sum"),
    ).reset_index()
    g["observed_frequency"] = g["observed_claims"] / g["exposure"]
    g["predicted_frequency"] = g["predicted_claims"] / g["exposure"]
    g["oe_ratio"] = g["observed_claims"] / g["predicted_claims"]
    return g


def severity_calibration(test: pd.DataFrame, pred: np.ndarray) -> pd.DataFrame:
    x = test[["IDpol", "ClaimAmount"]].copy()
    x["predicted_severity"] = pred
    x["risk_decile"] = assign_deciles(x["predicted_severity"], 10)
    g = x.groupby("risk_decile", observed=True).agg(
        claim_rows=("IDpol", "size"),
        observed_total=("ClaimAmount", "sum"),
        predicted_total=("predicted_severity", "sum"),
        observed_mean=("ClaimAmount", "mean"),
        predicted_mean=("predicted_severity", "mean"),
    ).reset_index()
    g["oe_ratio"] = g["observed_total"] / g["predicted_total"]
    return g


def build_segment_table(freq: pd.DataFrame, sev: pd.DataFrame, segment: str) -> pd.DataFrame:
    sev_by_policy = sev.groupby("IDpol", as_index=False).agg(
        matched_claim_amount=("ClaimAmount", "sum"),
        severity_claims=("ClaimAmount", "size"),
    )
    x = freq.merge(sev_by_policy, on="IDpol", how="left")
    x[["matched_claim_amount", "severity_claims"]] = x[
        ["matched_claim_amount", "severity_claims"]
    ].fillna(0)
    g = x.groupby(segment, observed=True).agg(
        policies=("IDpol", "size"),
        exposure=("Exposure", "sum"),
        claims=("ClaimNb", "sum"),
        matched_claim_amount=("matched_claim_amount", "sum"),
        severity_claims=("severity_claims", "sum"),
    ).reset_index()
    g["claim_frequency"] = g["claims"] / g["exposure"]
    g["average_severity"] = np.where(
        g["severity_claims"] > 0,
        g["matched_claim_amount"] / g["severity_claims"],
        np.nan,
    )
    g["matched_loss_cost"] = g["matched_claim_amount"] / g["exposure"]
    g["indicated_pure_premium"] = g["claim_frequency"] * g["average_severity"]
    return g


def save_line_calibration(df: pd.DataFrame, observed: str, predicted: str, title: str, ylabel: str, path: Path):
    plt.figure(figsize=(7.2, 4.6))
    x = df["risk_decile"].astype(int)
    plt.plot(x, df[observed], marker="o", label="Observed")
    plt.plot(x, df[predicted], marker="o", label="Predicted")
    plt.xlabel("Predicted-risk decile")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)

    if not FREQ_PATH.exists() or not SEV_PATH.exists():
        raise FileNotFoundError(
            "Raw files are missing. Run: python src/download_data.py"
        )

    freq_raw = clean_strings(pd.read_csv(FREQ_PATH))
    sev_raw = clean_strings(pd.read_csv(SEV_PATH))

    missing_f = FREQ_REQUIRED - set(freq_raw.columns)
    missing_s = SEV_REQUIRED - set(sev_raw.columns)
    if missing_f or missing_s:
        raise ValueError(f"Missing required columns: frequency={missing_f}; severity={missing_s}")

    # Canonical numeric types.
    for col in ["ClaimNb", "Exposure", "VehPower", "VehAge", "DrivAge", "BonusMalus", "Density"]:
        freq_raw[col] = pd.to_numeric(freq_raw[col], errors="coerce")
    sev_raw["ClaimAmount"] = pd.to_numeric(sev_raw["ClaimAmount"], errors="coerce")
    freq_raw["IDpol"] = pd.to_numeric(freq_raw["IDpol"], errors="coerce").astype("Int64")
    sev_raw["IDpol"] = pd.to_numeric(sev_raw["IDpol"], errors="coerce").astype("Int64")

    raw_freq_rows = len(freq_raw)
    raw_sev_rows = len(sev_raw)

    freq = freq_raw.loc[
        freq_raw["IDpol"].notna()
        & freq_raw["Exposure"].gt(0)
        & freq_raw["ClaimNb"].ge(0)
    ].copy()
    sev = sev_raw.loc[
        sev_raw["IDpol"].notna() & sev_raw["ClaimAmount"].gt(0)
    ].copy()
    freq["IDpol"] = freq["IDpol"].astype("int64")
    sev["IDpol"] = sev["IDpol"].astype("int64")

    levels = make_levels(freq)
    freq = add_features(freq, levels)

    freq_ids = set(freq["IDpol"].tolist())
    sev["matched_policy"] = sev["IDpol"].isin(freq_ids)
    sev_matched = sev.loc[sev["matched_policy"]].copy()

    # Merge policy characteristics onto matched severity rows.
    policy_cols = [
        "IDpol", "DriverAgeBand", "VehicleAgeBand", "BonusMalusBand",
        "VehiclePowerBand", "Area", "VehGas", "Region", "VehBrand", "LogDensity",
    ]
    sev_m = sev_matched[["IDpol", "ClaimAmount"]].merge(
        freq[policy_cols], on="IDpol", how="inner", validate="many_to_one"
    )

    # One policy-level split drives both frequency and severity partitions.
    unique_ids = freq["IDpol"].to_numpy()
    train_ids, test_ids = train_test_split(
        unique_ids, test_size=TEST_SIZE, random_state=SEED
    )
    train_set, test_set = set(train_ids.tolist()), set(test_ids.tolist())

    train_f = freq.loc[freq["IDpol"].isin(train_set)].copy()
    test_f = freq.loc[freq["IDpol"].isin(test_set)].copy()
    train_s = sev_m.loc[sev_m["IDpol"].isin(train_set)].copy()
    test_s = sev_m.loc[sev_m["IDpol"].isin(test_set)].copy()

    # ---------------- Primary frequency model ----------------
    freq_model = smf.glm(
        formula=FREQ_FORMULA,
        data=train_f,
        family=sm.families.Poisson(),
        offset=np.log(train_f["Exposure"].clip(lower=1e-9)),
    ).fit()

    pred_count = np.clip(
        np.asarray(
            freq_model.predict(
                test_f, offset=np.log(test_f["Exposure"].clip(lower=1e-9))
            )
        ),
        1e-12,
        None,
    )
    pred_annual = np.clip(
        np.asarray(freq_model.predict(test_f, offset=np.zeros(len(test_f)))),
        1e-12,
        None,
    )
    freq_dev = float(mean_poisson_deviance(test_f["ClaimNb"], pred_count))
    freq_oe = float(test_f["ClaimNb"].sum() / pred_count.sum())
    dispersion = float(freq_model.pearson_chi2 / freq_model.df_resid)

    freq_cal = frequency_calibration(test_f, pred_count, pred_annual)
    freq_cal.to_csv(OUT / "frequency_calibration.csv", index=False)
    coefficient_table(freq_model, "Poisson frequency GLM").to_csv(
        OUT / "frequency_coefficients.csv", index=False
    )

    # Exposure sensitivity: a small number of freMTPL2 records have Exposure > 1.
    # Standard public examples sometimes cap such observations at one policy-year.
    # We keep the uncapped data as primary and report the capped result only as sensitivity.
    train_f_exp_cap = train_f.copy()
    test_f_exp_cap = test_f.copy()
    train_f_exp_cap["Exposure"] = train_f_exp_cap["Exposure"].clip(upper=1.0)
    test_f_exp_cap["Exposure"] = test_f_exp_cap["Exposure"].clip(upper=1.0)
    freq_exp_cap_model = smf.glm(
        formula=FREQ_FORMULA,
        data=train_f_exp_cap,
        family=sm.families.Poisson(),
        offset=np.log(train_f_exp_cap["Exposure"].clip(lower=1e-9)),
    ).fit()
    exp_cap_pred_count = np.clip(
        np.asarray(freq_exp_cap_model.predict(
            test_f_exp_cap,
            offset=np.log(test_f_exp_cap["Exposure"].clip(lower=1e-9)),
        )),
        1e-12,
        None,
    )
    exp_cap_dev = float(mean_poisson_deviance(test_f_exp_cap["ClaimNb"], exp_cap_pred_count))
    exp_cap_oe = float(test_f_exp_cap["ClaimNb"].sum() / exp_cap_pred_count.sum())

    # Method-of-moments NB2 alpha; used only as a sensitivity model.
    mu_train = np.clip(np.asarray(freq_model.fittedvalues), 1e-12, None)
    y_train = train_f["ClaimNb"].to_numpy(dtype=float)
    alpha_num = np.sum((y_train - mu_train) ** 2 - y_train)
    alpha_den = np.sum(mu_train ** 2)
    alpha_hat = float(max(alpha_num / alpha_den, 1e-8))

    nb_family = sm.families.NegativeBinomial(alpha=alpha_hat)
    nb_model = smf.glm(
        formula=FREQ_FORMULA,
        data=train_f,
        family=nb_family,
        offset=np.log(train_f["Exposure"].clip(lower=1e-9)),
    ).fit()
    nb_pred_count = np.clip(
        np.asarray(
            nb_model.predict(
                test_f, offset=np.log(test_f["Exposure"].clip(lower=1e-9))
            )
        ),
        1e-12,
        None,
    )
    nb_dev = float(
        nb_family.deviance(
            test_f["ClaimNb"].to_numpy(dtype=float), nb_pred_count
        ) / len(test_f)
    )
    nb_oe = float(test_f["ClaimNb"].sum() / nb_pred_count.sum())

    # ---------------- Primary severity model ----------------
    sev_model = smf.glm(
        formula=SEV_FORMULA,
        data=train_s,
        family=sm.families.Gamma(link=sm.families.links.Log()),
    ).fit()
    pred_sev = np.clip(np.asarray(sev_model.predict(test_s)), 1e-12, None)
    sev_dev = float(mean_gamma_deviance(test_s["ClaimAmount"], pred_sev))
    sev_mae = float(mean_absolute_error(test_s["ClaimAmount"], pred_sev))
    sev_oe = float(test_s["ClaimAmount"].sum() / pred_sev.sum())

    sev_cal = severity_calibration(test_s, pred_sev)
    sev_cal.to_csv(OUT / "severity_calibration.csv", index=False)
    coefficient_table(sev_model, "Gamma severity GLM").to_csv(
        OUT / "severity_coefficients.csv", index=False
    )

    # Large-loss sensitivity: winsorise at training-sample 99.5th percentile.
    cap = float(train_s["ClaimAmount"].quantile(0.995))
    train_s_sens = train_s.copy()
    test_s_sens = test_s.copy()
    train_s_sens["ClaimAmount"] = train_s_sens["ClaimAmount"].clip(upper=cap)
    test_s_sens["ClaimAmount"] = test_s_sens["ClaimAmount"].clip(upper=cap)
    sev_sens_model = smf.glm(
        formula=SEV_FORMULA,
        data=train_s_sens,
        family=sm.families.Gamma(link=sm.families.links.Log()),
    ).fit()
    pred_sev_sens = np.clip(
        np.asarray(sev_sens_model.predict(test_s_sens)), 1e-12, None
    )
    sev_sens_dev = float(
        mean_gamma_deviance(test_s_sens["ClaimAmount"], pred_sev_sens)
    )
    sev_sens_oe = float(
        test_s_sens["ClaimAmount"].sum() / pred_sev_sens.sum()
    )

    # ---------------- Pure-premium scoring / calibration ----------------
    test_pp = test_f[["IDpol", "Exposure", "ClaimNb"]].copy()
    test_pp["predicted_frequency"] = pred_annual
    test_pp["predicted_severity"] = np.clip(
        np.asarray(sev_model.predict(test_f)), 1e-12, None
    )
    test_pp["predicted_pure_premium"] = (
        test_pp["predicted_frequency"] * test_pp["predicted_severity"]
    )

    sev_by_policy = sev_matched.groupby("IDpol", as_index=False).agg(
        matched_claim_amount=("ClaimAmount", "sum"),
        severity_count=("ClaimAmount", "size"),
    )
    test_pp = test_pp.merge(sev_by_policy, on="IDpol", how="left")
    test_pp[["matched_claim_amount", "severity_count"]] = test_pp[
        ["matched_claim_amount", "severity_count"]
    ].fillna(0)
    test_pp["predicted_loss_amount"] = (
        test_pp["predicted_pure_premium"] * test_pp["Exposure"]
    )
    test_pp["risk_decile"] = assign_deciles(
        test_pp["predicted_pure_premium"], 10
    )

    pp_cal = test_pp.groupby("risk_decile", observed=True).agg(
        policies=("IDpol", "size"),
        exposure=("Exposure", "sum"),
        observed_matched_loss=("matched_claim_amount", "sum"),
        predicted_loss=("predicted_loss_amount", "sum"),
        mean_predicted_pure_premium=("predicted_pure_premium", "mean"),
    ).reset_index()
    pp_cal["observed_matched_loss_cost"] = (
        pp_cal["observed_matched_loss"] / pp_cal["exposure"]
    )
    pp_cal["predicted_loss_cost"] = pp_cal["predicted_loss"] / pp_cal["exposure"]
    pp_cal["oe_ratio"] = pp_cal["observed_matched_loss"] / pp_cal["predicted_loss"]
    pp_cal.to_csv(OUT / "pure_premium_calibration.csv", index=False)

    # ---------------- Source consistency audit ----------------
    sev_counts = sev_matched.groupby("IDpol").size().rename("SeverityCount")
    consistency = freq[["IDpol", "ClaimNb", "Exposure"]].copy()
    consistency = consistency.merge(
        sev_counts, left_on="IDpol", right_index=True, how="left"
    )
    consistency["SeverityCount"] = consistency["SeverityCount"].fillna(0).astype(int)
    consistency["status"] = np.select(
        [
            consistency["ClaimNb"].eq(consistency["SeverityCount"]),
            consistency["ClaimNb"].gt(consistency["SeverityCount"]),
        ],
        ["exact_match", "frequency_gt_severity"],
        default="severity_gt_frequency",
    )
    consistency_summary = consistency.groupby("status").agg(
        policies=("IDpol", "size"),
        exposure=("Exposure", "sum"),
        frequency_claims=("ClaimNb", "sum"),
        severity_rows=("SeverityCount", "sum"),
    ).reset_index()
    consistency_summary.to_csv(OUT / "consistency_analysis.csv", index=False)

    exact_ids = set(
        consistency.loc[consistency["status"].eq("exact_match"), "IDpol"].tolist()
    )
    consistent_pp = test_pp.loc[test_pp["IDpol"].isin(exact_ids)]
    consistent_observed = float(consistent_pp["matched_claim_amount"].sum())
    consistent_predicted = float(consistent_pp["predicted_loss_amount"].sum())
    consistent_oe = (
        consistent_observed / consistent_predicted
        if consistent_predicted > 0 else np.nan
    )

    # ---------------- Descriptive figures ----------------
    full_banded = freq.copy()
    age = build_segment_table(full_banded, sev_matched, "DriverAgeBand")
    bm = build_segment_table(full_banded, sev_matched, "BonusMalusBand")
    age.to_csv(OUT / "driver_age_descriptive.csv", index=False)
    bm.to_csv(OUT / "bonus_malus_descriptive.csv", index=False)

    plt.figure(figsize=(7.2, 4.6))
    plt.bar(age["DriverAgeBand"].astype(str), age["claim_frequency"] * 100)
    plt.xlabel("Driver age band")
    plt.ylabel("Claims per 100 policy-years")
    plt.title("Observed Claim Frequency by Driver Age")
    plt.tight_layout()
    plt.savefig(FIG / "driver_age_frequency.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.2, 4.6))
    plt.bar(bm["BonusMalusBand"].astype(str), bm["indicated_pure_premium"])
    plt.xlabel("Bonus-Malus band")
    plt.ylabel("Indicated pure premium")
    plt.title("Indicated Pure Premium by Bonus-Malus Band")
    plt.tight_layout()
    plt.savefig(FIG / "bonus_malus_pure_premium.png", dpi=180)
    plt.close()

    save_line_calibration(
        freq_cal, "observed_frequency", "predicted_frequency",
        "Frequency Model Calibration", "Annual claim frequency",
        FIG / "frequency_calibration.png",
    )
    save_line_calibration(
        sev_cal, "observed_mean", "predicted_mean",
        "Severity Model Calibration", "Mean claim severity",
        FIG / "severity_calibration.png",
    )
    save_line_calibration(
        pp_cal, "observed_matched_loss_cost", "predicted_loss_cost",
        "Pure-Premium Calibration (Matched-Loss Diagnostic)",
        "Loss cost per policy-year",
        FIG / "pure_premium_calibration.png",
    )

    # ---------------- Audit and metrics ----------------
    raw_unmatched_sev = int((~sev["matched_policy"]).sum())
    duplicate_freq_ids = int(freq["IDpol"].duplicated().sum())
    exposure_gt_1 = int(freq["Exposure"].gt(1).sum())
    claimnb_gt_4 = int(freq["ClaimNb"].gt(4).sum())
    max_claimnb = float(freq["ClaimNb"].max())
    severity_gt_200k = int(sev_matched["ClaimAmount"].gt(200000).sum())
    max_severity = float(sev_matched["ClaimAmount"].max())
    severity_p99 = float(sev_matched["ClaimAmount"].quantile(0.99))
    severity_p995 = float(sev_matched["ClaimAmount"].quantile(0.995))

    audit = {
        "dataset": "freMTPL2",
        "frequency_source": "project downloader / public mirror",
        "severity_source": "project downloader / public mirror",
        "frequency_sha256": sha256(FREQ_PATH),
        "severity_sha256": sha256(SEV_PATH),
        "raw_frequency_rows": int(raw_freq_rows),
        "valid_frequency_rows": int(len(freq)),
        "raw_severity_rows": int(raw_sev_rows),
        "positive_severity_rows": int(len(sev)),
        "matched_positive_severity_rows": int(len(sev_matched)),
        "unmatched_positive_severity_rows": raw_unmatched_sev,
        "duplicate_frequency_policy_ids": duplicate_freq_ids,
        "frequency_total_claims": float(freq["ClaimNb"].sum()),
        "total_exposure": float(freq["Exposure"].sum()),
        "policies_exposure_gt_1": exposure_gt_1,
        "max_exposure": float(freq["Exposure"].max()),
        "policies_claimnb_gt_4": claimnb_gt_4,
        "max_claim_count": max_claimnb,
        "matched_severity_rows_gt_200000": severity_gt_200k,
        "max_matched_severity": max_severity,
        "matched_severity_p99": severity_p99,
        "matched_severity_p995": severity_p995,
        "train_policy_rows": int(len(train_f)),
        "test_policy_rows": int(len(test_f)),
        "train_severity_rows": int(len(train_s)),
        "test_severity_rows": int(len(test_s)),
        "random_seed": SEED,
        "test_size": TEST_SIZE,
        "git_commit": git_sha(),
        "python_version": platform.python_version(),
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "scikit_learn_version": sklearn.__version__,
        "statsmodels_version": statsmodels.__version__,
    }
    with (OUT / "data_audit.json").open("w") as f:
        json.dump(audit, f, indent=2)

    portfolio_frequency = float(freq["ClaimNb"].sum() / freq["Exposure"].sum())
    matched_avg_severity = float(sev_matched["ClaimAmount"].mean())
    matched_loss_amount = float(sev_matched["ClaimAmount"].sum())
    matched_loss_cost = float(matched_loss_amount / freq["Exposure"].sum())
    frequency_x_severity = float(portfolio_frequency * matched_avg_severity)

    metrics = {
        "portfolio": {
            "annual_claim_frequency": portfolio_frequency,
            "claims_per_100_policy_years": portfolio_frequency * 100,
            "matched_average_severity": matched_avg_severity,
            "matched_observed_loss_cost": matched_loss_cost,
            "frequency_x_matched_severity_benchmark": frequency_x_severity,
        },
        "frequency_poisson": {
            "test_mean_poisson_deviance": freq_dev,
            "test_observed_expected_ratio": freq_oe,
            "training_pearson_dispersion": dispersion,
        },
        "frequency_exposure_cap_sensitivity": {
            "exposure_cap": 1.0,
            "test_mean_poisson_deviance": exp_cap_dev,
            "test_observed_expected_ratio": exp_cap_oe,
        },
        "frequency_negative_binomial_sensitivity": {
            "method_of_moments_alpha": alpha_hat,
            "test_mean_nb_deviance": nb_dev,
            "test_observed_expected_ratio": nb_oe,
        },
        "severity_gamma": {
            "test_mean_gamma_deviance": sev_dev,
            "test_mae": sev_mae,
            "test_observed_expected_ratio": sev_oe,
        },
        "severity_large_loss_sensitivity": {
            "training_cap_percentile": 0.995,
            "training_cap_value": cap,
            "test_mean_gamma_deviance_capped": sev_sens_dev,
            "test_observed_expected_ratio_capped": sev_sens_oe,
        },
        "pure_premium_matched_loss_diagnostic": {
            "test_observed_matched_loss": float(test_pp["matched_claim_amount"].sum()),
            "test_predicted_loss": float(test_pp["predicted_loss_amount"].sum()),
            "test_observed_expected_ratio": float(
                test_pp["matched_claim_amount"].sum()
                / test_pp["predicted_loss_amount"].sum()
            ),
            "consistent_subset_observed_expected_ratio": float(consistent_oe),
        },
    }
    with (OUT / "model_metrics.json").open("w") as f:
        json.dump(metrics, f, indent=2)

    sensitivity = pd.DataFrame([
        {
            "analysis": "Poisson frequency GLM",
            "metric": "mean_poisson_deviance",
            "value": freq_dev,
            "oe_ratio": freq_oe,
            "note": "Primary frequency model",
        },
        {
            "analysis": "Poisson exposure-capped sensitivity",
            "metric": "mean_poisson_deviance",
            "value": exp_cap_dev,
            "oe_ratio": exp_cap_oe,
            "note": "Exposure capped at 1.0 policy-year; primary analysis remains uncapped",
        },
        {
            "analysis": "Negative Binomial GLM sensitivity",
            "metric": "mean_nb_deviance",
            "value": nb_dev,
            "oe_ratio": nb_oe,
            "note": f"NB2 method-of-moments alpha={alpha_hat:.6g}",
        },
        {
            "analysis": "Gamma severity GLM",
            "metric": "mean_gamma_deviance",
            "value": sev_dev,
            "oe_ratio": sev_oe,
            "note": "Primary positive-claim severity model",
        },
        {
            "analysis": "Gamma severity 99.5% capped sensitivity",
            "metric": "mean_gamma_deviance",
            "value": sev_sens_dev,
            "oe_ratio": sev_sens_oe,
            "note": f"Training-sample cap={cap:.6g}",
        },
    ])
    sensitivity.to_csv(OUT / "sensitivity_results.csv", index=False)

    # Machine-readable sample counts.
    pd.DataFrame([
        {"sample": "frequency_train", "rows": len(train_f)},
        {"sample": "frequency_test", "rows": len(test_f)},
        {"sample": "severity_train", "rows": len(train_s)},
        {"sample": "severity_test", "rows": len(test_s)},
    ]).to_csv(OUT / "modelling_sample_counts.csv", index=False)

    mismatch_policies = int(
        consistency.loc[~consistency["status"].eq("exact_match"), "IDpol"].nunique()
    )
    summary = f"""# Step 5 Research Execution Summary

Generated automatically from the publication-grade research pipeline.

## Dataset audit

- Valid frequency policies: **{len(freq):,}**
- Total exposure: **{freq["Exposure"].sum():,.2f} policy-years**
- Frequency-table claims: **{freq["ClaimNb"].sum():,.0f}**
- Positive severity rows: **{len(sev):,}**
- Matched positive severity rows: **{len(sev_matched):,}**
- Unmatched positive severity rows: **{raw_unmatched_sev:,}**
- Policies with frequency/severity count mismatch: **{mismatch_policies:,}**

## Held-out models

- Poisson test mean deviance: **{freq_dev:.6f}**
- Poisson test O/E: **{freq_oe:.4f}**
- Poisson training Pearson dispersion: **{dispersion:.4f}**
- Exposure-capped Poisson test mean deviance: **{exp_cap_dev:.6f}**
- Exposure-capped Poisson test O/E: **{exp_cap_oe:.4f}**
- Negative Binomial sensitivity alpha: **{alpha_hat:.6f}**
- Negative Binomial test mean deviance: **{nb_dev:.6f}**
- Gamma severity test mean deviance: **{sev_dev:.6f}**
- Gamma severity test MAE: **{sev_mae:,.2f}**
- Gamma severity test O/E: **{sev_oe:.4f}**
- 99.5% training large-loss cap: **{cap:,.2f}**
- Capped Gamma test mean deviance: **{sev_sens_dev:.6f}**

## Portfolio benchmarks

- Claim frequency: **{portfolio_frequency:.6f}** ({portfolio_frequency*100:.2f} per 100 policy-years)
- Matched average severity: **{matched_avg_severity:,.2f}**
- Matched observed loss cost: **{matched_loss_cost:,.2f} per policy-year**
- Frequency × matched-severity benchmark: **{frequency_x_severity:,.2f} per policy-year**

## Research integrity note

The source frequency and severity files are not perfectly aligned. The paper must keep
the matched observed loss-cost diagnostic separate from the frequency × severity benchmark
and must not describe either as a final commercial premium.
"""
    (OUT / "results_summary.md").write_text(summary)

    print(summary)


if __name__ == "__main__":
    main()
