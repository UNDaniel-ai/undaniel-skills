---
name: und-workflow-entry
description: |
  TRIGGER when:
    - A new development task, implementation-oriented discussion, refactor, multi-step debugging, or cross-chat continuation starts
    - The user asks the agent to follow the workspace workflow, AGENTS.md, or shared process before acting
    - The task needs an explicit first-pass decision about which skills to use, skip, or order

  DO NOT TRIGGER when:
    - The request is a clearly atomic edit with no meaningful skill choice
    - The user only wants a direct factual answer, translation, or summarization with no workflow execution
metadata:
  emoji: "🧭"
  category: "workflow-entry"
  version: "1.0.0"
---

# und-workflow-entry

Use this skill as the first coordination layer for workflow-driven tasks.

## Entry Protocol

Before any substantial action, explicitly assess:

1. `und-workflow-entry`
2. `complex-task-solver`
3. `workspace-structure-manager`
4. Any explicitly named skills
5. Any obviously matching supporting skills for the task

When the task touches shared skills under `lulu-skills-common/skills/`, also assess `skills-manager`.

When the task creates or substantially updates a skill, also assess `und-writing-skills`.

## First Response Contract

The first response must explicitly include `use / skip / why / order`.

Minimum fields:

- `und-workflow-entry`: `use` or `skip`, with a concrete reason
- `complex-task-solver`: `use` or `skip`, with a concrete reason
- `workspace-structure-manager`: `use` or `skip`, with a concrete reason
- additional skills: `use` or `skip`, with a concrete reason
- execution order
- session strategy: `new` / `reuse` / `skip`

Preferred short format:

- `und-workflow-entry: use/skip - why`
- `complex-task-solver: use/skip - why`
- `workspace-structure-manager: use/skip - why`
- `additional skills: name -> use/skip - why`
- `order: ...; session strategy: ...`

## Hard Gates

- If `complex-task-solver` selects Route B or Route C, `workspace-structure-manager` becomes mandatory unless the user explicitly rejects session documents.
- If a clearly relevant skill is skipped, say why.
- If the user explicitly names a skill, assess it before acting.
- Requirement clarification is not stage confirmation.
- In a new chat, `继续` or `好的` does not remove the need for entry assessment.
- Mentioning a path or file name does not make a task atomic by itself.
- Before the assessment is complete, do not start design, implementation planning, coding, validation, or completion claims.

## Collaboration Boundaries

- `und-workflow-entry` does not replace `complex-task-solver` route selection.
- `und-workflow-entry` does not replace `workspace-structure-manager` session ownership.
- `und-workflow-entry` does not replace `skills-manager` governance decisions.
- `und-workflow-entry` only decides the initial skill coordination and response shape.

## Common Use Cases

### 1. New implementation task

Use `und-workflow-entry` first, then decide whether `complex-task-solver` and `workspace-structure-manager` are needed.

### 2. Shared skill maintenance

If the task modifies `lulu-skills-common`, include `skills-manager`. If skill authoring is involved, include `und-writing-skills`.

### 3. Cross-chat continuation

Even when the user says "继续", re-evaluate whether this is a new chat that still requires the initial use/skip/order/session declaration.
