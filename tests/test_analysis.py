import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from analysis import add_bands, portfolio_summary, build_segment_outputs


def toy_data():
    freq = pd.DataFrame({
        "IDpol": ["1", "2", "3"],
        "ClaimNb": [0, 1, 2],
        "Exposure": [1.0, 1.0, 0.5],
        "Area": ["A", "B", "B"],
        "VehPower": [5, 7, 10],
        "VehAge": [1, 4, 12],
        "DrivAge": [24, 40, 70],
        "BonusMalus": [50, 70, 110],
        "VehBrand": ["B1", "B2", "B3"],
        "VehGas": ["Diesel", "Regular", "Diesel"],
        "Density": [10, 100, 1000],
        "Region": ["R1", "R2", "R2"],
    })
    sev = pd.DataFrame({"IDpol": ["2", "3", "3"], "ClaimAmount": [1000.0, 500.0, 1500.0]})
    return freq, sev


def test_bands():
    freq, _ = toy_data()
    out = add_bands(freq)
    assert str(out.loc[0, "DriverAgeBand"]) == "18-25"
    assert str(out.loc[2, "BonusMalusBand"]) == ">100"


def test_pure_premium_identity():
    freq, sev = toy_data()
    s = portfolio_summary(freq, sev).iloc[0]
    assert abs(s["indicated_pure_premium"] - s["claim_frequency"] * s["avg_severity"]) < 1e-9


def test_segment_outputs_exist():
    freq, sev = toy_data()
    outputs = build_segment_outputs(freq, sev)
    assert "driver_age" in outputs
    assert "indicated_pure_premium" in outputs["driver_age"].columns
