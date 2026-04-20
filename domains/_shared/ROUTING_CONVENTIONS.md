# Routing Conventions

## Standard Route Fields

Every route entry should include:

- `route_id`
- `intent_pattern`
- `source_domain`
- `target_type` (`domain_doc`, `cross_domain`, `external`)
- `target_ref`
- `confidence_floor`
- `required_context`
- `on_miss`

## Naming Contract

- Function-first names are required for repo-level routing and validation artifacts.
- Parsers must evaluate only the filename stem before `--`.
- Codename suffixes are optional aliases and never influence routing behavior.
- Canonical naming rules live in `/domains/_shared/NAMING_CONVENTIONS.md`.

## Standard Adjudication Fields

Every adjudication outcome should include:

- `selected_target`
- `confidence_score`
- `fallback_used`
- `rationale`
- `evidence_refs`
- `promote_to_deterministic_route`

## Routing File Charters

- `ROUTES.md` defines deterministic routing paths from domain intents to destinations (local docs, cross-domain handoffs, or approved external targets), including required context for execution.
- `ADJUDICATION.md` defines how uncertain routing decisions are resolved, including confidence thresholds, ambiguity handling, and Joan-Clode primary scoring with Jean-Claude fallback.
