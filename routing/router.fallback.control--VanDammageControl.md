# Router Fallback Control

Codename: VanDammageControl

## Purpose

Define fallback controls that reduce routing damage when confidence degrades.

## Controls

- enforce minimum confidence floor before execution
- require evidence references for non-deterministic choices
- cap retry count for repeated ambiguous inputs
- downgrade to safe unresolved response when checks fail

## Escalation Contract

- Always emit `fallback_used` and `confidence_score`.
- Route unresolved intents to `operations/runbook.incident.split_blocker--SplitHappens.md`.

## Canonical References

- `/domains/_template/routing/ADJUDICATION.md`
- `/validation/CI_CONTRACT.md`
