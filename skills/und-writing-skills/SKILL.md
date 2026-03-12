---
name: und-writing-skills
description: |
  TRIGGER when:
    - Creating a new shared skill or substantially rewriting an existing one
    - Repairing skill trigger accuracy, bootstrap wording, validator contracts, or governance rules
    - Defining skill authoring standards, metadata conventions, or behavior tests

  DO NOT TRIGGER when:
    - The task only uses existing skills without changing them
    - The change is pure product code with no skill or governance impact
metadata:
  emoji: "🛠"
  category: "skill-authoring"
  version: "1.2.0"
---

# und-writing-skills

Use this skill when authoring or repairing skills in `lulu-skills-common`.

## Authoring Standard

- description 只写触发条件，不写完整流程摘要。
- For this capability family, use the `und-` prefix.
- Keep the body focused on execution rules, boundaries, and validation.
- Do not duplicate route ownership from `complex-task-solver`.
- Do not duplicate session ownership from `workspace-structure-manager`.
- When a capability mainly defines execution method inside an existing workflow stage, prefer a dedicated method skill over expanding an orchestration skill.
- Keep orchestration skills focused on dispatch / gate / route ownership, and keep protocol detail inside the method skill.

## Integration Surface Checklist

When adding or heavily rewriting a shared workflow skill, explicitly evaluate whether each of these surfaces must change:

- `templates/workspace/AGENTS.md.template`
- `tools/init_workspace.py`
- `tests/test_init_workspace.py`
- `tools/quick_validate.py`
- `tests/fixtures/skill-triggering/`
- `tests/fixtures/multiturn/`
- outward-facing docs such as `README.md` or `SETUP.md`

Hard rule:

- do not treat `SKILL.md` as the whole integration if the skill must also be discoverable, bootstrapped, validated, or behavior-tested
- if the bootstrap surface changed, add or update a bootstrap regression instead of relying only on behavior fixtures

## Change Surface Scan

When updating an existing core workflow skill, scan the nearby surfaces that commonly drift:

- related `knowledge/*.md` files
- workspace bootstrap wording
- bootstrap regression coverage such as `tests/test_init_workspace.py`
- validator contracts
- existing fixtures and test expectations
- user-facing setup or workflow docs

Hard rule:

- if the main skill contract changes, do not assume the surrounding knowledge and bootstrap surfaces stayed correct

## Required Structure

For new or heavily rewritten skills, include:

- clear trigger conditions
- clear do-not-trigger conditions
- hard gates or non-negotiable checks
- collaboration boundaries with adjacent skills
- validation expectations

## Behavior Test Minimum

Every non-trivial skill change should consider:

- `automatic trigger` coverage
- `explicit request` coverage
- `multi-turn` coverage
- semantic assertions for protocol behavior, not just literal wording

When a test checks workflow fields such as `order`, `session strategy`, or stage confirmation wording:

- prefer semantic assertions over a single exact token
- allow equivalent wording in Chinese / English when the protocol meaning is preserved
- allow equivalent punctuation or hyphenation when the protocol meaning is preserved, such as `main-session` vs `main session`
- only use exact-token assertions when the exact token itself is the contract

Preferred tooling:

- `tools/run_codex_fixture.py`
- `tests/test_codex_skill_triggering.py`
- `tests/test_codex_multiturn.py`

## Validation Sequence

1. Run `tools/quick_validate.py --skill <skill-name>` or `tools/skillctl validate --skill <skill-name>`.
2. If bootstrap discoverability changed, run `pytest tests/test_init_workspace.py`.
3. If trigger wording changed, update the relevant fixture cases.
4. If trigger behavior changed, run the opt-in behavior tests.
5. Record the governance decision with `skills-manager`.

## Review Checklist

- Is this really a new skill rather than an update to an existing one?
- If this is a method skill, should orchestration stay in an existing parent skill instead of being duplicated here?
- Does the description only encode trigger conditions?
- Does the skill stay concise instead of restating generic LLM knowledge?
- Does the skill state what it does not own?
- Were the integration surfaces checked: bootstrap, validator, fixtures, and docs?
- If bootstrap changed, was `tests/test_init_workspace.py` updated to prevent silent drift?
- If a core workflow skill changed, were related `knowledge/*.md` and templates scanned for drift?
- Do the behavior tests verify protocol semantics instead of brittle single-token wording?
- Is there evidence for automatic trigger, explicit request, and multi-turn behavior, or a documented reason to defer it?

## Version History

- **v1.2.0** (2026-03-11):
  - added `tests/test_init_workspace.py` to the integration-surface checklist
  - clarified that bootstrap changes require bootstrap regression, not only behavior fixtures
  - clarified semantic assertions should allow equivalent punctuation or hyphenation such as `main-session`

- **v1.1.0** (2026-03-11):
  - added integration-surface checklist for shared workflow skills
  - added method-skill vs orchestration-skill boundary guidance
  - added change-surface scan guidance for knowledge/bootstrap/validator drift
