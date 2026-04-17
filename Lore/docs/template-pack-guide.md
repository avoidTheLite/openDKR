# Template Pack Guide

This guide explains how to apply the scaffold as a live repository structure and as a reusable reference pattern.

## Should This Be In-Repo or Reference-Only?

Use both:

- In-repo scaffold for immediate operational use.
- This guide as a reference for onboarding and domain rollout.

## Minimum Rollout Path

1. Keep `/domains/_shared` and `/validation` at repo root.
2. Copy `/domains/_template` into `/domains/<your-domain-id>`.
3. Fill domain model, use cases, and routing files.
4. Wire CI to enforce `/validation/CI_CONTRACT.md`.

## Multi-Domain Growth Pattern

- Start with one domain.
- Add new domain folders using `_template`.
- Add cross-domain routes in each domain's `routing/ROUTES.md`.
- Keep global standards in `_shared` to avoid drift.

## Routing File Charters

- `ROUTES.md` defines deterministic routing paths from domain intents to destinations (local docs, cross-domain handoffs, or approved external targets), including required context for execution.
- `ADJUDICATION.md` defines how uncertain routing decisions are resolved, including confidence thresholds, ambiguity handling, and Joan-Clode primary scoring with Jean-Claude fallback.
