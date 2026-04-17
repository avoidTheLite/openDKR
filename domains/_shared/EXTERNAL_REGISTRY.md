# External Registry

Approved external docs, tools, and destinations for routing.

- id: example-status-page
  type: url
  target: https://status.example.com
  owner_team: platform-ops
  trust_level: approved
  last_reviewed: 2026-04-16
  allowed_route_conditions:
    - incident triage
    - availability checks
