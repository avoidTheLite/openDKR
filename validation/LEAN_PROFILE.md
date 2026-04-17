# Lean Validation Profile

This file classifies validation assets into keep, merge, relocate, and remove buckets for a balanced footprint.

## Keep (Core)

- `validation/README.md`
- `validation/AGENTS.md`
- `validation/CHECKS.md`
- `validation/CI_CONTRACT.md`
- `validation/LINK_HEALTH.md`
- `validation/metrics/SCHEMA.md`
- `validation/metrics/TOKEN_BUDGETS.md`
- `validation/reports/README.md`
- `validation/routing/README.md`
- `validation/routing/RUNBOOK.md`
- `validation/routing/OUTPUT_CONTRACT.md`

## Merge

- `validation/routing/INPUTS.md` -> merged into `validation/routing/RUNBOOK.md`
- `validation/routing/EVALUATION_RULES.md` -> merged into `validation/routing/RUNBOOK.md`
- `validation/routing/RECOMMENDATION_POLICY.md` -> merged into `validation/routing/RUNBOOK.md`

## Relocate

- `validation/routing/test-cases/*` -> `validation/test-cases/*`

## Remove (After Consolidation)

- `validation/AGENT_OPTIMIZATION_LOOP.md`
- `validation/routing/INPUTS.md`
- `validation/routing/EVALUATION_RULES.md`
- `validation/routing/RECOMMENDATION_POLICY.md`
