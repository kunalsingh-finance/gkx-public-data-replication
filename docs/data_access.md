# Data Access and Reconstruction

## What is not redistributed

The public candidate excludes:

- The complete 77,988-row public market panel and ticker universe because redistribution permission was not established.
- The GKX institutional data, which require proprietary sources and are not reconstructed by this project.
- CRSP, WRDS, Compustat, IBES, and historical membership/delisting data.
- Kenneth French ZIP downloads; obtain them from the official library.
- Full stock-level predictions and portfolio assignments because they duplicate the excluded market-return records and are large.

## Completed-experiment input

- Private filename: `sp500_price_panel_2010_2023.csv`
- SHA-256: `8866aae8f7240c93da20b09a2da067b827e07861bd6af1a64e1b8ad6e028a71a`
- Observation unit: one security-month
- Date format: ISO `YYYY-MM-DD`, month end
- Security identifier: synthetic integer local to this project; not CRSP PERMNO
- Rows: 77,988
- Securities: 497 surviving current constituents
- Dates: January 2010–November 2023

## Required schema

```text
permno                    integer-like security identifier
ticker                    string security label
DATE                      month-end date
RET                       next-month adjusted-price raw return
mom_1m
mom_3m
mom_6m
mom_12m
vol_3m
vol_6m
vol_12m
downside_vol_6m
max_drawdown_12m
price_to_12m_high
moving_average_gap_3m
moving_average_gap_6m
beta_12m_vs_spy
correlation_12m_vs_spy
average_monthly_volume
```

All 15 predictor fields and `RET` are numeric or missing. Each `(permno, DATE)` key must be unique. Dates must be monotonic within security after sorting. `RET` must represent the return realized strictly after the feature date.

## Synthetic sample

`sample_data/sample_panel.csv` is fully synthetic and exists only for schema validation and smoke tests. It is not a subset of the research data and must not be used to reproduce reported metrics.

Validate it with:

```powershell
python scripts/generate_sample.py
python scripts/validate_sample.py
```

## Reconstructing a permitted private input

Researchers may construct a similarly shaped dataset from sources they are authorized to use. They must independently comply with provider terms and document:

1. Point-in-time universe construction.
2. Adjusted-price and corporate-action conventions.
3. Monthly sampling and timezone.
4. Feature formulas and availability lags.
5. Target shift and realized-return date.
6. Missing-data behavior.
7. Dataset hash and collection timestamp.

A reconstructed dataset will not have the completed experiment’s hash and therefore constitutes a new experiment. It cannot be presented as an exact reproduction of the frozen results.

## Kenneth French factors

Official source: `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html`

Expected archives:

- `F-F_Research_Data_5_Factors_2x3_CSV.zip`
  - Completed-run SHA-256: `ddc0280b2bb8ca6c4c6ea5b68923a5549c37259bde468202108c11e812bd4241`
- `F-F_Momentum_Factor_CSV.zip`
  - Completed-run SHA-256: `37baf72ae4eace9715e8746413d0122334c63aa4083fd1c3cf2060fa04e4bd28`

Parsing uses monthly rows whose first field is `YYYYMM`, converts percentages to decimals by dividing by 100, and aligns the factor month with the realized portfolio-return month.

## What can be reproduced publicly

Without the private panel, users can:

- Verify every published headline against aggregate source CSVs.
- Regenerate five publication figures.
- Regenerate publication tables.
- Validate the synthetic schema sample.
- Run link, privacy, and deterministic smoke tests.

Full model training, stock-level prediction reconstruction, and constituent-level portfolio reconstruction require the complete private analytical inputs/artifacts and are intentionally unavailable in the public candidate.
