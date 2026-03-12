# lulu-skills-common

Shared source-of-truth repository for common agent skills.

## Team Guide

For team onboarding and day-to-day setup, start from:

- [SETUP.md](SETUP.md)

## Repository Layout

- `skills/<skill-name>/`: managed skill contents
- `tools/skillctl`: sync/status/restore command entrypoint
- `tools/init_workspace.py`: bootstrap a workspace-local `AGENTS.md`
- `tools/run_codex_fixture.py`: opt-in Codex behavior fixture runner
- `templates/workspace/AGENTS.md.template`: shared workspace bootstrap template

## Quick Start

```bash
# Sync one skill to Codex + Claude
tools/skillctl sync --skill AIWay --agent all

# Sync all skills
tools/skillctl sync --all --agent all

# Check link status
tools/skillctl status --agent all

# Restore latest backup
tools/skillctl restore --skill AIWay --agent codex --latest
```

## Workspace Bootstrap

Bootstrap the current workspace so the agent follows the shared `lulu-skills-common` process:

```bash
# From this repository root, initialize the current directory
python3 tools/init_workspace.py

# Initialize a specific workspace path
python3 tools/init_workspace.py /path/to/workspace

# Overwrite an existing AGENTS.md only when you explicitly want to replace it
python3 tools/init_workspace.py /path/to/workspace --force
```

The generated `AGENTS.md` includes:

- `und-workflow-entry` for first-response skill coordination
- `und-brainstorming` and `und-writing-plans` for Route C design/planning methods
- `und-test-driven-development`, `und-systematic-debugging`, and `und-verification-before-completion` for execution and acceptance discipline
- shared workflow skill references for `complex-task-solver`, `workspace-structure-manager`, and `skills-manager`
- `und-writing-skills` for shared skill authoring governance
- mandatory first-response assessment for `und-workflow-entry`, `complex-task-solver`, and `workspace-structure-manager`
- a reminder that requirement clarification is not stage confirmation
- a reserved section for repo-specific extensions

If you want a short instruction file to hand to an agent, use:

- `templates/workspace/INIT_AGENT_PROMPT.md`

## Validation

Validate skill format and syntax:

```bash
# Validate a single skill
tools/skillctl validate --skill AIWay

# Validate all skills
tools/skillctl validate --all
```

Run opt-in behavior tests when trigger or workflow entry behavior changes:

```bash
CODEX_BEHAVIOR_TESTS=1 pytest tests/test_codex_skill_triggering.py
CODEX_BEHAVIOR_TESTS=1 pytest tests/test_codex_multiturn.py
```

## Governance Logging

Track governance decisions:

```bash
# Create a new governance log
tools/governance_log.py create --task-id <id> --interactive

# List recent logs
tools/governance_log.py list --last 10

# Search logs
tools/governance_log.py search --skill AIWay
```

## Git Pre-commit Hook (Optional)

Install automated validation before commits:

```bash
# Install the hook
bash tools/install-hooks.sh

# The hook will automatically validate modified SKILL.md files
# before each commit

# Bypass if needed (not recommended)
git commit --no-verify
```

**What the hook does:**
- Only validates SKILL.md files you're committing (fast!)
- Blocks commits with validation errors
- Shows clear error messages
- Performance: < 2 seconds per skill

**Note:** If you have a global `core.hooksPath` configured, you'll need to either:
- Unset it: `git config --global --unset core.hooksPath`
- Copy the hook to your global hooks directory

## Testing

Run tests with validation tool:

```bash
# Test against a skill with intentional errors
tools/quick_validate.py skills/.test-skill

# Should report 5 errors and 15 warnings
```

The `.test-skill` contains comprehensive error examples for testing the validation tool.

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Install Git pre-commit hook:
   ```bash
   bash tools/install-hooks.sh
   ```

3. Sync skills to agents:
   ```bash
   tools/skillctl sync --all --agent all
   ```

4. Bootstrap the target workspace when you want it to follow the shared flow:
   ```bash
   python3 tools/init_workspace.py /path/to/workspace
   ```

## Sync Behavior

`sync` behavior:

1. `git fetch origin main`
2. `git pull --ff-only origin main`
3. Replace target skill paths with symlinks to this repository.
4. If conflict exists (real directory/file), move it to `.skillctl-backups/<skill>/<timestamp>`.

Managed scope:

- `skillctl` only manages skills that exist under this repository's `skills/` directory.

Skills governance:

- Use `skills/skills-manager` to run post-task capture and calibration:
  - decide whether experience should be captured;
  - confirm update-existing vs create-new by capability boundary;
  - fix confirmed skill accuracy gaps for skills used in the task.
- When a task creates or rewrites skills, also use `skills/und-writing-skills`.
- Route B / Route C execution additionally relies on:
  - `skills/und-test-driven-development`
  - `skills/und-systematic-debugging`
  - `skills/und-verification-before-completion`
