# Agent Navigation Contract

## Purpose

This repository provides a domain-oriented documentation routing system for any agent runner.
Use folder contracts and markdown rules, not runner-specific orchestration.

## Navigation Order

1. Read `/domains/_shared/ROUTING_CONVENTIONS.md`.
2. Select the best domain under `/domains/<domain-id>`.
3. Read that domain's `AGENTS.md`.
4. Apply deterministic routes from `/routing/ROUTES.md`.
5. If confidence is low or ambiguous, apply `/routing/ADJUDICATION.md`.
6. Validate result shape against `/validation/CI_CONTRACT.md`.

## Output Contract

Each routing response should return:

- `selected_domain`
- `selected_target`
- `confidence_score`
- `fallback_used`
- `evidence_refs`

## Routing File Charters

- `ROUTES.md` defines deterministic routing paths from domain intents to destinations (local docs, cross-domain handoffs, or approved external targets), including required context for execution.
- `ADJUDICATION.md` defines how uncertain routing decisions are resolved, including confidence thresholds, ambiguity handling, and Joan-Clode primary scoring with Jean-Claude fallback.

## Missing File Behavior

- If optional files are missing, continue with baseline behavior.
- If routing information is incomplete, return best-effort output and clearly mark uncertainty.
- Never invent external targets not listed in `/domains/_shared/EXTERNAL_REGISTRY.md`.
