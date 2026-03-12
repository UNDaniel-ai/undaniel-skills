---
name: und-subagent-driven-development
description: |
  TRIGGER when:
    - A confirmed Route C implementation slice is ready for execution and needs a decision about real subagent dispatch versus explicit main-session fallback
    - The user explicitly asks for subagent-driven development, child-agent execution, collab-assisted implementation, or spec-first review loops during coding
    - Stage 4 execution has clear task boundaries and should check whether subagent orchestration is genuinely available before proceeding

  DO NOT TRIGGER when:
    - The task is still in requirements alignment, design, or implementation planning
    - The immediate need is debugging an unknown failure rather than executing a bounded implementation slice
    - The work is pure documentation, governance, or template authoring where a subagent orchestration loop would be artificial
metadata:
  emoji: "🤝"
  category: "execution-orchestration"
  version: "1.0.0"
---

# und-subagent-driven-development

Use this skill to decide whether Stage 4 execution should use real subagent orchestration or an explicit main-session fallback.

## What This Owns

- capability detection for real subagent / collab execution
- task eligibility checks for subagent candidates
- implementer status handling and review sequencing
- explicit fallback when tooling or task shape does not support subagents

## What This Does Not Own

- route or stage ownership: `complex-task-solver`
- session lifecycle or document ownership: `workspace-structure-manager`
- red/green execution method for the implementation itself: `und-test-driven-development`
- root-cause investigation for unknown failures: `und-systematic-debugging`
- completion claims or acceptance evidence: `und-verification-before-completion`

## Capability Detection

Before claiming subagent-driven execution, evaluate all three checks:

- `tooling_supported`
  - real child-agent, task-dispatch, or equivalent collab tooling is available in the current environment
- `workspace_supported`
  - the worker can safely operate on the current workspace and return inspectable results
- `review_supported`
  - the controller can review code or diffs with enough fidelity to run spec compliance review and, when available, code quality review

Hard rule:

- if any capability check fails, record the failure and use fallback
- do not imply that subagents were used when execution stayed in the main session

## Task Eligibility

Only treat a step as a subagent candidate when all of the following are true:

- the implementation plan is already confirmed
- the step has explicit `前置输入`, `文件范围`, and `预期结果`
- the current slice is bounded implementation work, not open-ended debugging
- there is no unresolved design ambiguity for the step
- the review contract is clear enough to evaluate what the implementer returns

Hard rule:

- if the step boundary is vague, stay in the main session and tighten the plan first

## Status Model

Implementers or fallback controllers must classify execution as one of:

- `DONE`
- `DONE_WITH_CONCERNS`
- `NEEDS_CONTEXT`
- `BLOCKED`

Handling rules:

- `DONE`: continue to spec compliance review
- `DONE_WITH_CONCERNS`: read concerns before review; resolve correctness or scope risks first
- `NEEDS_CONTEXT`: provide missing context and re-dispatch only after the gap is addressed
- `BLOCKED`: change something real before retrying, such as context, task size, or execution mode

Hard rule:

- do not silently retry the same blocked dispatch without new context or a smaller slice

## Spec Compliance Review

Spec compliance review is the minimum required gate whenever subagent orchestration is attempted.

- review actual changed files, diffs, and verification evidence instead of trusting the implementer report
- check for missing requirements, extra scope, and requirement misinterpretation
- keep spec compliance review ahead of any code quality review

Hard rule:

- if spec compliance is not clearly green, the task is not done

## Code Quality Review

Code quality review is capability-aware rather than mandatory in every environment.

- when review tooling is strong enough, run a second pass focused on maintainability, testing quality, file responsibility, and integration safety
- when review tooling is not strong enough, downgrade to a documented fallback checklist in the main session
- never let code quality review replace spec compliance review

## Fallback Protocol

Fallback means: execution continues in the main session under honest Stage 4 discipline.

Record all of the following in `progress-details.md`:

- which capability check failed, or why the step was not eligible
- whether the fallback is step-scoped or task-scoped
- which method replaces subagent execution, usually `und-test-driven-development`
- whether any review work is reduced to a controller checklist

Fallback execution rules:

- continue the confirmed implementation step in the main session
- keep TDD discipline unless a documented `TDD 例外` applies
- if execution turns into unknown-failure diagnosis, switch to `und-systematic-debugging`
- before any completion claim, still use `und-verification-before-completion`

## Execution Protocol

1. Read the confirmed implementation step and its execution-mode fields.
2. Run capability detection.
3. Decide whether the step is a real subagent candidate.
4. If supported, dispatch one bounded implementer task with full task text and context.
5. Handle the returned status using the status model.
6. Run spec compliance review first.
7. Run code quality review only when capability support is sufficient; otherwise record fallback review.
8. Update `progress-details.md` with dispatch, review, and fallback facts.

## Collaboration Boundaries

- `complex-task-solver` decides when Stage 4 should route through this skill.
- `workspace-structure-manager` provides the plan and progress documents that hold execution-mode and fallback facts.
- `und-subagent-driven-development` orchestrates execution mode selection; it does not replace the underlying implementation, debugging, or acceptance methods.

## Validation Expectations

- `automatic trigger`: confirmed Route C coding work with clear task boundaries and possible subagent execution
- `explicit request`: user asks for subagent-driven development, child-agent help, or spec-first review loops
- `multi-turn`: resumed execution preserves the distinction between real subagent dispatch and honest main-session fallback
- semantic assertions should accept equivalent wording such as `subagent`, `child agent`, `collab`, `spec compliance review`, `code quality review`, or `fallback`
