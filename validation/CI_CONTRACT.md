# CI Contract

CI should emit structured results for documentation routing quality.

## Required Output Fields

- total_checks
- warnings_count
- blocking_errors_count
- duplicate_clusters
- unresolved_internal_links
- unresolved_external_links
- reference_link_update_violations
- uncovered_routes
- report_location
- route_token_totals
- route_token_p95
- file_token_breakdown
- top_context_files_by_tokens
- budget_violations
- split_recommendations
- token_report_latest_path
- token_report_history_path
- flow_token_summary
- flow_token_summary_latest_path

## Route Decision Trace Requirements

Each routed execution should be traceable with:

- selected_domain
- route_id
- selected_target
- confidence_score
- fallback_used
- evidence_refs

## Token Reporting Contract

- If provider token telemetry is available, emit provider values and set `token_source=provider_reported`.
- If unavailable, emit estimated values and set `token_source=estimated`.
- Include markdown file-level contribution records so split decisions can be mapped to specific files.
- Emit a compact flow token summary so end-to-end routing costs can be reviewed with fewer attributes.
- `routing_coverage` should include unresolved intent reporting to avoid duplicate unresolved-intent outputs.
