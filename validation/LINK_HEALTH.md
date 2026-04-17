# Link Health

## Internal Links

- all relative markdown links must resolve
- unresolved internal links are blocking
- any file move/rename requires link updates in the same change set

## External Links

- validate on CI cadence or scheduled checks
- unavailable external links are warning-level findings until review window expires
- deprecated targets should be replaced with approved registry entries

## Agent Update Discipline

- agents must update stale references immediately when editing related files
- link fixes should not be deferred to a later PR
