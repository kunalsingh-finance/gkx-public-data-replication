# Public Reproducibility Guide

## Supported verification

The public candidate verifies published aggregate results, regenerates tables/charts, and validates a fully synthetic schema sample. It does not train the frozen models because the complete market panel and stock-level derived artifacts are intentionally not redistributed.

## Environment

- Python 3.11
- Windows, macOS, or Linux
- Pinned runtime packages in `requirements-lock.txt`

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
```

On macOS/Linux, activate with `.venv/bin/python` or the shell’s standard virtual-environment command.

## Tests and smoke validation

```powershell
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python scripts\verify_public_manifest.py
.\.venv\Scripts\python scripts\generate_sample.py
.\.venv\Scripts\python scripts\validate_sample.py
```

The sample is synthetic and verifies only schema, uniqueness, dates, target timing, and deterministic calculations.

GitHub Actions runs these public checks on Linux and Windows, along with table/chart generation and link/public-tree checks. It does not fit or validate the private full-panel models. The manifest verifier checks committed artifact identities, normalizing UTF-8 text CRLF endings to LF so Windows checkouts preserve the same public identity; binary files retain exact byte hashes.

## Regenerate publication tables and charts

```powershell
.\.venv\Scripts\python scripts\generate_publication_tables.py
.\.venv\Scripts\python scripts\generate_publication_figures.py
```

The scripts read only `results/publication_source_data/`. They do not fit models or change results. Five charts and four compact publication tables are expected.

## Link and privacy checks

```powershell
.\.venv\Scripts\python scripts\check_public_links.py
.\.venv\Scripts\python scripts\scan_public_tree.py
```

## Completed-experiment provenance

- Raw panel SHA-256: `8866aae8f7240c93da20b09a2da067b827e07861bd6af1a64e1b8ad6e028a71a`
- Phase 2A protocol SHA-256: `3a1b741bdae6220711bfe32984cc313ecc5e51c4243082998aea13fa12931ada`
- Phase 2A tag: `phase2a-validity-corrected`
- Phase 2B tag: `phase2b-economic-diagnostics-complete`

## Expected limitation without private data

The public repository cannot reproduce model training, 83,985 stock-level prediction records, or constituent-level portfolio weights. It can independently verify all public headline numbers and visualizations from compact machine-readable aggregate sources. `docs/data_access.md` explains the boundary.
