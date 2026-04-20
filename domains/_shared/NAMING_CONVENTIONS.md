# Naming Conventions

This repository uses function-first names so agents can infer behavior without relying on lore-specific aliases.

## Naming Principle

Every artifact name has two parts:

- required functional stem for deterministic parsing
- optional codename suffix for human readability

File format:

- `<function>.<scope?>.<type>--<codename>.md`

Rules:

- Parse only the segment before `--` for automation.
- Treat codename as display-only metadata.
- Do not route from codename text.
- Use lowercase dot-separated stems.

## Canonical Function Vocabulary

- `router`: deterministic target selection
- `adjudicator`: confidence-based fallback decisioning
- `validator`: contract and quality gate enforcement
- `policy`: pass/fail criteria and thresholds
- `pipeline`: ordered stage flow definitions
- `registry`: authoritative cross-domain index
- `runbook`: operator incident and recovery steps
- `profile`: optimization profile and budget tuning

## Approved Codenames

- `VanDammageControl`: fallback control behavior
- `SplitDecisionPeel`: low-confidence tie-break adjudication
- `BananaSplitPolicy`: blocking decision policy
- `BananaRepublic`: cross-domain registry alias
- `SplitHappens`: incident runbook alias
- `KongaPipeline`: stage flow alias
- `BarrelCannon`: fast-path route launcher alias
- `JeanKong`: validation gatekeeper alias

## Examples

- `router.fast_path.cannon--BarrelCannon.md`
- `router.fallback.control--VanDammageControl.md`
- `adjudicator.tie_break--SplitDecisionPeel.md`
- `validator.confidence.gate--JeanKong.md`
- `policy.decision.blocking--BananaSplitPolicy.md`
