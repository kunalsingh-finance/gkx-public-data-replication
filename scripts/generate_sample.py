"""Generate a deterministic, fully synthetic panel for public smoke tests."""

from pathlib import Path
import math

import pandas as pd

from gkx_public.core import EXPECTED_COLUMNS, validate_panel


def build_synthetic_panel() -> pd.DataFrame:
    """Return a schema-compatible panel with no research observations."""
    dates = pd.date_range("2020-01-31", periods=18, freq="ME")
    records: list[dict[str, object]] = []
    for security_index, ticker in enumerate(("SYN_A", "SYN_B", "SYN_C"), start=1):
        for month_index, date in enumerate(dates, start=1):
            phase = float(security_index * 10 + month_index)
            record: dict[str, object] = {
                "permno": 900000 + security_index,
                "ticker": ticker,
                "DATE": date.date().isoformat(),
                "RET": round(0.005 * math.sin(phase), 8),
                "mom_1m": round(0.01 * math.cos(phase), 8),
                "mom_3m": round(0.012 * math.cos(phase / 2.0), 8),
                "mom_6m": round(0.014 * math.sin(phase / 3.0), 8),
                "mom_12m": round(0.016 * math.cos(phase / 4.0), 8),
                "vol_3m": round(0.02 + 0.001 * security_index, 8),
                "vol_6m": round(0.025 + 0.001 * security_index, 8),
                "vol_12m": round(0.03 + 0.001 * security_index, 8),
                "downside_vol_6m": round(0.018 + 0.001 * security_index, 8),
                "max_drawdown_12m": round(-0.05 - 0.002 * month_index, 8),
                "price_to_12m_high": round(0.85 + 0.005 * month_index, 8),
                "moving_average_gap_3m": round(0.01 * math.sin(phase / 2.0), 8),
                "moving_average_gap_6m": round(0.01 * math.cos(phase / 3.0), 8),
                "beta_12m_vs_spy": round(0.8 + 0.05 * security_index, 8),
                "correlation_12m_vs_spy": round(0.4 + 0.02 * security_index, 8),
                "average_monthly_volume": float(1_000_000 + security_index * 100_000 + month_index * 1_000),
            }
            records.append(record)
    panel = pd.DataFrame.from_records(records, columns=EXPECTED_COLUMNS)
    return validate_panel(panel)


def main() -> None:
    output_path = Path(__file__).resolve().parents[1] / "sample_data" / "sample_panel.csv"
    build_synthetic_panel().to_csv(output_path, index=False, date_format="%Y-%m-%d")


if __name__ == "__main__":
    main()
