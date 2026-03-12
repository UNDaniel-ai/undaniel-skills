# Skills Manager Commands

## Managed Agents

- `codex` -> `~/.codex/skills`
- `claude` -> `~/.claude/skills`

## CLI

```bash
tools/skillctl sync --skill <name> --agent <codex|claude|all> [--dry-run]
tools/skillctl sync --all --agent <codex|claude|all> [--dry-run]
tools/skillctl status [--agent <codex|claude|all>] [--skill <name>]
tools/skillctl restore --skill <name> --agent <codex|claude> --latest [--dry-run]
```

## Sync Behavior

1. Run `git fetch origin main`.
2. Run `git pull --ff-only origin main`.
3. For `sync --all`, enumerate only non-hidden directories under `skills/`.
4. Validate each target skill exists in `skills/<name>/SKILL.md`.
5. For each target agent:
   - If skill target is already the correct symlink, keep as-is.
   - If target is a real directory/file, move it to `.skillctl-backups/<skill>/<timestamp>`.
   - Create or repair symlink to repository skill path.

`sync --all` excludes hidden directories (for example, `.test-skill`).

## Status States

- `linked-ok`: symlink exists and points to repository skill path.
- `linked-mismatch`: symlink exists but points to another location.
- `conflict-dir` / `conflict-file`: target exists but is not a symlink.
- `missing`: target path is absent.
- `missing-source`: requested skill does not exist under repo `skills/`.

## Restore Behavior

- `restore --latest` moves the latest backup entry back to target path.
- If target currently exists:
  - symlink: remove it first;
  - real directory/file: move it to `pre-restore-<timestamp>` under the same backup root.

## Governance Usage

- Run post-task governance after delivery:
  - detect reusable experience;
  - perform two-step user confirmation;
  - route to update-existing-skill or create-new-skill by capability boundary.
- Check accuracy only for skills used in the task.
- For governance protocol details, read `governance.md`.

## Recommended Verification Sequence

Run these commands in order and avoid parallel execution:

1. `tools/skillctl sync --all --agent all`
2. `tools/skillctl status --agent all`

Running `sync` and `status` concurrently can cause status checks to read stale state.
