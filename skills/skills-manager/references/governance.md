# Skills Governance Protocol

## Goal

Make post-task skill capture deterministic and auditable.

## Two-Step Confirmation

Use this exact structure:

1. Step 1 (capture intent):
   - ask whether this task has reusable experience worth capturing.
2. Step 2 (target decision):
   - ask whether to update an existing skill or create a new skill;
   - include the concrete target skill name or the proposed new skill name.

Do not mutate files before both confirmations complete.

## Boundary-First Routing

Choose the route with this order:

1. Check if the experience is already inside one existing skill scope (`description` + SKILL.md responsibilities).
2. If yes, update that skill.
3. If no, create a new skill.

Use this quick decision table:

| Condition | Route |
| --- | --- |
| Experience extends steps/checks/examples of one existing capability | Update existing skill |
| Experience introduces a new independent workflow | Create new skill |
| Experience spans multiple skills and cannot fit one boundary cleanly | Create new skill |

## Accuracy Calibration Trigger

For each skill used in the task, flag calibration if any of these occur:

- instruction is outdated relative to actual command/path/API;
- instruction is incomplete and caused avoidable retries;
- instruction is inaccurate and leads to wrong operation.

After user confirmation, patch the skill and validate.

## Validation Minimum

After each confirmed governance change:

1. Run `quick_validate.py` for each affected skill folder:
   ```bash
   tools/skillctl validate --skill <skill-name>
   ```

   The validation tool checks:
   - YAML frontmatter format and required fields (name, description)
   - Markdown structure (code blocks closed, heading levels)
   - Code block content (bash syntax, JSON format)
   - Link integrity (internal and external)

2. If command examples changed, run representative command dry-run checks.

3. Record governance decision:
   ```bash
   tools/governance_log.py create --task-id <id> --interactive
   ```

4. Report what changed and why.

## Governance Log System

All governance decisions should be recorded in local logs:

- **Create logs**: Use `governance_log.py create --interactive` for guided prompts
- **List logs**: Use `governance_log.py list --last 10` to view recent decisions
- **Search logs**: Use `governance_log.py search --skill <name>` to find specific skill logs
- **Automatic cleanup**: Logs are automatically cleaned (keeping 200 most recent) to prevent disk bloat

Logs are stored locally in `skills/skills-manager/logs/` and are not committed to Git.
