# Routing Recommendation Output Contract

Every recommendation batch should include:

- `domain_id`
- `route_id`
- `flow_id`
- `offending_files`
- `proposed_change`
- `expected_token_reduction`
- `confidence`
- `policy_trigger`

Compact flow reporting output should include:

- `run`
- `flow_token_summary` (list of end-to-end flow token entries)
