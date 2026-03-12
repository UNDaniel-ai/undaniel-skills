---
name: und-brainstorming
description: |
  TRIGGER when:
    - A Route C task needs requirements gap scanning, design challenge, or multi-option solution comparison before implementation
    - The user explicitly asks to brainstorm, compare options, challenge a design, or check whether requirements/design missed anything
    - A design-stage workflow needs 2-3 candidate approaches, a recommendation, or a completeness review

  DO NOT TRIGGER when:
    - The task is atomic and has one obvious implementation path with no meaningful tradeoff
    - The work is already in confirmed implementation planning or coding and only needs execution detail
    - The user has fixed both the approach and the constraints and does not want alternatives or challenge
metadata:
  emoji: "💡"
  category: "design-method"
  version: "1.1.0"
---

# und-brainstorming

Use this skill for structured pre-implementation thinking in Phase 2 style workflows.

## What This Owns

- scope decomposition check:
  - detect when the requested design actually contains multiple independent subsystems and should be split before deeper brainstorming
- requirements gap scan:
  - check whether `requirements-alignment.md` is missing goals, scope, constraints, acceptance, or unresolved questions
- option comparison:
  - generate and compare 2-3 viable approaches when tradeoffs are material
- design challenge:
  - stress-test a proposed design for completeness, rollback, compatibility, risk closure, and testability

## What This Does Not Own

- route selection or stage transitions: owned by `complex-task-solver`
- session lifecycle or document ownership: owned by `workspace-structure-manager`
- implementation planning detail: owned by `und-writing-plans`

## Required Output Modes

### 1. Requirements Gap Scan

Use when:
- the task is still in `requirements-alignment.md`
- the user asks "还有没有遗漏", "查漏补缺", or equivalent
- a Route C task has high ambiguity or incomplete acceptance criteria

Must produce:
- missing or weak requirement areas
- concrete follow-up questions
- explicit statement of what remains assumed vs confirmed

Hard rule:
- report missing items as questions or risks; do not silently rewrite user intent

### 2. Option Comparison

Use when:
- multiple viable implementation paths exist
- Route C requires solution evaluation
- the user asks for alternatives or tradeoffs

Must produce:
- 2-3 candidate approaches
- pros / cons / risk / cost for each
- AI recommendation and rationale

### 3. Design Challenge

Use when:
- `design.md` exists or is being drafted
- the task needs a completeness review before design confirmation

Must challenge:
- boundary coverage
- dropped alternatives
- rollback strategy
- compatibility impact
- validation / testability
- unresolved risks

Hard rule:
- challenge the current proposal directly; do not only expand the happy path

## Scope Check First

Before doing deep brainstorming, check whether the current request is actually too large for one coherent design pass.

Signals that scope should be decomposed first:
- multiple independent subsystems are bundled into one request
- the user is asking for a platform-sized workflow instead of one implementation slice
- the success criteria differ across parts strongly enough that one design would stay vague

If scope is too large:
- stop expanding details prematurely
- propose a decomposition into smaller design slices
- recommend which slice should go first

Hard rule:
- do not pretend one brainstorm pass has enough clarity when the task should first be decomposed

## Interaction Protocol

When clarification is needed:
- ask one question at a time
- prefer multiple-choice wording when it reduces ambiguity
- focus questions on purpose, constraints, success criteria, or missing boundaries

When presenting a medium or high-complexity design:
- validate in sections instead of forcing one giant approval
- use earlier feedback to revise later sections

## Execution Protocol

1. Read the current stage document first:
   - `requirements-alignment.md` for gap scan
   - `design.md` for option comparison or challenge
2. Run a scope decomposition check before deepening the design.
3. Choose the lightest mode that fits:
   - gap scan only
   - option comparison
   - challenge only
   - combined comparison + challenge
4. Ask at most one new clarifying question per turn when the current document still lacks a key decision.
5. Write findings back into the stage document structure instead of creating a competing owner document.
6. Preserve explicit stage confirmation boundaries and do not treat ordinary replies as design approval.

## Collaboration Boundaries

- `complex-task-solver` decides when Route C must invoke this skill.
- `workspace-structure-manager` owns where the result is recorded.
- `und-brainstorming` improves `requirements-alignment.md` and `design.md`; it does not replace them.

## Validation Expectations

- `automatic trigger`: Route C / multi-option / gap-scan scenarios
- `explicit request`: user directly asks for brainstorming, challenge, or completeness review
- `multi-turn`: resumed design work still routes through the correct brainstorming mode
- semantic assertions should allow equivalent wording such as `查漏`, `challenge`, `方案比较`, or `design review`

## Version History

- **v1.1.0** (2026-03-11):
  - added scope decomposition checks for oversized design requests
  - added one-question-at-a-time / multiple-choice interaction guidance
  - added section-by-section validation guidance for richer design discussions
