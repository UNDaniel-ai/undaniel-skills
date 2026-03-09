---
name: skills-manager
description: Manage and govern shared skills in the lulu-skills-common repository. Use when asked to sync or repair skills, and also when a task finishes and the agent should decide whether reusable experience must be captured, confirm with the user, route to update-existing-skill vs create-new-skill by capability boundary, and fix skill accuracy gaps for skills used in the task.
---

# Skills Manager

## Overview

Use this skill to run two responsibilities:

1. Keep managed skills aligned across agents with `tools/skillctl`.
2. Govern skill knowledge quality through post-task capture and self-calibration.

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
6. Record the governance result with the template in `references/governance-log-template.md`.

If no candidate is found, record `decision=none` and do not mutate files.

## Candidate Signals

Treat experience as "worth capturing" when at least one signal is true:

- the same non-trivial procedure was repeated in this task;
- a stable failure mode and fix path was discovered;
- an important missing step/checklist was identified;
- current skill instructions were inaccurate, stale, or ambiguous during execution.

## Accuracy Self-Calibration (Used Skills Only)

Only check skills actually used or cited during the task.

1. Detect mismatch between skill instructions and real execution behavior.
2. Prompt the user with concrete gap + impact.
3. After user confirmation, update the affected skill immediately.
4. Validate the updated skill before finishing.

## Sync Operations

- Treat symlink as the steady state; do not remove symlinks after verification.
- When target path is a real directory/file, move it into `.skillctl-backups/<skill>/<timestamp>` first, then create symlink.
- Only skills that exist in this repository under `skills/` are managed by `skillctl`.
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
