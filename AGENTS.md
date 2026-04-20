# Agent Navigation Contract

## Purpose

This repository provides a domain-oriented documentation routing system for any agent runner.
Use folder contracts and markdown rules, not runner-specific orchestration.

## Navigation Order

1. Read `/domains/_shared/ROUTING_CONVENTIONS.md`.
2. Read `/domains/_shared/NAMING_CONVENTIONS.md`.
3. Select the best domain under `/domains/<domain-id>`.
4. Read that domain's `AGENTS.md`.
5. Apply deterministic routes from `/routing/router.standard.routes.md`.
6. If a fast-path trigger matches, use `/routing/router.fast_path.cannon--BarrelCannon.md`.
7. If confidence is low or ambiguous, apply `/routing/adjudicator.tie_break--SplitDecisionPeel.md`.
8. Apply fallback controls from `/routing/router.fallback.control--VanDammageControl.md`.
9. Validate result shape against `/validation/CI_CONTRACT.md`.

## Output Contract

Each routing response should return:

- `selected_domain`
- `selected_target`
- `confidence_score`
- `fallback_used`
- `evidence_refs`

## Routing File Charters

- `router.standard.routes.md` defines deterministic routing paths from domain intents to destinations (local docs, cross-domain handoffs, or approved external targets), including required context for execution.
- `router.fast_path.cannon--BarrelCannon.md` defines high-confidence launch paths that skip adjudication.
- `adjudicator.tie_break--SplitDecisionPeel.md` defines how uncertain routing decisions are resolved, including confidence thresholds, ambiguity handling, and Joan-Clode primary scoring with Jean-Claude fallback.

## Naming Parse Rules

- Parse only the filename stem before `--`.
- Treat codename suffixes as non-functional aliases.
- Reject codename-only filenames during validation.

## Missing File Behavior

- If optional files are missing, continue with baseline behavior.
- If routing information is incomplete, return best-effort output and clearly mark uncertainty.
- Never invent external targets not listed in `/domains/_shared/EXTERNAL_REGISTRY.md`.
