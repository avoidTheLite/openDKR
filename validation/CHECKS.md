# Validation Checks

## Required Checks

- schema_completeness
- required_file_presence
- broken_internal_links
- stale_external_links
- reference_link_updates_on_change
- duplicate_content_clusters
- routing_coverage
- route_token_budget_checks
- compact_flow_token_summary_present
- function_first_naming_convention
- codename_without_function_prefix

## Severity

- warning: banana_peel
- blocking: banana_split
- pass: banana_complete

## Naming Validation Rules

- A markdown artifact name must begin with a canonical function stem from `/domains/_shared/NAMING_CONVENTIONS.md`.
- If `--` is present, text after it is treated as codename only.
- A codename-only filename is a blocking `banana_split`.
