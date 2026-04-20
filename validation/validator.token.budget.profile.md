# Validator Token Budget Profile

## Purpose

Define low-token context constraints and optimization checks for routing and adjudication.

## Profile Rules

- prefer minimal required context before optional context
- fail when route total exceeds hard budget
- warn when p95 route token usage approaches hard budget
- emit split recommendations for oversized context files

## Required Outputs

- `route_token_totals`
- `route_token_p95`
- `file_token_breakdown`
- `top_context_files_by_tokens`
- `budget_violations`
- `split_recommendations`

## Canonical References

- `/validation/metrics/TOKEN_BUDGETS.md`
- `/validation/TOKEN_POLICY.md`
- `/validation/CI_CONTRACT.md`
