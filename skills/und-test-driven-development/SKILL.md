---
name: und-test-driven-development
description: |
  TRIGGER when:
    - A confirmed implementation step is about to start and the work should follow a failing-test-first loop
    - The user explicitly asks for TDD, failing test first, Verify RED / Verify GREEN, or a red/green/refactor workflow
    - Stage 4 execution needs an explicit decision about strict TDD versus a documented `TDD 例外`

  DO NOT TRIGGER when:
    - The task is still in requirements alignment, design, or implementation planning
    - The immediate need is debugging an unknown failure rather than executing a confirmed implementation slice
    - The step is pure documentation, governance, or template work with an explicit non-TDD verification path
metadata:
  emoji: "🧪"
  category: "execution-method"
  version: "1.0.0"
---

# und-test-driven-development

Use this skill to execute confirmed implementation work with a disciplined red/green/refactor loop.

## What This Owns

- failing-test-first execution for Stage 4 work
- `Verify RED -> Minimal Implementation -> Verify GREEN -> Refactor` ordering
- explicit `TDD 例外` decisions and recording requirements
- anti-pattern checks around mocks, test-only methods, and false-green workflows

## What This Does Not Own

- route selection or stage transitions: `complex-task-solver`
- session lifecycle or document ownership: `workspace-structure-manager`
- root-cause investigation for bugs or flaky behavior: `und-systematic-debugging`
- completion claims or acceptance evidence: `und-verification-before-completion`

## Verify RED

Before writing production code:

- define the smallest observable behavior change
- run the target test to prove it fails for the expected reason
- narrow the failure to the intended slice instead of relying on a noisy broad failure

Hard rule:

- do not describe the step as TDD if no red proof was observed and no `TDD 例外` was recorded

## Minimal Implementation

- implement only what is required to turn the target test green
- avoid speculative refactors during the first green pass
- if mocks are needed, use them only at real boundaries with stable contracts

## Verify GREEN

After the minimal change:

- rerun the target test and confirm it now passes
- rerun the smallest necessary regression scope
- record the command, scope, or observed result in `progress-details.md`

Hard rule:

- a broad green suite does not replace proving that the original failing test turned green

## Refactor After Green

- refactor only after the target behavior is green
- keep tests running during refactor
- if refactor reveals missing coverage, add the next failing test before making the next production change

## Anti-Pattern Checks

- mock abuse:
  - do not use a mock to hide an unverified integration contract
- test-only methods:
  - do not add production APIs, flags, or branches that only exist for the test harness
- incomplete mocks:
  - do not model only the happy-path subset when the real dependency contract is richer
- false TDD:
  - do not write production code first and retrofit a confirming test later
- assertion drift:
  - prefer observable behavior over private implementation details

## TDD Exceptions

Typical `TDD 例外` cases:

- pure documentation or template changes
- mechanical renames with no behavior change
- tooling or bootstrap work where verification is contract-based rather than executable behavior-based

When using an exception, record:

- why strict TDD does not fit
- what verification replaces it
- whether the exception is step-scoped or task-scoped

Hard rule:

- never leave a non-TDD step unclassified; either follow TDD or write the exception explicitly

## Execution Protocol

1. Pick the smallest behavior slice from the confirmed plan.
2. Write or update the failing test.
3. Verify RED.
4. Apply the minimal implementation.
5. Verify GREEN.
6. Refactor only after green.
7. Record evidence or `TDD 例外` in `progress-details.md` and, when needed, `implementation-plan.md`.

## Collaboration Boundaries

- `complex-task-solver` decides when Stage 4 should route through this skill.
- `workspace-structure-manager` defines where TDD evidence is recorded.
- `und-test-driven-development` owns the method, not the overall workflow gate.

## Validation Expectations

- `automatic trigger`: confirmed Stage 4 implementation work that should start with a failing test
- `explicit request`: the user directly asks for TDD, failing test first, or `Verify RED / Verify GREEN`
- `multi-turn`: resumed execution still preserves red/green ordering and `TDD 例外` handling
- semantic assertions should allow equivalent wording such as `failing test first`, `red/green`, `Verify RED`, `Verify GREEN`, or `TDD 例外`
