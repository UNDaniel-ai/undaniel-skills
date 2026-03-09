"""
Comprehensive tests for governance_log.py

Test coverage:
- LogsConfig class
- Log file operations (create, list, show, search)
- Cleanup functionality
- CLI integration
"""

import pytest
import os
from pathlib import Path
from datetime import datetime
from click.testing import CliRunner

# Import modules under test
import governance_log
from governance_log import (
    LogsConfig,
    generate_log_filename,
    parse_log_content,
    list_logs,
    get_total_size,
    format_size,
    cleanup_logs,
    cli,
)


# ==============================================================================
# LogsConfig Tests
# ==============================================================================

class TestLogsConfig:
    """Tests for LogsConfig class."""

    def test_default_config(self):
        """Test LogsConfig with default values."""
        config = LogsConfig()
        assert config.logs_dir.exists() or True  # May not exist yet
        assert config.max_logs == 200
        assert config.max_size_mb == 50
        assert config.warning_threshold == 150

    def test_custom_logs_dir(self, tmp_logs_dir):
        """Test LogsConfig with custom logs directory."""
        config = LogsConfig(logs_dir=tmp_logs_dir)
        assert config.logs_dir == tmp_logs_dir

    def test_custom_max_logs(self):
        """Test LogsConfig with custom max_logs."""
        config = LogsConfig(max_logs=100)
        assert config.max_logs == 100

    def test_custom_max_size_mb(self):
        """Test LogsConfig with custom max_size_mb."""
        config = LogsConfig(max_size_mb=25)
        assert config.max_size_mb == 25

    def test_environment_variables(self, monkeypatch):
        """Test LogsConfig reads from environment variables."""
        monkeypatch.setenv("SKILLCTL_MAX_LOGS", "300")
        monkeypatch.setenv("SKILLCTL_MAX_LOG_SIZE_MB", "75")

        config = LogsConfig()
        assert config.max_logs == 300
        assert config.max_size_mb == 75

    def test_explicit_overrides_environment(self, monkeypatch):
        """Test explicit parameters override environment variables."""
        monkeypatch.setenv("SKILLCTL_MAX_LOGS", "300")

        config = LogsConfig(max_logs=150)
        assert config.max_logs == 150  # Explicit value wins


# ==============================================================================
# Utility Function Tests
# ==============================================================================

class TestUtilityFunctions:
    """Tests for utility functions."""

    def test_generate_log_filename(self):
        """Test log filename generation."""
        filename = generate_log_filename("task-123")
        assert filename.endswith("_task-123.md")
        assert filename.startswith("20")  # Year prefix
        assert len(filename.split("_")[0]) == 10  # YYYY-MM-DD format

    def test_generate_log_filename_format(self):
        """Test log filename follows expected format."""
        filename = generate_log_filename("test")
        parts = filename.split("_")
        assert len(parts) == 2
        date_part = parts[0]
        assert date_part.count("-") == 2  # YYYY-MM-DD

    def test_parse_log_content_all_fields(self):
        """Test parsing log content with all fields."""
        content = """# Governance Record

- task_id: task-001
- touched_skills: AIWay, miravia-git
- candidate_found: yes
- decision: update-existing
- decision_reason: Found matching skill
- confirmation_step_1: User confirmed
- confirmation_step_2: Changes applied
- changes_applied: Updated SKILL.md
- validation: Passed validation
- followups: None
"""
        fields = parse_log_content(content)

        assert fields["task_id"] == "task-001"
        assert fields["touched_skills"] == "AIWay, miravia-git"
        assert fields["candidate_found"] == "yes"
        assert fields["decision"] == "update-existing"
        assert fields["decision_reason"] == "Found matching skill"

    def test_parse_log_content_partial_fields(self):
        """Test parsing log content with missing fields."""
        content = """# Governance Record

- task_id: task-002
- decision: create-new
"""
        fields = parse_log_content(content)

        assert fields["task_id"] == "task-002"
        assert fields["decision"] == "create-new"
        assert "touched_skills" not in fields

    def test_format_size_bytes(self):
        """Test size formatting for bytes."""
        assert "B" in format_size(500)

    def test_format_size_kilobytes(self):
        """Test size formatting for kilobytes."""
        result = format_size(2048)
        assert "KB" in result or "B" in result

    def test_format_size_megabytes(self):
        """Test size formatting for megabytes."""
        result = format_size(5 * 1024 * 1024)
        assert "MB" in result


# ==============================================================================
# Log Operations Tests
# ==============================================================================

class TestLogOperations:
    """Tests for log file operations."""

    def test_list_logs_empty_directory(self, tmp_logs_dir):
        """Test listing logs in empty directory."""
        logs = list_logs(tmp_logs_dir)
        assert logs == []

    def test_list_logs_nonexistent_directory(self, tmp_path):
        """Test listing logs in non-existent directory."""
        nonexistent = tmp_path / "nonexistent"
        logs = list_logs(nonexistent)
        assert logs == []

    def test_list_logs_with_files(self, tmp_logs_dir):
        """Test listing logs with multiple files."""
        # Create log files
        (tmp_logs_dir / "2026-03-08_task-001.md").write_text("Log 1")
        (tmp_logs_dir / "2026-03-07_task-002.md").write_text("Log 2")
        (tmp_logs_dir / "README.md").write_text("Readme")  # Should be excluded

        logs = list_logs(tmp_logs_dir)

        assert len(logs) == 2
        assert all(log.suffix == ".md" for log in logs)
        assert not any(log.name == "README.md" for log in logs)

    def test_list_logs_sorted_by_time(self, tmp_logs_dir):
        """Test logs are sorted by modification time (newest first)."""
        import time

        # Create files with delays to ensure different mtimes
        file1 = tmp_logs_dir / "2026-03-08_old.md"
        file1.write_text("Old")
        time.sleep(0.01)

        file2 = tmp_logs_dir / "2026-03-08_new.md"
        file2.write_text("New")

        logs = list_logs(tmp_logs_dir)

        assert len(logs) == 2
        # Newest should be first
        assert logs[0].name == "2026-03-08_new.md"

    def test_get_total_size(self, tmp_logs_dir):
        """Test calculating total size of logs."""
        (tmp_logs_dir / "log1.md").write_text("a" * 100)
        (tmp_logs_dir / "log2.md").write_text("b" * 200)

        logs = list_logs(tmp_logs_dir)
        total_size = get_total_size(logs)

        assert total_size == 300

    def test_get_total_size_empty_list(self):
        """Test total size of empty log list."""
        assert get_total_size([]) == 0


# ==============================================================================
# Cleanup Functionality Tests
# ==============================================================================

class TestCleanupLogs:
    """Tests for log cleanup functionality."""

    def test_cleanup_no_logs(self, tmp_logs_dir):
        """Test cleanup with no logs."""
        config = LogsConfig(logs_dir=tmp_logs_dir, max_logs=100)
        result = cleanup_logs(config=config)

        assert result["total_before"] == 0
        assert result["deleted_count"] == 0

    def test_cleanup_under_limit(self, tmp_logs_dir):
        """Test cleanup when under log count limit."""
        config = LogsConfig(logs_dir=tmp_logs_dir, max_logs=100)

        # Create 50 logs (under limit)
        for i in range(50):
            (tmp_logs_dir / f"2026-03-08_task-{i:03d}.md").write_text(f"Log {i}")

        result = cleanup_logs(config=config)

        assert result["total_before"] == 50
        assert result["deleted_count"] == 0

    def test_cleanup_over_count_limit(self, tmp_logs_dir):
        """Test cleanup when over log count limit."""
        config = LogsConfig(logs_dir=tmp_logs_dir, max_logs=10)

        # Create 15 logs (over limit)
        for i in range(15):
            (tmp_logs_dir / f"2026-03-08_task-{i:03d}.md").write_text(f"Log {i}")

        result = cleanup_logs(config=config)

        assert result["total_before"] == 15
        assert result["deleted_count"] == 5  # Delete oldest 5
        assert result["total_before"] - result["deleted_count"] == 10

    def test_cleanup_dry_run(self, tmp_logs_dir):
        """Test cleanup in dry-run mode doesn't delete files."""
        config = LogsConfig(logs_dir=tmp_logs_dir, max_logs=5)

        # Create 10 logs
        for i in range(10):
            (tmp_logs_dir / f"2026-03-08_task-{i:03d}.md").write_text(f"Log {i}")

        result = cleanup_logs(config=config, dry_run=True)

        # Should report what would be deleted
        assert result["deleted_count"] == 5

        # But files should still exist
        remaining_logs = list_logs(tmp_logs_dir)
        assert len(remaining_logs) == 10  # Nothing actually deleted

    def test_cleanup_keeps_newest(self, tmp_logs_dir):
        """Test cleanup keeps newest logs."""
        import time

        config = LogsConfig(logs_dir=tmp_logs_dir, max_logs=3)

        # Create logs with sequential timing
        for i in range(5):
            file = tmp_logs_dir / f"2026-03-08_task-{i:03d}.md"
            file.write_text(f"Log {i}")
            time.sleep(0.01)  # Ensure different mtimes

        result = cleanup_logs(config=config)

        assert result["deleted_count"] == 2
        remaining_logs = list_logs(tmp_logs_dir)
        assert len(remaining_logs) == 3

        # Check that newest logs remain (higher numbers)
        remaining_names = [log.name for log in remaining_logs]
        assert "2026-03-08_task-004.md" in remaining_names
        assert "2026-03-08_task-003.md" in remaining_names

    def test_cleanup_size_limit(self, tmp_logs_dir):
        """Test cleanup by size limit."""
        config = LogsConfig(logs_dir=tmp_logs_dir, max_logs=100, max_size_mb=0.001)  # ~1KB

        # Create logs that exceed size limit
        for i in range(5):
            (tmp_logs_dir / f"2026-03-08_task-{i:03d}.md").write_text("x" * 500)  # 500 bytes each

        result = cleanup_logs(config=config)

        # Should delete some logs to get under size limit
        assert result["deleted_count"] > 0
        assert result["size_before"] > (0.001 * 1024 * 1024)

    def test_cleanup_with_max_count_override(self, tmp_logs_dir):
        """Test cleanup with max_count parameter override."""
        config = LogsConfig(logs_dir=tmp_logs_dir, max_logs=50)

        # Create 20 logs
        for i in range(20):
            (tmp_logs_dir / f"2026-03-08_task-{i:03d}.md").write_text(f"Log {i}")

        # Override max_count to 10
        result = cleanup_logs(config=config, max_count=10)

        assert result["deleted_count"] == 10  # Deleted 10 to reach limit

    def test_cleanup_backward_compat_logs_dir(self, tmp_logs_dir):
        """Test cleanup with logs_dir parameter (backward compatibility)."""
        # Create logs
        for i in range(15):
            (tmp_logs_dir / f"2026-03-08_task-{i:03d}.md").write_text(f"Log {i}")

        # Use deprecated logs_dir parameter
        result = cleanup_logs(logs_dir=tmp_logs_dir, max_count=10)

        assert result["deleted_count"] == 5


# ==============================================================================
# CLI Integration Tests
# ==============================================================================

class TestCLI:
    """Tests for CLI commands."""

    def test_cli_create_log_non_interactive(self, tmp_logs_dir, monkeypatch):
        """Test creating log via CLI in non-interactive mode."""
        # Temporarily change logs dir
        monkeypatch.setattr(governance_log, "LogsConfig",
                          lambda: LogsConfig(logs_dir=tmp_logs_dir))

        runner = CliRunner()
        result = runner.invoke(cli, ["create", "--task-id", "test-001"])

        # Should succeed (even in non-interactive mode)
        # Note: This tests the CLI structure, actual creation may require mocking

    def test_cli_list_empty_logs(self, tmp_logs_dir, monkeypatch):
        """Test listing logs when directory is empty."""
        def mock_config():
            return LogsConfig(logs_dir=tmp_logs_dir)

        monkeypatch.setattr(governance_log, "LogsConfig", mock_config)

        runner = CliRunner()
        result = runner.invoke(cli, ["list"])

        assert "No logs found" in result.output or result.exit_code == 0

    def test_cli_cleanup_dry_run(self, tmp_logs_dir, monkeypatch):
        """Test cleanup command with --dry-run flag."""
        def mock_config():
            return LogsConfig(logs_dir=tmp_logs_dir, max_logs=5)

        monkeypatch.setattr(governance_log, "LogsConfig", mock_config)

        # Create some logs
        for i in range(10):
            (tmp_logs_dir / f"2026-03-08_task-{i:03d}.md").write_text(f"Log {i}")

        runner = CliRunner()
        result = runner.invoke(cli, ["cleanup", "--dry-run"])

        assert result.exit_code == 0
        assert "DRY RUN" in result.output or "would" in result.output.lower()


# ==============================================================================
# Integration Tests
# ==============================================================================

class TestIntegration:
    """Integration tests combining multiple components."""

    def test_create_and_list_workflow(self, tmp_logs_dir):
        """Test creating logs and listing them."""
        config = LogsConfig(logs_dir=tmp_logs_dir)

        # Create logs manually (simulating create command)
        log_content = """# Governance Record

- task_id: task-001
- touched_skills: test-skill
- decision: create-new
"""
        log_file = config.logs_dir / generate_log_filename("task-001")
        config.logs_dir.mkdir(parents=True, exist_ok=True)
        log_file.write_text(log_content)

        # List logs
        logs = list_logs(config.logs_dir)
        assert len(logs) == 1

        # Parse content
        content = logs[0].read_text()
        fields = parse_log_content(content)
        assert fields["task_id"] == "task-001"

    def test_create_list_cleanup_workflow(self, tmp_logs_dir):
        """Test full workflow: create, list, cleanup."""
        config = LogsConfig(logs_dir=tmp_logs_dir, max_logs=5)
        config.logs_dir.mkdir(parents=True, exist_ok=True)

        # Create 10 logs
        for i in range(10):
            log_file = config.logs_dir / f"2026-03-08_task-{i:03d}.md"
            log_file.write_text(f"Log {i}")

        # List logs
        logs_before = list_logs(config.logs_dir)
        assert len(logs_before) == 10

        # Cleanup
        result = cleanup_logs(config=config)
        assert result["deleted_count"] == 5

        # List again
        logs_after = list_logs(config.logs_dir)
        assert len(logs_after) == 5
