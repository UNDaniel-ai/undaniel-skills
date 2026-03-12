#!/usr/bin/env python3
"""
Run Codex behavior fixtures against a bootstrapped workspace.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import click

from init_workspace import bootstrap_workspace, default_repo_root

DEFAULT_TIMEOUT_SECONDS = 90


@dataclass
class CodexTurnResult:
    """Structured output for one Codex turn."""

    prompt: str
    command: List[str]
    exit_code: int
    events: List[Dict[str, Any]]
    non_json_lines: List[str]
    agent_messages: List[str]
    thread_id: Optional[str]
    stderr: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def load_fixture(path: Path) -> Dict[str, Any]:
    """Load a JSON fixture definition while preserving extra metadata fields."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_jsonl_output(output: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Parse JSONL output while preserving non-JSON lines for debugging."""
    events: List[Dict[str, Any]] = []
    non_json_lines: List[str] = []

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            non_json_lines.append(line)

    return events, non_json_lines


def extract_thread_id(events: List[Dict[str, Any]]) -> Optional[str]:
    """Extract the thread id from Codex events."""
    for event in events:
        if event.get("type") == "thread.started":
            return event.get("thread_id")
    return None


def extract_agent_messages(events: List[Dict[str, Any]]) -> List[str]:
    """Extract completed agent message texts from Codex events."""
    messages: List[str] = []

    for event in events:
        if event.get("type") != "item.completed":
            continue

        item = event.get("item", {})
        if item.get("type") != "agent_message":
            continue

        text = item.get("text")
        if isinstance(text, str) and text.strip():
            messages.append(text)

    return messages


def build_exec_command(
    prompt: str,
    ephemeral: bool,
    skip_git_repo_check: bool = True,
) -> List[str]:
    """Build a `codex exec` command."""
    command = ["codex", "exec", "--json", "--sandbox", "read-only"]

    if skip_git_repo_check:
        command.append("--skip-git-repo-check")
    if ephemeral:
        command.append("--ephemeral")

    command.append(prompt)
    return command


def build_resume_command(
    thread_id: str,
    prompt: str,
    skip_git_repo_check: bool = True,
) -> List[str]:
    """Build a `codex exec resume` command."""
    command = ["codex", "exec", "resume", "--json"]

    if skip_git_repo_check:
        command.append("--skip-git-repo-check")

    command.extend([thread_id, prompt])
    return command


def run_turn(
    prompt: str,
    cwd: Path,
    timeout_seconds: int,
    thread_id: Optional[str] = None,
    ephemeral: bool = False,
) -> CodexTurnResult:
    """Run a single Codex turn."""
    cwd = Path(cwd).resolve()
    if thread_id is None:
        command = build_exec_command(prompt, ephemeral=ephemeral)
    else:
        command = build_resume_command(thread_id, prompt)

    completed = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )

    events, non_json_lines = parse_jsonl_output(completed.stdout)
    result = CodexTurnResult(
        prompt=prompt,
        command=command,
        exit_code=completed.returncode,
        events=events,
        non_json_lines=non_json_lines,
        agent_messages=extract_agent_messages(events),
        thread_id=extract_thread_id(events),
        stderr=completed.stderr,
    )

    if completed.returncode != 0:
        raise RuntimeError(
            f"Codex turn failed with exit code {completed.returncode}: {completed.stderr or completed.stdout}"
        )

    if not result.events:
        raise RuntimeError("Codex produced no JSON events")

    return result


def run_fixture(
    fixture_path: Path,
    repo_root: Optional[Path] = None,
    workspace: Optional[Path] = None,
) -> Dict[str, Any]:
    """Run all turns in a fixture inside a bootstrapped test workspace."""
    fixture_path = Path(fixture_path).resolve()
    fixture = load_fixture(fixture_path)
    repo_root = default_repo_root() if repo_root is None else Path(repo_root).resolve()

    timeout_seconds = int(fixture.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
    turns = fixture.get("turns", [])
    if not turns:
        raise ValueError(f"Fixture has no turns: {fixture_path}")

    if workspace is not None:
        workspace_path = Path(workspace).resolve()
        bootstrap_workspace(workspace_path, repo_root, force=True)
        return _run_fixture_turns(turns, workspace_path, timeout_seconds)

    with tempfile.TemporaryDirectory(prefix="codex-fixture-") as temp_dir:
        workspace_path = Path(temp_dir)
        bootstrap_workspace(workspace_path, repo_root)
        return _run_fixture_turns(turns, workspace_path, timeout_seconds)


def _run_fixture_turns(
    turns: List[Dict[str, Any]],
    workspace_path: Path,
    timeout_seconds: int,
) -> Dict[str, Any]:
    """Execute fixture turns inside an already-bootstrapped workspace."""
    thread_id: Optional[str] = None
    results: List[Dict[str, Any]] = []

    for turn in turns:
        prompt = turn["prompt"]
        result = run_turn(
            prompt=prompt,
            cwd=workspace_path,
            timeout_seconds=timeout_seconds,
            thread_id=thread_id,
            ephemeral=bool(turn.get("ephemeral", len(turns) == 1)),
        )
        if result.thread_id:
            thread_id = result.thread_id
        results.append(result.to_dict())

    return {
        "workspace": str(workspace_path),
        "thread_id": thread_id,
        "turns": results,
    }


@click.command()
@click.argument("fixture", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--repo-root",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Path to the lulu-skills-common repository.",
)
@click.option(
    "--workspace",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Reuse a specific workspace directory instead of a temporary one.",
)
def main(fixture: Path, repo_root: Optional[Path], workspace: Optional[Path]):
    """Run a Codex behavior fixture and print a JSON summary."""
    result = run_fixture(fixture, repo_root=repo_root, workspace=workspace)
    click.echo(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
