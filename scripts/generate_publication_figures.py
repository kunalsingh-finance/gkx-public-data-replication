"""Regenerate five publication charts from committed aggregate source CSVs."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def _finish(path: Path, title: str, x_label: str, y_label: str) -> None:
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()


def _format_month_axis() -> None:
    axis = plt.gca()
    axis.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))


def _figure_one(source_root: Path, output_root: Path) -> None:
    source = pd.read_csv(source_root / "figure_1_model_oos_r2.csv")
    plt.figure(figsize=(8, 4.6))
    colors = ["#2F5597" if model == "RandomForest" else "#9FBAD0" for model in source["model_name"]]
    plt.bar(source["model_name"], source["gkx_r2_oos_zero"] * 100.0, color=colors)
    plt.axhline(0.0, color="black", linewidth=0.8)
    _finish(output_root / "figure_1_model_oos_r2.png", "Locked-test stock-level OOS R-squared by model", "Model", "GKX-formula OOS R-squared (%)")


def _figure_two(source_root: Path, output_root: Path) -> None:
    source = pd.read_csv(source_root / "figure_2_random_forest_deciles.csv")
    plt.figure(figsize=(7.5, 4.8))
    plt.plot(source["decile"], source["average_prediction"] * 100.0, marker="o", label="Average prediction")
    plt.plot(source["decile"], source["average_realized_return"] * 100.0, marker="o", label="Average realized return")
    plt.xticks(range(1, 11))
    plt.legend()
    _finish(output_root / "figure_2_random_forest_deciles.png", "Random Forest prediction sorts were not monotonic", "Predicted-return decile (1 = lowest, 10 = highest)", "Average monthly return (%)")


def _figure_three(source_root: Path, output_root: Path) -> None:
    source = pd.read_csv(source_root / "figure_3_random_forest_rank_ic.csv", parse_dates=["date"])
    plt.figure(figsize=(8.5, 4.8))
    plt.plot(source["date"], source["spearman_rank_ic"], color="#9FBAD0", marker="o", markersize=3, label="Monthly rank IC")
    plt.plot(source["date"], source["rolling_12_month_rank_ic"], color="#C00000", linewidth=2.0, label="Rolling 12-month mean")
    plt.axhline(0.0, color="black", linewidth=0.8)
    plt.legend()
    _format_month_axis()
    _finish(output_root / "figure_3_random_forest_rank_ic.png", "Random Forest cross-sectional rank IC was unstable", "Realized-return month", "Spearman rank IC")


def _figure_four(source_root: Path, output_root: Path) -> None:
    source = pd.read_csv(source_root / "figure_4_random_forest_cumulative_spread.csv", parse_dates=["realized_return_date"])
    plt.figure(figsize=(8.5, 4.8))
    plt.plot(source["realized_return_date"], source["cumulative_return"] * 100.0, color="#C00000", linewidth=2.0)
    plt.axhline(0.0, color="black", linewidth=0.8)
    _format_month_axis()
    _finish(output_root / "figure_4_random_forest_cumulative_spread.png", "Random Forest D10-minus-D1 portfolio lost money", "Realized-return month", "Cumulative compounded return (%)")


def _figure_five(source_root: Path, output_root: Path) -> None:
    source = pd.read_csv(source_root / "figure_5_random_forest_cost_sensitivity.csv", parse_dates=["realized_return_date"])
    plt.figure(figsize=(8.5, 4.8))
    for cost, group in source.groupby("cost_bps_one_way", sort=True):
        plt.plot(group["realized_return_date"], group["cumulative_net_return"] * 100.0, label=f"{int(cost)} bps")
    plt.axhline(0.0, color="black", linewidth=0.8)
    plt.legend(title="One-way cost", ncol=3)
    _format_month_axis()
    _finish(output_root / "figure_5_random_forest_cost_sensitivity.png", "Costs weakened an already negative Random Forest spread", "Realized-return month", "Cumulative net return (%)")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    source_root = root / "results" / "publication_source_data"
    output_root = root / "build" / "figures"
    output_root.mkdir(parents=True, exist_ok=True)
    _figure_one(source_root, output_root)
    _figure_two(source_root, output_root)
    _figure_three(source_root, output_root)
    _figure_four(source_root, output_root)
    _figure_five(source_root, output_root)


if __name__ == "__main__":
    main()
