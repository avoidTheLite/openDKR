# Token Observability Schema

This file is the source-of-truth schema for routing token telemetry.

## Run-Level Fields

- `run_id`: unique id for a telemetry run.
- `timestamp`: ISO-8601 run timestamp.
- `repo_sha`: commit sha at measurement time.
- `runner`: runner identifier (`cursor`, `copilot`, `claude_code`, or custom).
- `model`: optional model name/version.
- `token_source`: `provider_reported` or `estimated`.

## Route Execution Fields

Each route execution record should include:

- `domain_id`
- `route_id`
- `selected_target`
- `adjudication_used` (`true`/`false`)
- `confidence_score`
- `latency_ms`
- `prompt_tokens` (optional when provider does not expose)
- `completion_tokens` (optional when provider does not expose)
- `total_tokens` (required for all runs, provider value or estimate)

## File Token Breakdown Fields

Each markdown context file should include:

- `file_path`
- `file_type` (`markdown`)
- `raw_char_count`
- `estimated_tokens`
- `percent_of_route_context`
- `included_by` (`route_required_context` or `adjudication_context`)

## Derived Summary Fields

- `route_token_totals`: totals by route id.
- `route_token_p95`: p95 token count per route id.
- `top_context_files_by_tokens`: highest token files across the run.
- `budget_violations`: policy violations from `TOKEN_BUDGETS.md`.
- `routing_sync_violations`: stale routing findings such as missing required context, missing cross-domain targets, stale intent terms, or confidence floor drift.
- `split_recommendations`: route/file split suggestions generated from thresholds.
- `flow_token_summary`: compact end-to-end flow rows for quick token review.

## Estimation Rule

If provider token usage is unavailable, estimate tokens from file content consistently and mark records with `token_source: estimated`.
All estimated runs must keep `raw_char_count` and `estimated_tokens` for comparability across runners.
