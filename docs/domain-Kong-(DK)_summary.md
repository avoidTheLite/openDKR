# Version 3 — Domain Kong (DK)
## The Agent-Navigable Product Repository

**Runner compatibility:** Any agent, any LLM, any runner  
**Core pattern:** The Kong is the authority. Agents navigate it. Funky keeps it honest.  
**Human role:** Feeds the Kong. Reviews Funky's flagged peels and splits. Approves merges.  
**Orchestration model:** The Barrel routes. The Kong answers. Kremlings don't get through.

---

## The Naming System

```
Kong              The repository itself. The domain gateway.
                  What the product is, what it does, how it works.
                  Agents don't query the codebase directly — they go through the Kong.

Barrel            AGENTS.md. The single entry point. The re-export of the domain surface.
                  Every Kong needs exactly one. Drop it at the root.
                  Named for the barrel file pattern: one entry point, internals stay internal.

Barrel Cannon     A compressed routing file that doesn't walk through stages.
                  Loads context and fires an agent directly to its destination.
                  Used for high-confidence, well-understood workflows.
                  The cannon doesn't route — it launches.

Bananas           Completed, well-formed knowledge artifacts.
                  One banana per qualifying file.
                  Coverage metric: how many bananas does this Kong have?

Banana Peel       A linter warning. Something that will cause a slip if not addressed.
                  Unresolved reference. Empty knowledge folder. Untested use case.

Banana Split      A linter error. Incompatibility detected. Blocks merge.
                  Broken reference. Schema violation. Contract mismatch.

Banana Hoard      The org-scale registry. All Kongs indexed. All bananas counted.
                  The hoard knows every Kong in the org and their relationships.

Cranky            The institutional memory layer. Grumpy. Always right.
                  Decision logs. First occurrence records. Routing history.
                  Ask Cranky before opening a new issue.

Funky             The DX tooling agent. Runs the shop. Gives you what you need.
                  Linter + workspace builder + coverage reporter combined.
                  "Run it through Funky" = validate the Kong.

Kremlings         Bad actors. Prompt injection. Corrupted signals. Stale references.
                  What Funky is partially defending against.

K. Rool           What a Kong becomes when no one feeds it.
                  Stale knowledge. Broken references. Routing rules that no longer match reality.
                  "This Kong has gone K. Rool."
```

---

## Folder Structure

```
/repo-root  (the Kong)
│
├── AGENTS.md                          ← The Barrel.
│                                         Universal entry point. Read this first.
│                                         Every runner orients here.
│                                         Describes the Kong's domain, what it does,
│                                         how to navigate, and how to behave
│                                         when a file is missing.
│                                         No runner-specific syntax. Plain markdown only.
│                                         The barrel for the domain surface.
│
├── BARREL_CANNON.md                   ← Compressed routing for known workflows.
│                                         High-confidence paths only.
│                                         Format per entry:
│                                           workflow_id
│                                           trigger_pattern
│                                           load_context  (files to read before executing)
│                                           fire_to       (exact destination: stage or agent)
│                                           confidence_floor  (minimum to use this cannon)
│                                         Ambiguous signals do not use the cannon.
│                                         The cannon doesn't decide — it launches.
│
├── /domain                            ← What the Kong knows about the product.
│   │
│   ├── USE_CASES.md                   ← 🍌 What the product does.
│   │                                     Discrete, enumerated use cases.
│   │                                     Each entry:
│   │                                       id           (UC-001, UC-002, ...)
│   │                                       actor
│   │                                       precondition
│   │                                       trigger
│   │                                       steps        (numbered, plain language)
│   │                                       postcondition
│   │                                       success_criteria  (testable)
│   │                                     Code derives from this file.
│   │                                     Tests validate against this file.
│   │
│   ├── DOMAIN_MODEL.md                ← 🍌 The concepts the product operates on.
│   │                                     Each entity:
│   │                                       name
│   │                                       definition   (one precise sentence)
│   │                                       properties   (typed)
│   │                                       relationships
│   │                                       appears_in   (UC ids)
│   │                                     The shared vocabulary.
│   │                                     Agents resolve ambiguity here.
│   │
│   ├── BOUNDARIES.md                  ← 🍌 What the Kong owns and what it doesn't.
│   │                                     Integration points. Upstream dependencies.
│   │                                     Downstream consumers. Failure behavior.
│   │
│   └── DECISIONS.md                   ← 🍌 Why things are the way they are.
│                                         Decision + rationale + alternatives + date.
│                                         Agents read before proposing changes.
│
├── /contracts                         ← How the Kong behaves at its edges.
│   │
│   ├── INPUT.md                       ← 🍌 Valid input shape. Typed fields.
│   │                                     Required vs optional. Validation rules.
│   │                                     Example payloads.
│   │
│   ├── OUTPUT.md                      ← 🍌 Valid output shape per resolution type.
│   │                                     Success criteria per use case.
│   │                                     What a complete artifact looks like.
│   │
│   ├── STAGE_CONTRACTS.md             ← 🍌 Per-stage input/output schemas.
│   │                                     Stage N output must satisfy Stage N+1 input.
│   │                                     Funky validates this file for consistency.
│   │                                     A split here blocks merge.
│   │
│   └── INTEGRATION_CONTRACTS.md      ← 🍌 Contracts with external systems.
│                                         One entry per boundary named in BOUNDARIES.md.
│
├── /knowledge                         ← The bananas. What the Kong has collected.
│   │                                     Agents read. Humans maintain.
│   │                                     Never write here autonomously.
│   │
│   ├── /_shared                       ← Cross-product bananas.
│   │   ├── PATTERNS.md                   🍌 Recurring patterns. Indexed by type.
│   │   └── FAILURE_MODES.md              🍌 Known failure signatures.
│   │
│   ├── /{product-id}                  ← Product-specific banana collection.
│   │   ├── PRODUCT_CONTEXT.md            🍌 What it does. Key concepts. Version history.
│   │   ├── KNOWN_ISSUES.md               🍌 Confirmed issues. Version-tagged.
│   │   └── WORKAROUNDS.md                🍌 Indexed by issue id. Links to UC ids.
│   │
│   └── README.md                      ← Navigation rules.
│                                         Read product folder first.
│                                         Fall back to _shared.
│                                         Never write here — Kremlings get in that way.
│
├── /generation                        ← Artifacts the Kong produces.
│   │                                     Derived from /domain files.
│   │                                     Traceable to a use case id.
│   │                                     Funky flags any artifact with no UC trace.
│   │
│   ├── /code                          ← 🍌 per file that declares a UC id
│   │   └── README.md                     States which UC id each file satisfies.
│   │
│   ├── /tests                         ← 🍌 per file that maps to success criteria
│   │   └── README.md                     States UC id + criteria index per test.
│   │
│   └── /documentation                 ← 🍌 per file that covers a UC
│       └── README.md                     States which UCs are covered.
│
├── /stages                            ← Active work. Transient. Empties on resolution.
│   │
│   ├── /01-intake                     ← Raw input lands here.
│   ├── /02-analysis                   ← Mapped to domain model. UC identified.
│   ├── /03-execution                  ← Agent works against contract.
│   ├── /04-validation                 ← Funky validates output against STAGE_CONTRACTS.md.
│   └── /05-resolution                 ← Artifact staged. Awaits merge or dispatch.
│
└── /cranky                            ← Institutional memory. Grumpy. Always right.
    │                                     Don't rename this folder. Cranky is load-bearing.
    │
    ├── DECISIONS.md                   ← Dated judgment calls made without contract coverage.
    │                                     Graduates to /domain/DECISIONS.md
    │                                     when the pattern recurs 3 or more times.
    │                                     This is how the Kong feeds itself.
    │
    ├── FIRST_OCCURRENCES.md           ← New signal types, new UC patterns, novel inputs.
    │                                     Reviewed by humans on a defined cadence.
    │                                     Graduates to USE_CASES.md or KNOWN_ISSUES.md.
    │
    └── COVERAGE.md                    ← Running banana count per product and UC.
                                          Updated by Funky on each merge.
                                          Shows: bananas earned, peels open, splits blocking.
```

---

## The Barrel Cannon vs Barrel Distinction

```
The Barrel (AGENTS.md)

  Every agent reads the Barrel first.
  It tells them what the Kong is, what it contains, how to navigate it.
  It is the entry point. Passive. Orienting. Always present.


The Barrel Cannon (BARREL_CANNON.md)

  Not every Kong needs a Barrel Cannon.
  It is for workflows that are fully understood, high-confidence, and repeatable.
  The cannon skips analysis. It loads a specific context set and fires the agent
  directly to the target stage or agent.

  Example entry:

    workflow_id:       known-issue-response
    trigger_pattern:   SAP.signal_type == "question" AND confidence == "clear"
                       AND known_issue_matcher returns match_confidence > 0.9
    load_context:      /knowledge/{product_id}/KNOWN_ISSUES.md
                       /knowledge/{product_id}/WORKAROUNDS.md
                       /contracts/OUTPUT.md
    fire_to:           /stages/03-execution (answer-composer)
    confidence_floor:  0.9

  A cannon with no trigger_pattern match does nothing.
  Ambiguous signals fall through to standard stage navigation.
  The cannon is an optimization, not a replacement for the stage flow.
```

---

## The Banana Count

Funky produces this report on every merge:

```
Kong: product-alpha
  /domain
    USE_CASES.md              🍌  present, 12 use cases
    DOMAIN_MODEL.md           🍌  present, 8 entities
    BOUNDARIES.md             🍌  present
    DECISIONS.md              🍌  present, 6 decisions

  /contracts
    INPUT.md                  🍌  present
    OUTPUT.md                 🍌  present
    STAGE_CONTRACTS.md        🍌  present
    INTEGRATION_CONTRACTS.md  ⚠️  present — 2 boundaries unnamed (peel)

  /knowledge/product-alpha
    PRODUCT_CONTEXT.md        🍌  present
    KNOWN_ISSUES.md           🍌  present, 4 open issues
    WORKAROUNDS.md            ⚠️  present — issue #3 has no workaround (peel)

  /generation
    /code                     🍌  11 of 12 UCs covered
                              ⚠️  UC-007 has no code artifact (peel)
    /tests                    💀  UC-003 test references UC-004 success criteria (split — blocks merge)
    /documentation            🍌  12 of 12 UCs covered

  /cranky
    DECISIONS.md              🍌  present, 3 entries
    FIRST_OCCURRENCES.md      ⚠️  2 entries pending review (peel)
    COVERAGE.md               🍌  current

Banana count:    14 🍌
Open peels:       4 ⚠️
Blocking splits:  1 💀  → merge blocked until resolved
```

---

## Kong Health States

```
Well-fed Kong      High banana count. No splits. Few peels.
                   Barrel Cannon entries are valid and exercised.
                   Cranky has recent entries.
                   Agents navigate with high confidence.

Hungry Kong        Low banana count. Many peels. No splits.
                   Works for the happy path. Falls back gracefully.
                   Funky has a draft list of what to build next.

K. Rool Kong       Splits present. Known issues with no workarounds.
                   DECISIONS.md entries that contradict current code.
                   First occurrences that were never reviewed.
                   Agents navigate but produce unreliable outputs.
                   Funky is loud about this. Fix it or archive it.

Stub Kong          Barrel only. One product context file.
                   Performs at baseline. No worse than asking the model directly.
                   This is the starting state. Every Kong begins here.
```

---

## Fallback Guarantee

A Stub Kong — Barrel only — performs at baseline for any runner.
No worse than asking the model a plain question with no context.

Each banana earned improves performance above baseline.
Peels warn of gaps that will cause slips at runtime.
Splits block merge until resolved.
K. Rool is preventable. Feed the Kong.
