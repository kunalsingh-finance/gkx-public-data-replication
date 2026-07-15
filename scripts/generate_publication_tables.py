"""Recreate publication tables from committed aggregate source artifacts."""

from pathlib import Path
import shutil


TABLE_NAMES: tuple[str, ...] = (
    "model_predictive_performance.csv",
    "prediction_sorted_portfolios.csv",
    "top_minus_bottom_diagnostics.csv",
    "paper_vs_public_data_implementation.csv",
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    source_root = root / "results" / "publication_tables"
    output_root = root / "build" / "publication_tables"
    output_root.mkdir(parents=True, exist_ok=True)
    for name in TABLE_NAMES:
        source = source_root / name
        if not source.is_file():
            raise FileNotFoundError(f"Publication table source is missing: {source}")
        shutil.copyfile(source, output_root / name)


if __name__ == "__main__":
    main()
