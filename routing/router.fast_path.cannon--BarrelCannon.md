# Router Fast Path Cannon

Codename: BarrelCannon

## Purpose

Define high-confidence workflows that can skip adjudication and dispatch directly.

## Entry Format

- `workflow_id`
- `trigger_pattern`
- `load_context`
- `fire_to`
- `confidence_floor`

## Guardrails

- Only use when confidence meets floor and trigger is unambiguous.
- If trigger does not match, fall through to `router.standard.routes.md`.
- If confidence is below floor, hand off to `adjudicator.tie_break--SplitDecisionPeel.md`.

## Canonical References

- `/domains/_shared/NAMING_CONVENTIONS.md`
- `/domains/_template/routing/ROUTES.md`
