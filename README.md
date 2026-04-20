# Multi-Domain Documentation Routing Scaffold

This repository now includes a runner-agnostic template pack for documentation-as-code routing.

## What This Is

- A reusable structure for multi-domain markdown systems.
- Compatible with Copilot, Claude, Cursor, and other agent runners.
- Designed so a single team can run one domain standalone, then expand to many domains.

## Navigation

1. Start with `AGENTS.md`.
2. Read `/domains/_shared/ROUTING_CONVENTIONS.md` and `/domains/_shared/NAMING_CONVENTIONS.md`.
3. Copy `/domains/_template` to create a real domain folder.
4. Implement deterministic and fallback routing in:
   - `/domains/<domain-id>/routing/ROUTES.md`
   - `/domains/<domain-id>/routing/ADJUDICATION.md`
5. Use root function-first routing docs in `/routing/` for repo-level orchestration.
6. Use `/validation` for CI checks, duplication detection, and coverage reporting.

## Routing File Charters

- `ROUTES.md` defines deterministic routing paths from domain intents to destinations (local docs, cross-domain handoffs, or approved external targets), including required context for execution.
- `ADJUDICATION.md` defines how uncertain routing decisions are resolved, including confidence thresholds, ambiguity handling, and Joan-Clode primary scoring with Jean-Claude fallback.

## Scaffold Layout

- `/domains/_shared` for global conventions and approved external targets.
- `/domains/_template` for the standard per-domain blueprint.
- `/validation` for repo-level CI content quality controls.

## Reference Guide

See `Lore/docs/template-pack-guide.md` for implementation guidance and rollout order.

## Install And Run Token Metrics

### Prerequisites

- Python 3.10+ available as `python3`.
- A route trace file at `validation/reports/route-trace-latest.json`.

### One-Command Refresh

Run:

```bash
./tools/refresh_token_metrics.sh
```

This will:

- archive the previous `validation/reports/token-usage-latest.json` into `validation/reports/archive/` with a timestamp-prefixed filename
- write a fresh latest report to `validation/reports/token-usage-latest.json`
- write a compact flow summary to `validation/reports/flow-token-summary-latest.json`
- write a timestamp-prefixed history snapshot to `validation/reports/token-usage-history/`

### Run Token Test Cases

```bash
./tools/run_token_metric_test_cases.sh
```

This executes the routing token fixtures under `validation/test-cases/` and generates per-case full + compact flow reports.
