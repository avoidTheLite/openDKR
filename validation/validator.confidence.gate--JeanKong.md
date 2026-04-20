# Validator Confidence Gate

Codename: JeanKong

## Purpose

Ensure routing confidence, evidence quality, and validation coverage are sufficient before final completion.

## Gate Rules

- reject outputs with missing `confidence_score`
- reject adjudicated outputs without `evidence_refs`
- reject unresolved intents without explicit fallback flag
- warn on repeated low-confidence routes and recommend deterministic promotion

## Completion Requirement

Completion is allowed only when:

- all blocking checks pass
- confidence is at or above policy floor
- required trace fields are present

## Canonical References

- `/validation/policy.decision.blocking--BananaSplitPolicy.md`
- `/validation/CI_CONTRACT.md`
