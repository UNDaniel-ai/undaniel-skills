---
name: und-systematic-debugging
description: |
  TRIGGER when:
    - Execution hits a bug, flaky test, regression, or unexpected behavior whose cause is not yet bounded
    - The user explicitly asks to debug, trace root cause, investigate a flaky issue, or avoid blind fixing
    - Stage 4 work needs evidence-driven diagnosis before further implementation

  DO NOT TRIGGER when:
    - The task is still in requirements, design, or planning with no concrete failure to investigate
    - The failure cause is already known and the remaining work is a straightforward implementation step
    - The immediate need is final completion verification rather than diagnosis
metadata:
  emoji: "🔎"
  category: "debugging-method"
  version: "1.0.0"
---

# und-systematic-debugging

Use this skill for evidence-first debugging when the failure is real but the cause is not yet understood.

## What This Owns

- root-cause-first debugging flow
- pattern analysis before patching
- hypothesis-driven experiments
- recording debugging evidence in `progress-details.md`

## What This Does Not Own

- route or stage ownership: `complex-task-solver`
- session lifecycle or document ownership: `workspace-structure-manager`
- normal greenfield implementation sequencing: `und-test-driven-development`
- completion evidence gating: `und-verification-before-completion`

## Root Cause Investigation

Start by tracing the symptom to the first known bad state.

- capture the observed failure, not only the guessed cause
- identify which component first violates expectation
- when multiple systems are involved, trace the handoff hop by hop

Hard rule:

- do not propose or apply a fix before the failing layer is narrowed enough to test a concrete hypothesis

## Pattern Analysis

Before changing code, answer:

- when does it happen
- when does it not happen
- what changed recently
- what boundaries or dependencies differ across good and bad cases

If repeated fix attempts are failing, treat that as a strong signal to widen the investigation scope instead of doubling down on the same guess.

## Hypothesis And Testing

- test one hypothesis at a time
- prefer short experiments that disprove a cause quickly
- use condition-based waiting instead of arbitrary sleep when timing is part of the issue

Hard rule:

- if a hypothesis cannot be falsified, it is not yet a useful debugging hypothesis

## Implementation

Only after the cause is bounded:

- apply the smallest fix that addresses the confirmed cause
- rerun the reproducer
- add defense-in-depth when justified, such as tests, guards, assertions, or better boundary validation

## High-Value Methods

- root-cause tracing:
  - follow the failure from symptom to the first broken assumption
- condition-based waiting:
  - wait for a state transition or observable condition, not an arbitrary timer, when reproducing timing-sensitive issues
- defense-in-depth:
  - close the confirmed bug, then add a proportionate layer that makes recurrence easier to catch

## Execution Protocol

1. Record the symptom and reproducer.
2. Run root-cause investigation.
3. Compare good vs bad patterns.
4. Form one hypothesis and test it.
5. Repeat until the failing layer is bounded.
6. Apply the fix.
7. Reproduce again and capture the new result.
8. Record root cause, verification action, and defense-in-depth follow-up in `progress-details.md`.

## Collaboration Boundaries

- `complex-task-solver` decides when debugging work should route through this skill.
- `workspace-structure-manager` provides the `progress-details.md` carrier for evidence and recovery notes.
- `und-systematic-debugging` improves execution discipline; it does not replace acceptance or closeout gates.

## Validation Expectations

- `automatic trigger`: bug, regression, flaky test, or unexpected behavior prompts
- `explicit request`: the user directly asks for systematic debugging or root-cause tracing
- `multi-turn`: resumed execution updates the skill order when implementation turns into debugging
- semantic assertions should accept equivalent wording such as `debug`, `root cause`, `flaky`, `condition-based waiting`, or `defense-in-depth`
