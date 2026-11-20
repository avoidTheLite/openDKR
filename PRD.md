# openDKR | Keeping requirements and code in sync

**Product requirements document · Proposed first release**

A reviewer opens a pull request that changes a product limit. CI is green. Did the team deliberately change the limit, and did a test exercise the new boundary? Today the reviewer often has to reconstruct the answer from a ticket, a diff, and a test suite. openDKR should put the requirement, its integration tests, and their results for the proposed change in one reviewable record.

## Who uses it

A product owner describes the behavior a user should observe. An engineer links that requirement to tests that exercise the running code. During review, either person can start with the requirement and inspect the evidence, or start with a test and find the product decision it protects.

## A change from start to finish

Consider a CSV importer. The team raises its import limit from 100 rows to 250. The engineer updates the implementation. The old test still passes because it only tries a 100-row file.

The product owner revises requirement `IMPORT-01` to say “Accept up to 250 data rows. Reject larger files before saving any rows.” The ID stays the same so its history and test links survive the edit. During review, the engineer and product owner agree that two cases exercise the boundary.

| Requirement | Mapped integration test | Observable result |
| --- | --- | --- |
| IMPORT-01 | Import a file with 250 data rows | The import succeeds and all 250 rows are saved. |
| IMPORT-01 | Import a file with 251 data rows | The import returns a limit error and zero rows are saved. |

CI runs both tests against the proposed code revision. If the second test finds 250 saved rows, the reviewer sees exactly which promise failed. After the fix, both tests pass on the new commit and the reviewer can follow the results back to the requirement. If the limit changes again, the same links identify the tests to revisit.

This example also defines the limit of the tool. A passing 100-row test could still be linked to the revised requirement. A reviewer judges whether its assertions cover the new boundary. openDKR makes that judgment inspectable and records the evidence behind it.

## Minimum product requirements

| Capability | Acceptance criterion |
| --- | --- |
| Identify required behavior | Each required behavior in the selected feature has a stable, unique ID and an observable outcome. Duplicate IDs make validation incomplete and the report identifies the conflict. |
| Map behavior to tests | An engineer can associate one requirement with several named integration tests and reuse a test across requirements. A reviewer can follow each link in either direction. A deleted test or unknown requirement ID produces a visible gap. |
| Bind results to a change | Each report identifies the requirements revision, the implementation commit, and the test run. A change to either revision requires fresh validation before the new pair can be reported as matching. |
| Explain the result in review | CI makes a report available from the pull request. For every required ID it lists the mapped tests, their outcomes, and a link to the run. A reviewer can identify a failing test or missing mapping directly from the report. |

A feature **matches** only when it has at least one required behavior, every required behavior has a valid mapping, and every mapped test passed for the revisions under review. A failed test identifies a behavioral mismatch to investigate. Missing mappings, skipped tests, and missing or stale results identify incomplete evidence. When both kinds of problem occur, the report shows both.

## First release and pilot

Start with one feature, its version-controlled requirements, its existing integration suite, and one CI report. Requirements and code may share a repository or live in separate repositories. Pinning both revisions supports either layout. Teams can use their existing test runner. Agent orchestration, lifecycle stages, and organization-wide dashboards are outside the first release.

The pilot succeeds when a reviewer unfamiliar with the feature can answer three questions from the pull request: What behavior changed? Which tests exercised it? What happened on this commit? Verify the report with four controlled changes: remove a mapping, break a mapped assertion, supply a result from an older commit, then restore the mapping and pass both boundary tests on the current commit. Only the final case should report a match.
