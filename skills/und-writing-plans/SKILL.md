---
name: und-writing-plans
description: |
  TRIGGER when:
    - A confirmed design needs to be converted into a step-by-step implementation plan before coding
    - The user explicitly asks for an implementation plan, execution plan, rollout steps, or detailed coding steps
    - Stage 3 planning needs stronger step contracts such as inputs, validation commands, expected results, or acceptance criteria

  DO NOT TRIGGER when:
    - The task is still in requirements alignment or design selection and the implementation path is not yet confirmed
    - The user only wants a high-level summary instead of an executable plan
    - Coding is already underway and the immediate need is debugging or verification instead of plan authoring
metadata:
  emoji: "🗺"
  category: "planning-method"
  version: "1.1.0"
---

# und-writing-plans

Use this skill to turn an approved design into an executable implementation plan.

## What This Owns

- step decomposition for `implementation-plan.md`
- step-level execution contracts
- planning quality for file scope, validation, and expected outputs

## What This Does Not Own

- route or stage ownership: `complex-task-solver`
- session ownership and document lifecycle: `workspace-structure-manager`
- brainstorming or design challenge: `und-brainstorming`

## Step Contract Requirements

Every non-trivial step should explicitly include:

- `前置输入`
- `文件范围`
- `验证命令`
- `预期结果`
- `Step Acceptance`

## File Structure First

Before decomposing tasks, map the expected file structure.

This pass should answer:
- which files will be created or modified
- what each file is responsible for
- whether any file is taking on multiple responsibilities
- whether the proposed structure follows the existing codebase patterns closely enough

Hard rule:
- if file ownership is still vague, the plan is not ready for task breakdown

## Meaning Of `预期结果`

`预期结果` is the step-level postcondition.

It must describe:
- what externally observable state changes after the step
- what new artifact, behavior, or contract now exists
- what a reviewer can verify without inferring intent

It must not be:
- a vague restatement of the goal
- "完成该步骤" style wording
- hidden inside `Step Acceptance`

## Hard Gates

- Do not start coding from this skill.
- Do not dump implementation code into the plan as a substitute for real decomposition.
- If a step lacks a validation path, it is not ready.
- If strict TDD does not fit a step, record the exception explicitly.

## Planning Protocol

1. Start from approved `design.md`.
2. Produce a file structure map before writing detailed steps.
3. Break work into minimal, testable increments.
4. For each step, identify:
   - dependencies
   - touched files
   - failing test or verification gap
   - minimal implementation
   - refactor work
   - expected result
   - step acceptance
5. Mark serial vs parallel boundaries explicitly when useful.

## Plan Chunking Guidance

If one plan is becoming hard to review as a whole:
- split it into logical chunks
- keep each chunk independently understandable
- preserve spec alignment and reviewability across chunks

Each chunk should still make it easy to answer:
- what files are in scope
- what result becomes observable after completion
- how the reviewer can verify the chunk is done

## Collaboration Boundaries

- `complex-task-solver` dispatches this skill at Stage 3.
- `und-writing-plans` defines how detailed the plan must be.
- `workspace-structure-manager` defines where the plan is recorded.

## Validation Expectations

- `automatic trigger`: implementation-planning stage after design confirmation
- `explicit request`: user asks for a detailed implementation plan
- `multi-turn`: resumed conversations preserve planning order and stage boundaries
- tests should verify semantic planning fields, especially `预期结果` as a postcondition contract

## Version History

- **v1.1.0** (2026-03-11):
  - added file-structure-first planning guidance
  - added explicit rule that vague file ownership blocks task breakdown
  - added chunking guidance for large implementation plans
