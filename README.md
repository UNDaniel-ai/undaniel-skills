# lulu-skills-common

Shared source-of-truth repository for common agent skills.

## Repository Layout

- `skills/<skill-name>/`: managed skill contents
- `tools/skillctl`: sync/status/restore command entrypoint

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

## Validation

Validate skill format and syntax:

```bash
# Validate a single skill
tools/skillctl validate --skill AIWay

# Validate all skills
tools/skillctl validate --all
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
