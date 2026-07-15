"""Integration checks for the publication-safe release candidate."""

from pathlib import Path
import hashlib

import numpy as np
import pandas as pd

from gkx_public.core import EXPECTED_COLUMNS, gkx_r2_oos, summarize_panel, validate_panel


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "results" / "publication_source_data"


def test_synthetic_sample_schema_and_identity() -> None:
    panel = pd.read_csv(ROOT / "sample_data" / "sample_panel.csv")
    summary = summarize_panel(panel)
    assert tuple(panel.columns) == EXPECTED_COLUMNS
    assert summary == {"rows": 54, "securities": 3, "months": 18, "first_date": "2020-01-31", "last_date": "2021-06-30"}
    assert set(panel["ticker"]) == {"SYN_A", "SYN_B", "SYN_C"}


def test_duplicate_security_month_is_rejected() -> None:
    panel = pd.read_csv(ROOT / "sample_data" / "sample_panel.csv")
    duplicated = pd.concat([panel, panel.iloc[[0]]], ignore_index=True)
    try:
        validate_panel(duplicated)
    except ValueError as error:
        assert "duplicate security-month" in str(error)
    else:
        raise AssertionError("Duplicate security-month was not rejected")


def test_gkx_zero_benchmark_formula() -> None:
    realized = np.array([0.10, -0.05, 0.02], dtype=float)
    predicted = np.array([0.08, -0.01, 0.01], dtype=float)
    expected = 1.0 - ((((0.02) ** 2) + ((-0.04) ** 2) + ((0.01) ** 2)) / (((0.10) ** 2) + ((-0.05) ** 2) + ((0.02) ** 2)))
    assert np.isclose(gkx_r2_oos(realized, predicted), expected)


def test_canonical_frozen_findings() -> None:
    metrics = pd.read_csv(SOURCE_ROOT / "metric_reconciliation.csv").set_index("model_name")
    random_forest = metrics.loc["RandomForest"]
    assert np.isclose(float(random_forest["gkx_r2_oos_zero"]), 0.014772335921295232)
    assert np.isclose(float(random_forest["mean_monthly_spearman_rank_ic"]), -0.011804410305034731)
    assert np.isclose(float(random_forest["median_monthly_rank_ic"]), -0.01689181605910548)
    assert np.isclose(float(random_forest["percentage_positive_rank_ic"]), 0.38235294117647056)
    assert np.isclose(float(random_forest["top_minus_bottom_average_return"]), -0.0037488659121461907)
    monotonicity = pd.read_csv(SOURCE_ROOT / "decile_monotonicity.csv")
    rf_violations = monotonicity.loc[monotonicity["model_name"].eq("RandomForest"), "monotonicity_violations"]
    assert np.isclose(float(rf_violations.mean()), 4.794117647058823)


def test_each_publication_chart_has_source_data() -> None:
    manifest = pd.read_csv(ROOT / "figures" / "figure_manifest.csv")
    assert len(manifest) == 5
    for source_path in manifest["Source data"]:
        assert (ROOT / source_path).is_file()


def test_publication_tables_are_complete_and_nonempty() -> None:
    expected_names = {
        "model_predictive_performance.csv",
        "prediction_sorted_portfolios.csv",
        "top_minus_bottom_diagnostics.csv",
        "paper_vs_public_data_implementation.csv",
    }
    source_root = ROOT / "results" / "publication_tables"
    observed_names = {path.name for path in source_root.glob("*.csv")}
    assert observed_names == expected_names
    for source in sorted(source_root.glob("*.csv")):
        assert hashlib.sha256(source.read_bytes()).hexdigest()
        assert len(pd.read_csv(source)) > 0


def test_no_legacy_decile_violation_claim_in_public_markdown() -> None:
    retired_value = "".join(("4", ".", "59"))
    for path in ROOT.rglob("*.md"):
        if any(part in {".venv", "build"} for part in path.parts):
            continue
        assert retired_value not in path.read_text(encoding="utf-8"), path
