"""Pure validation and metric functions for the publication-safe sample."""

from pathlib import Path
from typing import TypedDict

import numpy as np
import pandas as pd


EXPECTED_COLUMNS: tuple[str, ...] = (
    "permno", "ticker", "DATE", "RET", "mom_1m", "mom_3m", "mom_6m", "mom_12m",
    "vol_3m", "vol_6m", "vol_12m", "downside_vol_6m", "max_drawdown_12m",
    "price_to_12m_high", "moving_average_gap_3m", "moving_average_gap_6m",
    "beta_12m_vs_spy", "correlation_12m_vs_spy", "average_monthly_volume",
)


class PanelSummary(TypedDict):
    rows: int
    securities: int
    months: int
    first_date: str
    last_date: str


def validate_panel(panel: pd.DataFrame) -> pd.DataFrame:
    """Return a validated copy of a stock-month panel."""
    missing_columns = sorted(set(EXPECTED_COLUMNS).difference(panel.columns))
    if missing_columns:
        raise ValueError(f"Panel is missing required columns: {missing_columns}")
    validated = panel.loc[:, EXPECTED_COLUMNS].copy()
    validated["DATE"] = pd.to_datetime(validated["DATE"], errors="raise")
    if validated[["permno", "DATE"]].duplicated().any():
        raise ValueError("Panel contains duplicate security-month keys")
    sorted_panel = validated.sort_values(["permno", "DATE"], kind="stable").reset_index(drop=True)
    for _, group in sorted_panel.groupby("permno", sort=False):
        if not group["DATE"].is_monotonic_increasing:
            raise ValueError("Panel dates are not monotonic within security")
    return sorted_panel


def gkx_r2_oos(realized_returns: np.ndarray, predictions: np.ndarray) -> float:
    """Calculate GKX zero-return-benchmark out-of-sample R-squared."""
    if realized_returns.shape != predictions.shape:
        raise ValueError("Realized returns and predictions must have identical shapes")
    denominator = float(np.square(realized_returns).sum())
    if denominator == 0.0:
        raise ValueError("GKX R-squared denominator is zero")
    numerator = float(np.square(realized_returns - predictions).sum())
    return 1.0 - (numerator / denominator)


def summarize_panel(panel: pd.DataFrame) -> PanelSummary:
    """Summarize a validated panel without mutating it."""
    validated = validate_panel(panel)
    return {
        "rows": int(len(validated)),
        "securities": int(validated["permno"].nunique()),
        "months": int(validated["DATE"].nunique()),
        "first_date": validated["DATE"].min().date().isoformat(),
        "last_date": validated["DATE"].max().date().isoformat(),
    }


def read_panel(path: Path) -> pd.DataFrame:
    """Read and validate a panel from a CSV path."""
    if not path.is_file():
        raise FileNotFoundError(f"Panel file does not exist: {path}")
    return validate_panel(pd.read_csv(path))
