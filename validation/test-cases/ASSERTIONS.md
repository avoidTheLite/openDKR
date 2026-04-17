# Test Case Assertions

## happy-path-internal

- exactly 1 flow in `flow_token_summary`
- `adjudication_used` is `false`
- no blocking budget violation expected

## adjudication-fallback

- exactly 1 flow in `flow_token_summary`
- `adjudication_used` is `true`
- output includes route execution for fallback route

## cross-domain-handoff

- exactly 1 flow in `flow_token_summary`
- selected target references outbound handoff docs

## heavy-context-single-file

- flow likely triggers single-file share warning or blocking violation
- top context files should include `Lore/docs/domain-Kong-(DK)_summary.md`

## mixed-provider-estimated

- exactly 2 flow rows
- one flow with provider tokens and one estimated flow
