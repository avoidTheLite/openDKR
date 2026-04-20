# Router Standard Routes

## Purpose

Define deterministic route entries for normal routing when no fast-path cannon launch is used.

## Required Route Fields

- `route_id`
- `intent_pattern`
- `source_domain`
- `target_type`
- `target_ref`
- `confidence_floor`
- `required_context`
- `on_miss`

## On Miss Behavior

- `adjudicate`: send to `adjudicator.tie_break--SplitDecisionPeel.md`
- `handoff`: route to an approved cross-domain destination
- `escalate`: return unresolved with evidence

## Canonical References

- `/domains/_shared/ROUTING_CONVENTIONS.md`
- `/domains/_template/routing/ROUTES.md`
