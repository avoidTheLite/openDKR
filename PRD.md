# openDKR | Keeping requirements and code in sync

**Product requirements document · Proposed first release**

A reviewer opens a pull request that changes a product limit. CI is green. Did the team deliberately change the limit, and did a test exercise the new boundary? Today the reviewer often has to reconstruct the answer from a ticket, a diff, and a test suite. openDKR should put the requirement, its integration tests, and their results for the proposed change in one reviewable record.

## Product goal

Give a team maintaining one feature a repeatable way to decide whether the implementation still delivers the behavior it agreed to. The unit of coverage is a product promise. For a CSV importer, “reject an oversized file without saving any rows” is one such promise. An overall test pass rate tells the reviewer little about that specific outcome.

A team can adopt openDKR for a single feature while the rest of its codebase follows its existing process. The review report names the feature and the set of requirements it evaluated so readers know exactly what its verdict covers.

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

A passing 100-row test could still be linked to the revised requirement. A reviewer judges whether its assertions cover the new boundary. openDKR makes that judgment inspectable and records the evidence behind it.

The same review works when code changes first. Suppose an engineer splits the importer into batches and the 251-row test starts finding saved rows. The link to `IMPORT-01` tells the reviewer why partial writes matter. If the promise still holds, the engineer fixes the regression. If the team intends to allow partial imports, the product owner revises the promise and the engineer updates the assertions. Either decision leaves a reviewable history.

## Minimum product requirements

| Capability | Acceptance criterion |
| --- | --- |
| Identify required behavior | Each required behavior in the selected feature has a stable, unique ID and an observable outcome. Duplicate IDs make validation incomplete and the report identifies the conflict. |
| Map behavior to tests | An engineer can associate one requirement with several named integration tests and reuse a test across requirements. A reviewer can follow each link in either direction. A deleted test or unknown requirement ID produces a visible gap. |
| Bind results to a change | Each report identifies the requirements revision, the implementation commit, and the test run. A change to either revision requires fresh validation before the new pair can be reported as matching. |
| Explain the result in review | CI makes a report available from the pull request. For every required ID it lists the mapped tests, their outcomes, and a link to the run. A reviewer can identify a failing test or missing mapping directly from the report. |

The feature’s requirement list defines the coverage denominator. The report must include a required behavior even if nobody has linked a test to it yet. The implementation repository owns the mappings and executable tests. The requirement can live alongside the code or in a separate version-controlled repository.

A feature **matches** only when it has at least one required behavior, every required behavior has a valid mapping, and every mapped test passed for the revisions under review. A failed test identifies a behavioral mismatch to investigate. Missing mappings, skipped tests, and missing or stale results identify incomplete evidence. When both kinds of problem occur, the report shows both.

## What a reviewer sees

An illustrative report for **CSV import** identifies requirements revision `a12bc34`, implementation commit `d56ef78`, and CI run `42`. Each test name opens its definition, and each result opens its execution evidence.

| Requirement | Integration test | Result on this commit |
| --- | --- | --- |
| IMPORT-01 · Accept up to 250 rows and reject larger files before saving | Accept 250 rows | Passed. All 250 rows were saved. |
| IMPORT-01 · Same requirement | Reject 251 rows before saving | Failed. Expected zero saved rows and found 250. |

Here the reviewer can request a fix and cite the failed assertion. If the second test had been skipped, the reviewer would instead request a run that exercised rejection. If both tests passed but the requirement had since changed, the reviewer would request validation against the revised text. The first release supplies the evidence for that decision. The team retains its existing merge policy.

## First release and pilot

Start with one feature, its version-controlled requirements, its existing integration suite, and one CI report. Requirements and code may share a repository or live in separate repositories. Pinning both revisions supports either layout. Teams can use their existing test runner. Agent orchestration, lifecycle stages, and organization-wide dashboards are outside the first release.

### How to evaluate the pilot

Use the importer as a controlled fixture. Begin each trial from the same working baseline so the reviewer can attribute each verdict to one change.

| Trial | Expected report |
| --- | --- |
| Remove all mappings for `IMPORT-01` and leave its requirement in scope. | Incomplete. The report names the uncovered requirement even if the overall test suite passes. |
| Allow the first 250 rows of an oversized file to be saved. | Mismatch. The report identifies the rejection test and its failed assertion. |
| Provide passing results from an earlier implementation commit. Repeat with an earlier requirements revision. | Incomplete in both cases. The report identifies the stale revision. |
| Run both boundary tests successfully against the current revision pair. | Matches. Both results are traceable from `IMPORT-01`. |

**Proposed release criteria.** Every trial must produce the expected verdict. To test whether the report helps people, give three reviewers unfamiliar with the fixture a pull request and five minutes each. Ask each reviewer to identify the promised behavior, find the relevant assertion, and decide whether the evidence supports approval. Target three correct decisions with links to the supporting evidence. Record where reviewers spent their time so the team can distinguish unclear wording from hard-to-find test results.
