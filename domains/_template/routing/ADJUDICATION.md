# ADJUDICATION

File charter: `ADJUDICATION.md` defines how uncertain routing decisions are resolved, including confidence thresholds, ambiguity handling, and Joan-Clode primary scoring with Jean-Claude fallback.

## Confidence Bands

- high: >= 0.85
- medium: 0.60-0.84
- low: < 0.60

## Adjudication Policy

1. Joan-Clode scores candidate routes first.
2. If score is high and unambiguous, route directly.
3. If low confidence, tie, or first occurrence, invoke Jean-Claude.
4. Log decision for later promotion into deterministic routes.

## Required Outcome

- selected_target:
- confidence_score:
- fallback_used:
- rationale:
- evidence_refs:
- promote_to_deterministic_route:
