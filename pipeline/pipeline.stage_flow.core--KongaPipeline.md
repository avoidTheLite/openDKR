# Pipeline Stage Flow Core

Codename: KongaPipeline

## Purpose

Define the canonical routing-to-validation stage flow.

## Stage Order

1. intake
2. analysis
3. execution
4. validation
5. resolution

## Stage Contracts

- each stage output must satisfy next stage input
- stage validation must run before resolution
- unresolved validation blockers prevent completion

## Canonical References

- `/Lore/docs/domain-Kong-(DK)_summary.md`
- `/validation/CI_CONTRACT.md`
