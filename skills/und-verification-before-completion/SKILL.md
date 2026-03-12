---
name: und-verification-before-completion
description: |
  TRIGGER when:
    - The agent is about to claim a task is done, fixed, passing, or ready for acceptance
    - The user explicitly asks for verification before completion, fresh evidence, or proof that the claimed result is real
    - Stage 5 acceptance or closeout needs current-stage validation instead of a stale earlier result

  DO NOT TRIGGER when:
    - The task is still in requirements, design, or active implementation with no completion claim in scope
    - The immediate need is debugging an unknown failure rather than proving completion
    - The task is intentionally limited to planning or design with no runnable verification path
metadata:
  emoji: "✅"
  category: "verification-method"
  version: "1.0.0"
---

# und-verification-before-completion

Use this skill to gate completion claims on current-stage verification evidence.

## What This Owns

- the `claim -> command -> output -> evidence` gate before completion claims
- fresh verification evidence requirements for acceptance and closeout
- explicit labeling of partial verification versus full verification
- preventing status claims from relying only on agent narration

## What This Does Not Own

- route or stage ownership: `complex-task-solver`
- session lifecycle or document ownership: `workspace-structure-manager`
- authoring the tests themselves: `und-test-driven-development`
- root-cause diagnosis: `und-systematic-debugging`

## Fresh Verification Evidence

Completion claims must be backed by verification executed in the current stage window.

- rerun the relevant checks now, not only earlier in the task
- capture the actual command, scope, and result
- read the full output and exit code before claiming success

Hard rule:

- a previous passing run is not fresh verification evidence for a current completion claim unless the reason for reuse is explicitly recorded

## Claim Mapping

For every claim, identify the matching verification path:

- claim: what is being asserted as done, fixed, or passing
- command: what was run to test that claim
- output: what the command reported
- evidence: where the result is recorded for review

Hard rule:

- do not use one broad command as proof for an unrelated narrower claim unless the mapping is explicit and justified

## Partial Verification

When verification is incomplete:

- say it is partial verification
- list what was not rerun
- record why full verification was skipped or unavailable

Hard rule:

- never present partial verification as full completion

## Agent Success Report Is Not Evidence

- a summary sentence from the agent is not verification
- acceptance should point to concrete commands and observed results
- if manual validation is still needed, say so explicitly

## Execution Protocol

1. Enumerate the claims that are about to be made.
2. Map each claim to a verification command or a documented reason it cannot be rerun.
3. Execute the commands.
4. Read output and exit code fully.
5. Record fresh verification evidence in `acceptance.md` and, when useful, `progress-details.md`.
6. Only then state whether the claim is fully verified, partially verified, or still unverified.

## Collaboration Boundaries

- `complex-task-solver` decides when Stage 5 or completion claims must route through this skill.
- `workspace-structure-manager` provides the `acceptance.md` carrier for evidence.
- `und-verification-before-completion` sets the evidence bar; it does not replace user confirmation gates.

## Validation Expectations

- `automatic trigger`: prompts about claiming completion, writing acceptance, or proving a fix
- `explicit request`: the user directly asks for verification before completion or fresh evidence
- `multi-turn`: resumed conversations preserve the requirement for fresh verification evidence before declaring success
- semantic assertions should accept equivalent wording such as `fresh verification evidence`, `claim -> command -> output -> evidence`, `partial verification`, or `agent success report`
