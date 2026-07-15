# Synthetic sample data

`sample_panel.csv` is a deterministic, fully synthetic 54-row panel (three fictional securities across 18 months). It preserves the public input schema for validation and smoke tests but contains no observations from the research dataset and cannot reproduce the reported research results.

Generate and validate it with:

```bash
python scripts/generate_sample.py
python scripts/validate_sample.py
```

The complete market-data panel is excluded because redistribution permission was not established. See [Data access](../docs/data_access.md) for the required schema, research-run hash, and reconstruction boundary.
