# Token Policy

This policy governs when routes or files should be split to reduce context cost and routing latency.

## Trigger Conditions

Create a split recommendation when any of the following occurs:

- Route exceeds `soft_budget_tokens` for 3 consecutive runs.
- Route exceeds `hard_budget_tokens` in any single run.
- A single markdown file contributes more than `single_file_share_warn` of route context.
- Route p95 token usage grows beyond `route_p95_growth_warn` over baseline.

Create a blocking violation when any of the following occurs:

- Route exceeds `hard_budget_tokens`.
- A single markdown file contributes more than `single_file_share_block`.
- Route p95 growth exceeds `route_p95_growth_block`.

## Remediation Priority

1. Split or summarize overweight markdown files.
2. Remove duplicated context and link to canonical source.
3. Narrow `required_context` in `ROUTES.md`.
4. Promote recurring adjudication outcomes to deterministic routes.

## Waiver Rules

- A blocking token violation may be waived only with a temporary decision log entry.
- Every waiver must include owner, expiry date, and remediation plan.
