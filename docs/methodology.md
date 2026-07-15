# Methodology

This project is a public-data partial replication and extension of Gu, Kelly, and Xiu (2020), not an exact reproduction.

## Frozen experiment

- Observation: one security-month
- Target: next-month adjusted-price raw return
- Predictors: 15 price, volatility, drawdown, market-relative, and volume features
- Training: 2010-01 through 2018-04
- Validation: 2018-05 through 2021-01
- Locked test: 2021-02 through 2023-11 feature months
- Primary model: Random Forest, selected on validation only
- Refit schedule: initial forecast and each January using expanding history

Observed features are ranked within each month and mapped to `[−1, 1]`; missing ranked values are set to zero. This prevents full-panel preprocessing statistics. Target dates must follow feature dates, prediction cutoffs cannot exceed feature dates, and duplicate security-months fail validation.

## Metrics

GKX-formula stock-level OOS R-squared is:

`1 − sum((realized − predicted)^2) / sum(realized^2)`.

The benchmark is zero raw return in this adaptation. Rank IC is the monthly cross-sectional Spearman correlation. The two metrics evaluate different properties.

## Portfolios

Predictions are sorted monthly with security ID as a deterministic tie-breaker. Balanced deciles are equal weighted. The frozen spread is D10 minus D1. Portfolio returns reconstruct from constituent contributions. Turnover compares new target weights with prior return-drifted weights over entries, exits, and continuing securities.

## Inference

Monthly averages use Bartlett-kernel HAC inference with three lags. Confidence intervals use 2,000 circular moving-block bootstrap draws by calendar month, six-month blocks, and seed 20260714. Factor regressions use official FF5 plus momentum data but are descriptive over 34 months.

No model was retrained or retuned after the locked test.

