#!/usr/bin/env python3
"""
Governance log management tool.

Manages governance decision logs with create, list, show, search, and cleanup functionality.
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

try:
    import click
except ImportError:
    print("Error: Missing required dependency: click")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)


# Configuration constants
DEFAULT_MAX_LOGS = 200  # Keep ~1-2 years of history
DEFAULT_MAX_SIZE_MB = 50  # Safety net for abnormal cases
CLEANUP_WARNING_THRESHOLD = 150  # Warn when approaching limit


class LogsConfig:
    """Configuration for governance logs."""

    def __init__(
        self,
        logs_dir: Optional[Path] = None,
        max_logs: Optional[int] = None,
        max_size_mb: Optional[int] = None
    ):
        """
        Initialize logs configuration.

        Args:
            logs_dir: Directory for log files (default: auto-detect from script location)
            max_logs: Maximum number of logs to keep (default: from env or 200)
            max_size_mb: Maximum total size in MB (default: from env or 50)
        """
        if logs_dir is None:
            # Default: detect from script location
            script_dir = Path(__file__).parent
            repo_root = script_dir.parent
            logs_dir = repo_root / "skills" / "skills-manager" / "logs"

        self.logs_dir = Path(logs_dir)
        self.max_logs = max_logs if max_logs is not None else int(
            os.environ.get("SKILLCTL_MAX_LOGS", DEFAULT_MAX_LOGS)
        )
        self.max_size_mb = max_size_mb if max_size_mb is not None else int(
            os.environ.get("SKILLCTL_MAX_LOG_SIZE_MB", DEFAULT_MAX_SIZE_MB)
        )
        self.warning_threshold = CLEANUP_WARNING_THRESHOLD


# Backward compatibility functions (deprecated, use LogsConfig instead)
def get_max_logs() -> int:
    """Get maximum number of logs from environment or default."""
    return int(os.environ.get("SKILLCTL_MAX_LOGS", DEFAULT_MAX_LOGS))


def get_max_size_mb() -> int:
    """Get maximum log size in MB from environment or default."""
    return int(os.environ.get("SKILLCTL_MAX_LOG_SIZE_MB", DEFAULT_MAX_SIZE_MB))


def get_logs_dir() -> Path:
    """Get the logs directory path."""
    config = LogsConfig()
    return config.logs_dir


def generate_log_filename(task_id: str) -> str:
    """Generate log filename with date prefix."""
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    return f"{date_prefix}_{task_id}.md"


def parse_log_content(content: str) -> Dict[str, str]:
    """Parse log content into fields."""
    fields = {}

    # Extract fields using regex
    patterns = {
        "task_id": r"task_id:\s*(.+)",
        "touched_skills": r"touched_skills:\s*(.+)",
        "candidate_found": r"candidate_found:\s*(.+)",
        "decision": r"decision:\s*(.+)",
        "decision_reason": r"decision_reason:\s*(.+)",
        "confirmation_step_1": r"confirmation_step_1:\s*(.+)",
        "confirmation_step_2": r"confirmation_step_2:\s*(.+)",
        "changes_applied": r"changes_applied:\s*(.+)",
        "validation": r"validation:\s*(.+)",
        "followups": r"followups:\s*(.+)",
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            fields[field] = match.group(1).strip()

    return fields


def list_logs(logs_dir: Path) -> List[Path]:
    """List all log files sorted by modification time (newest first)."""
    if not logs_dir.exists():
        return []

    logs = [
        f for f in logs_dir.iterdir()
        if f.is_file() and f.suffix == ".md" and f.name != "README.md"
    ]

    # Sort by modification time (newest first)
    return sorted(logs, key=lambda f: f.stat().st_mtime, reverse=True)


def get_total_size(logs: List[Path]) -> int:
    """Get total size of logs in bytes."""
    return sum(log.stat().st_size for log in logs)


def format_size(bytes_size: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f}TB"


def cleanup_logs(
    logs_dir: Optional[Path] = None,
    dry_run: bool = False,
    max_count: Optional[int] = None,
    config: Optional[LogsConfig] = None
) -> Dict[str, any]:
    """
    Clean up old logs based on count and size limits.

    Args:
        logs_dir: Directory containing logs (deprecated, use config instead)
        dry_run: If True, don't delete, just report what would be deleted
        max_count: Override max log count
        config: LogsConfig instance (preferred over logs_dir)

    Returns:
        Dict with cleanup statistics
    """
    if config is None:
        if logs_dir is None:
            config = LogsConfig()
        else:
            # Backward compatibility: create config from logs_dir
            config = LogsConfig(logs_dir=logs_dir)

    max_logs = max_count if max_count is not None else config.max_logs
    max_size_bytes = config.max_size_mb * 1024 * 1024

    logs = list_logs(config.logs_dir)
    total_size = get_total_size(logs)

    result = {
        "total_before": len(logs),
        "size_before": total_size,
        "deleted_count": 0,
        "deleted_size": 0,
        "logs_deleted": [],
    }

    # Step 1: Apply count limit (keep newest)
    logs_to_delete = []
    if len(logs) > max_logs:
        logs_to_delete.extend(logs[max_logs:])

    # Step 2: Apply size limit (keep newest, delete oldest)
    remaining_logs = logs[:max_logs]
    current_size = get_total_size(remaining_logs)

    if current_size > max_size_bytes:
        # Delete oldest logs until under size limit
        for log in reversed(remaining_logs):
            if current_size <= max_size_bytes:
                break
            if log not in logs_to_delete:
                logs_to_delete.append(log)
                current_size -= log.stat().st_size

    # Perform deletion
    for log in logs_to_delete:
        result["deleted_count"] += 1
        result["deleted_size"] += log.stat().st_size
        result["logs_deleted"].append(log.name)

        if not dry_run:
            log.unlink()

    return result


@click.group()
def cli():
    """Governance log management tool."""
    pass


@cli.command()
@click.option("--task-id", required=True, help="Task identifier")
@click.option("--interactive", is_flag=True, help="Interactive mode with prompts")
def create(task_id: str, interactive: bool):
    """Create a new governance log."""
    config = LogsConfig()
    logs_dir = config.logs_dir
    logs_dir.mkdir(parents=True, exist_ok=True)

    filename = generate_log_filename(task_id)
    log_path = logs_dir / filename

    if log_path.exists():
        click.echo(f"Error: Log already exists: {filename}", err=True)
        sys.exit(1)

    # Interactive prompts
    if interactive:
        click.echo("Creating governance log (press Enter to skip optional fields)\n")

        touched_skills = click.prompt("Touched skills (comma-separated)", default="")
        candidate_found = click.prompt("Candidate found (yes/no)", default="no")
        decision = click.prompt("Decision (update-existing/create-new/none)", default="none")
        decision_reason = click.prompt("Decision reason", default="")
        confirmation_step_1 = click.prompt("Confirmation step 1", default="")
        confirmation_step_2 = click.prompt("Confirmation step 2", default="")
        changes_applied = click.prompt("Changes applied", default="")
        validation = click.prompt("Validation", default="")
        followups = click.prompt("Follow-ups (optional)", default="")
    else:
        # Non-interactive: use defaults
        touched_skills = ""
        candidate_found = "no"
        decision = "none"
        decision_reason = ""
        confirmation_step_1 = ""
        confirmation_step_2 = ""
        changes_applied = ""
        validation = ""
        followups = ""

    # Generate log content
    content = f"""# Governance Record

- task_id: {task_id}
- touched_skills: {touched_skills}
- candidate_found: {candidate_found}
- decision: {decision}
- decision_reason: {decision_reason}
- confirmation_step_1: {confirmation_step_1}
- confirmation_step_2: {confirmation_step_2}
- changes_applied: {changes_applied}
- validation: {validation}
- followups: {followups}
"""

    # Write log file
    log_path.write_text(content, encoding="utf-8")
    click.echo(f"\n✅ Log created: {filename}")

    # Auto-cleanup after creation
    click.echo("\nChecking for automatic cleanup...")
    result = cleanup_logs(config=config, dry_run=False)

    if result["deleted_count"] > 0:
        click.echo(f"🗑️  Cleaned up {result['deleted_count']} old logs ({format_size(result['deleted_size'])} freed)")

    # Warning if approaching limit
    remaining = result["total_before"] - result["deleted_count"]
    if remaining >= config.warning_threshold:
        click.echo(f"\n⚠️  Warning: {remaining} logs stored (limit: {config.max_logs})")
        click.echo("   Consider adjusting SKILLCTL_MAX_LOGS if needed")


@cli.command("list")
@click.option("--last", type=int, help="Show last N logs")
@click.option("--skill", help="Filter by skill name")
@click.option("--since", help="Filter by date (YYYY-MM-DD)")
def list_cmd(last: Optional[int], skill: Optional[str], since: Optional[str]):
    """List governance logs."""
    config = LogsConfig()
    logs_dir = config.logs_dir

    if not logs_dir.exists():
        click.echo("No logs directory found")
        return

    logs = list_logs(logs_dir)

    if not logs:
        click.echo("No logs found")
        return

    # Apply filters
    filtered_logs = logs

    if skill:
        filtered_logs = [
            log for log in filtered_logs
            if skill.lower() in log.read_text(encoding="utf-8").lower()
        ]

    if since:
        try:
            since_date = datetime.strptime(since, "%Y-%m-%d")
            filtered_logs = [
                log for log in filtered_logs
                if datetime.fromtimestamp(log.stat().st_mtime) >= since_date
            ]
        except ValueError:
            click.echo(f"Error: Invalid date format: {since} (expected YYYY-MM-DD)", err=True)
            sys.exit(1)

    if last:
        filtered_logs = filtered_logs[:last]

    # Display logs
    click.echo(f"{'Log File':<40} {'Modified':<20} {'Size':<10}")
    click.echo("=" * 70)

    for log in filtered_logs:
        mtime = datetime.fromtimestamp(log.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        size = format_size(log.stat().st_size)
        click.echo(f"{log.name:<40} {mtime:<20} {size:<10}")

    # Summary
    total_logs = len(logs)
    total_size = get_total_size(logs)
    click.echo("=" * 70)
    click.echo(f"Total: {total_logs} logs, {format_size(total_size)}")

    if len(filtered_logs) < total_logs:
        click.echo(f"Showing: {len(filtered_logs)} logs (filtered)")


@cli.command()
@click.argument("log_id")
def show(log_id: str):
    """Show content of a specific log."""
    config = LogsConfig()
    logs_dir = config.logs_dir

    # Try to find log by ID
    log_path = None

    # Direct match
    if (logs_dir / log_id).exists():
        log_path = logs_dir / log_id
    elif (logs_dir / f"{log_id}.md").exists():
        log_path = logs_dir / f"{log_id}.md"
    else:
        # Search for partial match
        for log in list_logs(logs_dir):
            if log_id in log.name:
                log_path = log
                break

    if not log_path:
        click.echo(f"Error: Log not found: {log_id}", err=True)
        sys.exit(1)

    # Display content
    content = log_path.read_text(encoding="utf-8")
    click.echo(f"\n{'='*60}")
    click.echo(f"Log: {log_path.name}")
    click.echo(f"{'='*60}\n")
    click.echo(content)


@cli.command()
@click.option("--decision", help="Filter by decision type")
@click.option("--text", help="Search by text content")
def search(decision: Optional[str], text: Optional[str]):
    """Search logs by criteria."""
    config = LogsConfig()
    logs_dir = config.logs_dir

    if not logs_dir.exists():
        click.echo("No logs directory found")
        return

    logs = list_logs(logs_dir)
    results = []

    for log in logs:
        content = log.read_text(encoding="utf-8")
        fields = parse_log_content(content)

        match = True

        if decision:
            if fields.get("decision", "").lower() != decision.lower():
                match = False

        if text:
            if text.lower() not in content.lower():
                match = False

        if match:
            results.append((log, fields))

    # Display results
    if not results:
        click.echo("No matching logs found")
        return

    click.echo(f"Found {len(results)} matching logs:\n")

    for log, fields in results:
        click.echo(f"📄 {log.name}")
        if "task_id" in fields:
            click.echo(f"   Task: {fields['task_id']}")
        if "decision" in fields:
            click.echo(f"   Decision: {fields['decision']}")
        if "touched_skills" in fields:
            click.echo(f"   Skills: {fields['touched_skills']}")
        click.echo()


@cli.command()
@click.option("--dry-run", is_flag=True, help="Preview what would be deleted")
@click.option("--max-count", type=int, help="Override max log count")
def cleanup(dry_run: bool, max_count: Optional[int]):
    """Clean up old logs based on configured limits."""
    config = LogsConfig()
    logs_dir = config.logs_dir

    if not logs_dir.exists():
        click.echo("No logs directory found")
        return

    max_logs = max_count if max_count is not None else config.max_logs
    max_size_mb = config.max_size_mb

    click.echo(f"Cleanup configuration:")
    click.echo(f"  Max logs: {max_logs}")
    click.echo(f"  Max size: {max_size_mb}MB")
    click.echo()

    result = cleanup_logs(config=config, dry_run=dry_run, max_count=max_count)

    if result["deleted_count"] == 0:
        click.echo("✅ No cleanup needed")
        click.echo(f"   Current: {result['total_before']} logs, {format_size(result['size_before'])}")
    else:
        if dry_run:
            click.echo(f"[DRY RUN] Would delete {result['deleted_count']} logs:")
        else:
            click.echo(f"🗑️  Deleted {result['deleted_count']} logs:")

        click.echo(f"   Total freed: {format_size(result['deleted_size'])}")
        click.echo(f"   Remaining: {result['total_before'] - result['deleted_count']} logs")
        click.echo()
        click.echo("Deleted files:")
        for filename in result["logs_deleted"]:
            click.echo(f"  - {filename}")


if __name__ == "__main__":
    cli()
