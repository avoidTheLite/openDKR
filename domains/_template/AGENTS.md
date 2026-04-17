# Domain Agent Entry

This is the reusable domain template. Copy this folder to `/domains/<domain-id>`.

## Read Order

1. `domain/DOMAIN_MODEL.md`
2. `domain/USE_CASES.md`
3. `routing/ROUTES.md`
4. `routing/ADJUDICATION.md`

## Routing File Charters

- `ROUTES.md` defines deterministic routing paths from domain intents to destinations (local docs, cross-domain handoffs, or approved external targets), including required context for execution.
- `ADJUDICATION.md` defines how uncertain routing decisions are resolved, including confidence thresholds, ambiguity handling, and Joan-Clode primary scoring with Jean-Claude fallback.
