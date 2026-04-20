# Runbook Incident Split Blocker

Codename: SplitHappens

## Purpose

Provide operator steps when blocking validation splits stop routing completion.

## Triage Steps

1. Identify the blocking check and affected file.
2. Confirm whether failure is contract, link, naming, or token policy related.
3. Resolve root cause and update references in the same change.
4. Re-run validation checks and confirm split is cleared.
5. Record recurring cases for deterministic route or policy improvements.

## Escalation

- If unresolved after two attempts, escalate with evidence bundle and proposed remediation.

## Canonical References

- `/validation/policy.decision.blocking--BananaSplitPolicy.md`
- `/validation/CHECKS.md`
