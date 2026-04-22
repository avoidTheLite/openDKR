# Routing Sync Validator

Use this validator to catch stale routing after a domain change has landed but related routing metadata has not been propagated.

## Required Checks

- `required_context_integrity`: every markdown path listed in route `required_context` must still exist.
- `intent_pattern_entity_alignment`: route `intent_pattern` terms should match currently valid entity or use-case identifiers from the domain.
- `cross_domain_target_existence`: every `cross_domain` route target must exist in `/registry/registry.cross_domain--BananaRepublic.md`.
- `confidence_floor_band_alignment`: route `confidence_floor` should match an allowed deterministic floor from the domain `routing/ADJUDICATION.md` policy.

## Output Shape

Each routing-sync violation should emit:

- `route_id`
- `domain_id`
- `severity`
- `violation_type`
- `stale_field`
- `expected_value`
- `actual_value`

## Suggested Enforcement

- Block on missing `required_context` files.
- Block on missing cross-domain targets.
- Warn on stale intent/entity alignment until domains expose stable indexes for entity names and use-case identifiers.
- Warn on confidence-floor drift until deterministic route floors are standardized beyond the template.