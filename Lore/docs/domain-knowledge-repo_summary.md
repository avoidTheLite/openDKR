# Version 2 — Domain Knowledge Repository (DKR)
## Structured Product Domain for Agent Navigation

**Runner compatibility:** Any agent, any LLM, any runner  
**Core pattern:** Environment is the complete authority. No named orchestrator.  
**Human role:** Maintains knowledge files. Reviews flagged outputs. Approves schema changes.  
**Orchestration model:** The folder structure routes. Agents execute. Humans govern.

---

## Design Principles

No agent owns routing. The directory structure encodes the product domain completely
enough that any sufficiently capable agent can orient, execute, and produce valid output
without a named orchestrator to guide it.

The domain model is the authority. Use cases define what the product does. Contracts
define what valid execution looks like. The linter enforces consistency between them.

Agents are stateless readers. They consume what the stage provides and produce what
the contract requires. Nothing is assumed to persist between stages.

The repository is self-describing. A runner encountering this structure for the first
time should be able to determine what the product does, what work is in progress,
and what a valid output looks like — from the files alone.

---

## Folder Structure

```
/repo-root
│
├── AGENTS.md                          ← Universal entry point.
│                                         Describes: what this product does,
│                                         the domain model in plain language,
│                                         how to navigate the directory,
│                                         what to do when a file is missing,
│                                         what a valid output looks like.
│                                         No runner-specific syntax.
│                                         No tool registration.
│                                         Plain markdown only.
│
├── /domain
│   │
│   ├── USE_CASES.md                   ← Enumerated product use cases.
│   │                                     Each use case entry contains:
│   │                                       id          (UC-001, UC-002, ...)
│   │                                       actor       (who initiates)
│   │                                       precondition
│   │                                       trigger     (what starts it)
│   │                                       steps       (numbered, plain language)
│   │                                       postcondition
│   │                                       success criteria (testable)
│   │                                     Code is generated from this file.
│   │                                     Tests are validated against this file.
│   │                                     Agents navigate by use case id.
│   │
│   ├── DOMAIN_MODEL.md                ← The concepts this product operates on.
│   │                                     Each entity entry contains:
│   │                                       name
│   │                                       definition  (one precise sentence)
│   │                                       properties  (typed fields)
│   │                                       relationships (to other entities)
│   │                                       appears_in  (use case ids)
│   │                                     This is the shared vocabulary.
│   │                                     Agents resolve ambiguous terms here.
│   │
│   ├── BOUNDARIES.md                  ← What this product owns and what it does not.
│   │                                     Defines integration points.
│   │                                     Names upstream dependencies.
│   │                                     Names downstream consumers.
│   │                                     Describes failure behavior at each boundary.
│   │
│   └── DECISIONS.md                   ← Architectural and design decisions.
│                                         Each entry: decision, rationale, alternatives
│                                         considered, date, still-valid flag.
│                                         Agents read this before proposing changes.
│
├── /contracts
│   │
│   ├── INPUT.md                       ← What valid input to this system looks like.
│   │                                     Typed field definitions.
│   │                                     Required vs optional.
│   │                                     Validation rules.
│   │                                     Example payloads.
│   │
│   ├── OUTPUT.md                      ← What valid output from this system looks like.
│   │                                     Shape per resolution type.
│   │                                     Success criteria per use case.
│   │                                     What constitutes a complete artifact.
│   │
│   ├── STAGE_CONTRACTS.md             ← Per-stage input/output schemas.
│   │                                     Stage N output must satisfy Stage N+1 input.
│   │                                     Linter validates this file for consistency.
│   │                                     Format:
│   │                                       stage: 01-intake
│   │                                       input:  (schema)
│   │                                       output: (schema)
│   │                                       validation: (rules)
│   │
│   └── INTEGRATION_CONTRACTS.md      ← Contracts with external systems.
│                                         One entry per integration point named in BOUNDARIES.md.
│                                         Defines expected behavior, failure modes, timeout rules.
│
├── /knowledge
│   │
│   ├── /_shared                       ← Cross-product or cross-domain knowledge.
│   │   ├── PATTERNS.md                   Recurring patterns. Indexed by type.
│   │   └── FAILURE_MODES.md              Known failure patterns and their signatures.
│   │
│   ├── /{product-id}                  ← One folder per product or subdomain.
│   │   ├── PRODUCT_CONTEXT.md            What it does. Key concepts. Current version.
│   │   │                                  Known fragile areas. Recent changes.
│   │   ├── KNOWN_ISSUES.md               Confirmed issues. Version-tagged.
│   │   │                                  Agents read. Humans maintain.
│   │   └── WORKAROUNDS.md                Indexed by issue id from KNOWN_ISSUES.md.
│   │                                      Links back to use case ids where relevant.
│   └── README.md                      ← Navigation rules for agents.
│                                         Read product folder first.
│                                         Fall back to _shared.
│                                         Never write to knowledge files.
│
├── /generation
│   │                                  ← Artifacts derived from the domain model.
│   │                                     Generated from USE_CASES.md and DOMAIN_MODEL.md.
│   │                                     Reviewed by humans before merge.
│   │                                     Linter checks generated artifacts against
│   │                                     the source files they were generated from.
│   │
│   ├── /code                          ← Generated or agent-authored code.
│   │   └── README.md                     States which use case id each file satisfies.
│   │
│   ├── /tests                         ← Generated or agent-authored tests.
│   │   └── README.md                     States which success criteria each test covers.
│   │                                      Maps to use case id + success criteria index.
│   │
│   └── /documentation                 ← Generated documentation artifacts.
│       └── README.md                     States which use cases are covered.
│
├── /stages
│   │                                  ← Active work in progress.
│   │                                     Stage folders are transient.
│   │                                     Completed stages produce artifacts
│   │                                     that move to /generation.
│   │
│   ├── /01-intake                     ← Raw input. Source metadata preserved.
│   ├── /02-analysis                   ← Input mapped to domain model. Use case identified.
│   ├── /03-execution                  ← Agent works against contract. Output produced.
│   ├── /04-validation                 ← Output validated against STAGE_CONTRACTS.md.
│   └── /05-resolution                 ← Artifact staged. Awaits review or merge.
│
└── /log
    │
    ├── DECISIONS.md                   ← Dated log of routing and execution decisions
    │                                     made without explicit contract coverage.
    │                                     Reviewed periodically.
    │                                     Graduates to /domain/DECISIONS.md
    │                                     when pattern recurs three or more times.
    │
    └── COVERAGE.md                    ← Running record of which use cases have
                                          generated artifacts, which have tests,
                                          which have known issues open against them.
                                          Updated by CI pipeline on each merge.
```

---

## Derivation Chain

The DKR enforces a strict derivation hierarchy. Everything downstream must
be traceable to a source upstream.

```
USE_CASES.md + DOMAIN_MODEL.md
  │
  ├──► STAGE_CONTRACTS.md        (contracts derived from use case shapes)
  │
  ├──► /generation/code          (code satisfies use case steps)
  │         └── traceable to UC-id
  │
  ├──► /generation/tests         (tests validate success criteria)
  │         └── traceable to UC-id + criteria index
  │
  └──► /generation/documentation (docs describe use case behavior)
            └── traceable to UC-id
```

A generated artifact with no traceable use case id is flagged by the linter.
A use case with no generated artifacts is flagged as uncovered in COVERAGE.md.

---

## Linter Responsibilities

The CI pipeline validates the following on every push:

**Schema validation**
- Required files present per folder type
- CONTRACT fields complete and typed
- DOMAIN_MODEL entries have all required properties

**Reference resolution**
- Every use case id referenced in /generation files exists in USE_CASES.md
- Every entity referenced in STAGE_CONTRACTS.md exists in DOMAIN_MODEL.md
- Every integration point in INTEGRATION_CONTRACTS.md exists in BOUNDARIES.md

**Derivation integrity**
- Generated code files declare a use case id
- Generated test files declare a use case id and criteria index
- No artifact references a use case marked invalid or deprecated

**Coverage reporting**
- Updates COVERAGE.md on merge
- Flags use cases with no tests
- Flags use cases with no code
- Flags open known issues with no workaround

---

## Fallback Guarantee

A repository containing only AGENTS.md performs at baseline for any runner.
A repository with AGENTS.md and DOMAIN_MODEL.md answers domain questions accurately.
A repository with USE_CASES.md enables valid code and test generation.
Each additional file improves output quality and reduces agent error rate.
No missing file causes performance below baseline.
