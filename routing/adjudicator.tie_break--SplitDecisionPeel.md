# Adjudicator Tie Break

Codename: SplitDecisionPeel

## Purpose

Resolve low-confidence or ambiguous routing outcomes when deterministic routing cannot safely decide.

## Trigger Conditions

- confidence below deterministic route floor
- score tie between candidate routes
- first occurrence with no deterministic route

## Outcome Fields

- `selected_target`
- `confidence_score`
- `fallback_used`
- `rationale`
- `evidence_refs`
- `promote_to_deterministic_route`

## Canonical References

- `/domains/_shared/ROUTING_CONVENTIONS.md`
- `/domains/_template/routing/ADJUDICATION.md`
