# Policy Decision Blocking

Codename: BananaSplitPolicy

## Purpose

Define blocking conditions that must fail validation and stop completion.

## Blocking Conditions

- unresolved internal links
- schema or contract mismatch for required routing fields
- naming convention violations for function-first stems
- missing decision trace fields in route outputs
- token budget violations above configured hard limits

## Severity Mapping

- `banana_peel`: warning, non-blocking
- `banana_split`: blocking, stop merge or completion
- `banana_complete`: pass

## Canonical References

- `/validation/CHECKS.md`
- `/validation/CI_CONTRACT.md`
