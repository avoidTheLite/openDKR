# Routing Validation Runbook

## 1) Generate telemetry

Run:

```bash
./tools/refresh_token_metrics.sh
```

## 2) Review compact flow costs

Open:

- `validation/reports/flow-token-summary-latest.json`

Use this to quickly inspect end-to-end flow token totals.

## Evaluation Rules

- Flag routes exceeding soft or hard token budgets.
- Flag routes with sustained p95 growth above threshold.
- Flag routes with repeated adjudication fallback.
- Flag markdown files exceeding single-file contribution thresholds.
- Flag duplicated high-token files that should canonicalize.

## 3) Review violations and causes

Open:

- `validation/reports/token-usage-latest.json`

Focus on:

- `budget_violations`
- `split_recommendations`
- top markdown contributors

## 4) Propose and apply route improvements

Update:

- `domains/<domain-id>/routing/ROUTES.md`
- `domains/<domain-id>/routing/ADJUDICATION.md`

Allowed recommendation types:

- split oversized markdown context files
- summarize context and link to canonical sources
- narrow route `required_context` sets
- promote recurrent adjudication outcomes into deterministic routes

Recommendation priority:

1. blocking budget violations
2. repeated soft budget overruns
3. high single-file share issues
4. p95 growth regressions

## 5) Re-run and compare

Re-run telemetry and compare flow totals with prior history snapshots.
