# ROUTES

File charter: `ROUTES.md` defines deterministic routing paths from domain intents to destinations (local docs, cross-domain handoffs, or approved external targets), including required context for execution.

## Route Entries

- route_id:
  intent_pattern:
  source_domain:
  target_type: domain_doc|cross_domain|external
  target_ref:
  confidence_floor:
  required_context:
  on_miss: adjudicate|handoff|escalate

## Example

- route_id: route-known-issue-response
  intent_pattern: known issue question with product context present
  source_domain: <domain-id>
  target_type: domain_doc
  target_ref: /domains/<domain-id>/knowledge/WORKAROUNDS.md
  confidence_floor: 0.85
  required_context:
    - /domains/<domain-id>/knowledge/KNOWN_ISSUES.md
    - /domains/<domain-id>/knowledge/WORKAROUNDS.md
  on_miss: adjudicate
