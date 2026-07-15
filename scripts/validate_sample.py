"""Validate and summarize the synthetic publication sample."""

from pathlib import Path
import json

import pandas as pd

from gkx_public.core import summarize_panel


def main() -> None:
    sample_path = Path(__file__).resolve().parents[1] / "sample_data" / "sample_panel.csv"
    if not sample_path.is_file():
        raise FileNotFoundError(f"Synthetic sample is missing: {sample_path}")
    summary = summarize_panel(pd.read_csv(sample_path))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
