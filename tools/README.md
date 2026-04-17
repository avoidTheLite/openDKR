# Tooling Scripts

## refresh_token_metrics.sh

CLI wrapper that refreshes token metrics using repository defaults.

### Usage

```bash
./tools/refresh_token_metrics.sh
```

### Behavior

- Archives previous latest report into `validation/reports/archive/` with a timestamp-prefixed filename.
- Regenerates `validation/reports/token-usage-latest.json`.
- Writes timestamp-prefixed history report into `validation/reports/token-usage-history/`.

## run_token_metric_test_cases.sh

Runs all routing token test fixtures and writes per-case outputs.

### Usage

```bash
./tools/run_token_metric_test_cases.sh
```

### Output

- `validation/reports/test-case-results/<case-name>/token-usage-latest.json`
- `validation/reports/test-case-results/<case-name>/flow-token-summary-latest.json`

## collect_token_metrics.py

Deterministically generates token observability reports from route trace data.

### Usage

```bash
python tools/collect_token_metrics.py \
  --repo-root . \
  --trace-file validation/reports/route-trace-latest.json \
  --budget-file validation/metrics/TOKEN_BUDGETS.md \
  --latest-output validation/reports/token-usage-latest.json \
  --history-dir validation/reports/token-usage-history \
  --archive-dir validation/reports/archive
```

### CI Flow

1. Generate route trace (`validation/reports/route-trace-latest.json`).
2. Run `collect_token_metrics.py`.
3. Publish `validation/reports/token-usage-latest.json` as CI artifact.
4. Archive timestamped history report from `validation/reports/token-usage-history/`.
5. Fail or warn build from `budget_violations` severity.
