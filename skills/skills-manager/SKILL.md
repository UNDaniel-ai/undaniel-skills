---
name: skills-manager
description: Manage and govern shared skills in the lulu-skills-common repository. Use when asked to sync or repair skills, and also when a task finishes and the agent should decide whether reusable experience must be captured, confirm with the user, route to update-existing-skill vs create-new-skill by capability boundary, and fix skill accuracy gaps for skills used in the task.
---

# Skills Manager

## Overview

Use this skill to run two responsibilities:

1. Keep managed skills aligned across agents with `tools/skillctl`.
2. Govern skill knowledge quality through post-task capture and self-calibration.

When the task creates or rewrites skills, also use `und-writing-skills`.

## Governance Runbook (Task End)

Run this sequence at the end of each completed task.

1. Capture candidate experience.
2. Ask first confirmation: "是否需要沉淀这次经验？"
3. If user confirms, route by capability boundary:
   - falls inside one existing skill responsibility -> update that skill;
   - introduces a new independent workflow/capability -> create a new skill.
4. Ask second confirmation with explicit target:
   - update `<skill-name>` or create `<new-skill-name>`.
5. After second confirmation, implement changes and validate.
   - if the task added or heavily rewrote a workflow skill, also verify integration surfaces instead of only `SKILL.md`
6. Record the governance result with the template in `references/governance-log-template.md`.

If no candidate is found, record `decision=none` and do not mutate files.

## Skill 识别失败修复流程

当用户、测试或回归观察到“该用的 skill 没有被稳定命中”时，先分类，再修复：

1. 判断是 `机制问题`、`执行漏触发`，还是 skill 内容本身不准。
2. 优先修 `机制问题`，再修单个 skill。
3. 修复后必须补验证，而不是只改文案。

### `机制问题`

典型信号：

- workspace `AGENTS.md` 没有列出需要的 skill
- workspace bootstrap 生成的 `AGENTS.md` 仍停留在旧 skill 集合，导致新 skill 在真实环境中根本不可见
- bootstrap 模板、初始化脚本、提示模板没有把入口协议写进去
- 缺少 bootstrap 回归，导致 `AGENTS.md.template` 与 `init_workspace.py` 的漂移不会被测试发现
- 行为测试 harness 缺失，导致无法证明触发是否真的发生

处理方式：

- 优先检查 `templates/workspace/AGENTS.md.template`
- 优先检查 `tools/init_workspace.py`
- 优先检查 `tests/test_init_workspace.py`
- 优先检查 `tools/run_codex_fixture.py` 与相关 fixtures
- 若 `skillctl validate` 已通过但 behavior fixture 仍漏触发，先查看 bootstrapped workspace 的 `AGENTS.md`，不要直接改 trigger wording
- 修复后补 bootstrap 或行为测试

### `执行漏触发`

典型信号：

- 规则已经写在 skill 或 `AGENTS.md` 里，但真实执行时没有先说 use/skip/order
- 用户显式点名 skill，执行中仍被忽略
- 多轮对话里第一轮遵守了入口纪律，后续 turn 又丢失

处理方式：

- 先确认是否该由 `und-workflow-entry` 协调
- 再检查目标 skill 的 trigger wording 是否足够清晰
- 对修复后的行为补 `automatic trigger`、`explicit request`、`multi-turn` 覆盖

### `skill 内容不准`

典型信号：

- skill 指令和真实执行顺序冲突
- 同一职责同时散落在多个 skill 里
- description 像流程摘要，而不是触发条件

处理方式：

- 结合 `und-writing-skills` 收紧 description、边界和验证要求
- 对受影响 skill 立即更新并重新校验

## Candidate Signals

Treat experience as "worth capturing" when at least one signal is true:

- the same non-trivial procedure was repeated in this task;
- a stable failure mode and fix path was discovered;
- an important missing step/checklist was identified;
- current skill instructions were inaccurate, stale, or ambiguous during execution.

High-value governance candidates often look like:

- a method skill was added but surrounding bootstrap / validator / fixtures / docs also needed coordinated changes
- a main skill contract changed and related `knowledge/*.md` or templates drifted behind it

## Accuracy Self-Calibration (Used Skills Only)

Only check skills actually used or cited during the task.

1. Detect mismatch between skill instructions and real execution behavior.
2. Prompt the user with concrete gap + impact.
3. After user confirmation, update the affected skill immediately.
4. Validate the updated skill before finishing.

## Governance Acceptance

After updating or adding skills, the governance acceptance bar is:

1. `tools/skillctl validate --skill <skill-name>`
2. Metadata and boundary wording match `und-writing-skills`
3. If trigger behavior changed, update or add behavior fixtures
4. If trigger behavior changed, run the opt-in behavior tests before declaring the fix stable
5. If the task is in Acceptance or Session Closeout, use fresh verification evidence from the current stage instead of relying only on earlier-stage results
6. If bootstrap discoverability changed, include `pytest tests/test_init_workspace.py` in the validation evidence

### Mechanism Completeness Check

When the governance change adds or heavily rewrites a shared workflow or method skill, explicitly check whether these surfaces also required updates:

- `templates/workspace/AGENTS.md.template`
- `tools/init_workspace.py`
- `tests/test_init_workspace.py`
- `tools/quick_validate.py`
- fixture coverage under `tests/fixtures/skill-triggering/` and `tests/fixtures/multiturn/`
- user-facing workflow docs such as `README.md` or `SETUP.md`

Hard rule:

- do not close governance by validating only `SKILL.md` when the real failure mode was a missing integration surface

### Knowledge Drift Check

When a core workflow skill or stage model changed, scan adjacent artifacts for drift:

- related `knowledge/*.md` files
- templates carrying the affected workflow stage
- bootstrap wording that references the changed skill or phase model

Use this check when the mismatch is not a new workflow, but stale surrounding instructions.

### Fresh Verification Evidence

- Acceptance / closeout conclusions must be backed by verification executed in the current stage window
- Do not rely only on yesterday's or a previous stage's test result when current-stage acceptance is being written
- If rerunning is intentionally skipped, record the concrete reason instead of silently reusing stale evidence

## Sync Operations

- Treat symlink as the steady state; do not remove symlinks after verification.
- When target path is a real directory/file, move it into `.skillctl-backups/<skill>/<timestamp>` first, then create symlink.
- Only skills that exist in this repository under `skills/` are managed by `skillctl`.
- Run `sync` and `status` in sequence (not in parallel). Parallel execution can read stale state and produce false `missing` results.
- Escalate only when command errors indicate missing remote, auth failure, or path permission issues.

## Command Patterns

- Sync one skill to both agents:
  - `tools/skillctl sync --skill <skill-name> --agent all`
- Sync all managed skills:
  - `tools/skillctl sync --all --agent all`
- Preview filesystem changes:
  - append `--dry-run` to `sync` or `restore`
- Check current link status:
  - `tools/skillctl status --agent all`
- Recommended verification sequence:
  - `tools/skillctl sync --all --agent all`
  - `tools/skillctl status --agent all`
- Restore one skill from latest backup:
  - `tools/skillctl restore --skill <skill-name> --agent codex --latest`
  - `tools/skillctl restore --skill <skill-name> --agent claude --latest`

## Validating Skill Changes

After completing skill modifications, run the validation tool:

```bash
# Validate single skill
tools/skillctl validate --skill <skill-name>

# Validate all skills
tools/skillctl validate --all
```

Validation checks:
- YAML frontmatter format and required fields
- Markdown code block integrity
- Command example basic syntax
- Link validity
- selected governance contracts

## Behavior Test Expectations

When the change affects triggering, workflow entry, or skill routing, treat behavior tests as part of the acceptance criteria.

Minimum coverage targets:

- `automatic trigger`
- `explicit request`
- `multi-turn`
- assertions should prefer protocol meaning over brittle single-token wording when possible
- accept equivalent wording such as Chinese / English variants or punctuation changes when the protocol meaning is unchanged

Recommended commands:

```bash
CODEX_BEHAVIOR_TESTS=1 pytest tests/test_codex_skill_triggering.py
CODEX_BEHAVIOR_TESTS=1 pytest tests/test_codex_multiturn.py
```

## Recording Governance Decisions

Use the governance log tool to record decisions:

```bash
# Create new log (interactive)
tools/governance_log.py create --task-id <id> --interactive

# View recent logs
tools/governance_log.py list --last 10

# Search for specific skill logs
tools/governance_log.py list --skill <skill-name>
```

## References

- For CLI syntax and expected states, read `references/commands.md`.
- For decision and confirmation protocol, read `references/governance.md`.
- For structured outcome recording, read `references/governance-log-template.md`.
