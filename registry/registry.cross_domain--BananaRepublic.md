# Registry Cross Domain

Codename: BananaRepublic

## Purpose

Maintain the authoritative cross-domain routing registry and approved shared targets.

## Registry Records

- domain id
- owning team
- canonical barrel path
- approved handoff targets
- external target approvals

## Integrity Rules

- only approved entries can be used for cross-domain routing
- external targets must be present in shared external registry
- stale domain records must be flagged as warnings

## Canonical References

- `/domains/_shared/EXTERNAL_REGISTRY.md`
- `/domains/_shared/ROUTING_CONVENTIONS.md`
