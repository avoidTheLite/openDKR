# Validation Agent Instructions

Agents working in this repository must treat reference links as part of the contract.

## Required Behavior On Every Update

1. Update any changed or moved file references in markdown links during the same change.
2. Keep internal references resolvable after rename, move, or structure updates.
3. Replace outdated external targets with approved entries from `/domains/_shared/EXTERNAL_REGISTRY.md`.
4. Do not leave stale references for a follow-up change.
5. Use function-first file names for new validation or routing docs per `/domains/_shared/NAMING_CONVENTIONS.md`.

## Enforcement

- The validation linter checks link integrity and will flag stale references.
- Unresolved internal links are blocking issues.
- Naming violations where codename replaces function stem are blocking issues.

## Token Optimization

Agents should use `validation/routing/` policies and runbook after token reports are generated.
High-token routes and oversized markdown files should be converted into concrete split/prune recommendations.
