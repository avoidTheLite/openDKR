# Validation

Repo-level CI and content-quality checks for multi-domain documentation routing.

Agents should read `validation/AGENTS.md` before making repository updates.
Any update that changes files or structure must include reference-link updates in the same change.

Validation focuses on:

- markdown quality and required contract presence
- duplication and canonical source drift
- link health (internal and external)
- routing coverage and unresolved intent visibility
- token observability, per-route budgets, and markdown file token contribution
- AI routing analysis policy and runbooks under `validation/routing/`

## Token Metrics Pipeline

- Schema and budgets: `validation/metrics/`
- Input traces: `validation/reports/route-trace-latest.json`
- Generated reports: `validation/reports/token-usage-latest.json` and `validation/reports/token-usage-history/`
- Collector script: `tools/collect_token_metrics.py`
- Compact flow token summary: `validation/reports/flow-token-summary-latest.json`
- Routing analysis policies: `validation/routing/`
