# Validation Checks

## Required Checks

- schema_completeness
- required_file_presence
- broken_internal_links
- stale_external_links
- reference_link_updates_on_change
- duplicate_content_clusters
- routing_coverage
- required_context_integrity
- intent_pattern_entity_alignment
- cross_domain_target_existence
- confidence_floor_band_alignment
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

## Routing Sync Validation Rules

- `required_context_integrity` is blocking when a route still points at a removed or moved markdown file.
- `cross_domain_target_existence` is blocking when a cross-domain handoff target is not present in the approved registry.
- `intent_pattern_entity_alignment` is warning-level until domains start carrying stable entity and use-case indexes.
- `confidence_floor_band_alignment` is warning-level and should match allowed floors defined by the domain adjudication policy.
- Routing-sync checks are defined in `/validation/validator.routing.sync.md`.
