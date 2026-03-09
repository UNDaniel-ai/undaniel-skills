# Governance Logs

This directory stores local governance decision logs. These logs are **not committed to Git** and remain device-local.

## Log Organization

- **Naming**: `YYYY-MM-DD_task-XXX.md` or `YYYY-MM-DD_<custom-id>.md`
- **Template**: See `../references/governance-log-template.md`
- **Storage**: Logs are stored locally only (see `.gitignore`)

## Log Management

Use `tools/governance_log.py` to manage logs:

```bash
# Create a new log (interactive)
tools/governance_log.py create --task-id <id> --interactive

# List recent logs
tools/governance_log.py list --last 10

# Search logs by skill
tools/governance_log.py list --skill <name>

# Show specific log
tools/governance_log.py show <log-id>

# Clean up old logs
tools/governance_log.py cleanup
```

## Automatic Cleanup

Logs are automatically cleaned when creating new logs to prevent unlimited growth:

- **Default**: Keep 200 most recent logs (~1-2 years of history)
- **Size limit**: Maximum 50MB total (safety net for abnormal cases)
- **Configurable**: Set `SKILLCTL_MAX_LOGS` and `SKILLCTL_MAX_LOG_SIZE_MB` environment variables

Example:

```bash
# Keep only 100 logs
export SKILLCTL_MAX_LOGS=100

# Set max size to 30MB
export SKILLCTL_MAX_LOG_SIZE_MB=30
```

## Why Local-Only?

- Logs contain personal workflow information
- Different devices have different usage patterns
- Avoids Git history pollution
- Maintains repository cleanliness
