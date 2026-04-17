# Token Budgets

Default budgets are intentionally conservative and should be tuned per domain.

## Per-Route Budgets

- `soft_budget_tokens`: 6000 (warning)
- `hard_budget_tokens`: 9000 (blocking unless explicitly waived)
- `adjudication_soft_budget_tokens`: 7500 (warning)
- `adjudication_hard_budget_tokens`: 11000 (blocking unless explicitly waived)

## Per-File Contribution Thresholds

- `single_file_share_warn`: 0.40
- `single_file_share_block`: 0.60
- `single_file_estimated_tokens_warn`: 2500
- `single_file_estimated_tokens_block`: 4000

These thresholds apply to markdown files loaded from `required_context` and adjudication context sets.

## Growth Thresholds

- `route_p95_growth_warn`: 0.20
- `route_p95_growth_block`: 0.35

Growth is measured against the current baseline window in report history.
