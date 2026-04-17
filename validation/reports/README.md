# Token Report Outputs

This directory stores generated token telemetry outputs.

## Paths

- Latest snapshot: `validation/reports/token-usage-latest.json`
- Latest compact flow summary: `validation/reports/flow-token-summary-latest.json`
- History snapshots: `validation/reports/token-usage-history/<timestamp>-token-usage.json`
- Archived latest snapshots: `validation/reports/archive/<timestamp>-token-usage-latest.json`

## Latest Report Format

`token-usage-latest.json` should contain:

- `run`
- `summary`
- `route_executions`
- `file_token_breakdown`
- `budget_violations`
- `split_recommendations`
- `flow_token_summary` (compact end-to-end flow view)

## Snapshot Policy

- Every refresh archives the previous `token-usage-latest.json` into `archive/` with a timestamp-prefixed filename.
- Every refresh overwrites `token-usage-latest.json` with current data.
- Successful default-branch runs append one timestamped history snapshot.
- Retain at least 90 days of history for trend analysis.
