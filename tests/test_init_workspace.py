"""
Tests for workspace AGENTS.md bootstrap tooling.
"""

from pathlib import Path

import pytest
from click.testing import CliRunner

import init_workspace
from init_workspace import bootstrap_workspace, main, render_template, shared_skill_paths


@pytest.fixture
def tmp_workspace_repo(tmp_path: Path) -> Path:
    """Create a temporary repo layout with a workspace template."""
    repo_root = tmp_path / "repo"
    templates_dir = repo_root / "templates" / "workspace"
    tools_dir = repo_root / "tools"

    templates_dir.mkdir(parents=True)
    tools_dir.mkdir()

    (templates_dir / "AGENTS.md.template").write_text(
        "\n".join(
            [
                "repo={{LULU_SKILLS_COMMON_ROOT}}",
                "entry={{UND_WORKFLOW_ENTRY_PATH}}",
                "brainstorm={{UND_BRAINSTORMING_PATH}}",
                "plans={{UND_WRITING_PLANS_PATH}}",
                "subagent={{UND_SUBAGENT_DRIVEN_DEVELOPMENT_PATH}}",
                "tdd={{UND_TEST_DRIVEN_DEVELOPMENT_PATH}}",
                "debug={{UND_SYSTEMATIC_DEBUGGING_PATH}}",
                "verify={{UND_VERIFICATION_BEFORE_COMPLETION_PATH}}",
                "complex={{COMPLEX_TASK_SOLVER_PATH}}",
                "workspace={{WORKSPACE_STRUCTURE_MANAGER_PATH}}",
                "skills={{SKILLS_MANAGER_PATH}}",
                "authoring={{UND_WRITING_SKILLS_PATH}}",
            ]
        ),
        encoding="utf-8",
    )

    return repo_root


def test_render_template_injects_absolute_paths(tmp_workspace_repo: Path):
    """Template rendering should substitute shared repo and skill paths."""
    rendered = render_template(tmp_workspace_repo)

    assert f"repo={tmp_workspace_repo}" in rendered
    assert str(tmp_workspace_repo / "skills" / "und-workflow-entry" / "SKILL.md") in rendered
    assert str(tmp_workspace_repo / "skills" / "und-brainstorming" / "SKILL.md") in rendered
    assert str(tmp_workspace_repo / "skills" / "und-writing-plans" / "SKILL.md") in rendered
    assert str(tmp_workspace_repo / "skills" / "und-subagent-driven-development" / "SKILL.md") in rendered
    assert str(tmp_workspace_repo / "skills" / "und-test-driven-development" / "SKILL.md") in rendered
    assert str(tmp_workspace_repo / "skills" / "und-systematic-debugging" / "SKILL.md") in rendered
    assert str(tmp_workspace_repo / "skills" / "und-verification-before-completion" / "SKILL.md") in rendered
    assert str(tmp_workspace_repo / "skills" / "complex-task-solver" / "SKILL.md") in rendered
    assert str(tmp_workspace_repo / "skills" / "workspace-structure-manager" / "SKILL.md") in rendered
    assert str(tmp_workspace_repo / "skills" / "skills-manager" / "SKILL.md") in rendered
    assert str(tmp_workspace_repo / "skills" / "und-writing-skills" / "SKILL.md") in rendered


def test_shared_skill_paths_includes_phase2_to_phase4_skills(tmp_workspace_repo: Path):
    """Shared skill path helper should include the current workflow method skills."""
    paths = shared_skill_paths(tmp_workspace_repo)

    assert "{{UND_WORKFLOW_ENTRY_PATH}}" in paths
    assert "{{UND_BRAINSTORMING_PATH}}" in paths
    assert "{{UND_WRITING_PLANS_PATH}}" in paths
    assert "{{UND_SUBAGENT_DRIVEN_DEVELOPMENT_PATH}}" in paths
    assert "{{UND_TEST_DRIVEN_DEVELOPMENT_PATH}}" in paths
    assert "{{UND_SYSTEMATIC_DEBUGGING_PATH}}" in paths
    assert "{{UND_VERIFICATION_BEFORE_COMPLETION_PATH}}" in paths
    assert "{{UND_WRITING_SKILLS_PATH}}" in paths
    assert paths["{{UND_WORKFLOW_ENTRY_PATH}}"].endswith("skills/und-workflow-entry/SKILL.md")
    assert paths["{{UND_BRAINSTORMING_PATH}}"].endswith("skills/und-brainstorming/SKILL.md")
    assert paths["{{UND_WRITING_PLANS_PATH}}"].endswith("skills/und-writing-plans/SKILL.md")
    assert paths["{{UND_SUBAGENT_DRIVEN_DEVELOPMENT_PATH}}"].endswith("skills/und-subagent-driven-development/SKILL.md")
    assert paths["{{UND_TEST_DRIVEN_DEVELOPMENT_PATH}}"].endswith("skills/und-test-driven-development/SKILL.md")
    assert paths["{{UND_SYSTEMATIC_DEBUGGING_PATH}}"].endswith("skills/und-systematic-debugging/SKILL.md")
    assert paths["{{UND_VERIFICATION_BEFORE_COMPLETION_PATH}}"].endswith("skills/und-verification-before-completion/SKILL.md")
    assert paths["{{UND_WRITING_SKILLS_PATH}}"].endswith("skills/und-writing-skills/SKILL.md")


def test_bootstrap_workspace_creates_agents_file(tmp_workspace_repo: Path, tmp_path: Path):
    """Bootstrap should create AGENTS.md when missing."""
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()

    target = bootstrap_workspace(workspace_dir, tmp_workspace_repo)

    assert target == workspace_dir / "AGENTS.md"
    assert target.exists()
    content = target.read_text(encoding="utf-8")
    assert "entry=" in content
    assert "brainstorm=" in content
    assert "plans=" in content
    assert "subagent=" in content
    assert "tdd=" in content
    assert "debug=" in content
    assert "verify=" in content
    assert "complex=" in content
    assert "workspace=" in content
    assert "skills=" in content
    assert "authoring=" in content


def test_bootstrap_workspace_refuses_overwrite_without_force(tmp_workspace_repo: Path, tmp_path: Path):
    """Bootstrap should not overwrite an existing AGENTS.md by default."""
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()
    target = workspace_dir / "AGENTS.md"
    target.write_text("original", encoding="utf-8")

    with pytest.raises(FileExistsError):
        bootstrap_workspace(workspace_dir, tmp_workspace_repo)

    assert target.read_text(encoding="utf-8") == "original"


def test_bootstrap_workspace_overwrites_with_force(tmp_workspace_repo: Path, tmp_path: Path):
    """Bootstrap should overwrite when force=True."""
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()
    target = workspace_dir / "AGENTS.md"
    target.write_text("original", encoding="utf-8")

    bootstrap_workspace(workspace_dir, tmp_workspace_repo, force=True)

    assert target.read_text(encoding="utf-8") != "original"
    assert "entry=" in target.read_text(encoding="utf-8")
    assert "subagent=" in target.read_text(encoding="utf-8")
    assert "tdd=" in target.read_text(encoding="utf-8")
    assert "complex=" in target.read_text(encoding="utf-8")


def test_cli_bootstraps_current_workspace(tmp_workspace_repo: Path, tmp_path: Path, monkeypatch):
    """CLI should default target workspace to the current directory."""
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()
    monkeypatch.chdir(workspace_dir)

    runner = CliRunner()
    result = runner.invoke(main, ["--repo-root", str(tmp_workspace_repo)])

    assert result.exit_code == 0
    assert (workspace_dir / "AGENTS.md").exists()


def test_cli_returns_error_when_agents_exists_without_force(
    tmp_workspace_repo: Path,
    tmp_path: Path,
    monkeypatch,
):
    """CLI should fail safely when AGENTS.md already exists."""
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()
    (workspace_dir / "AGENTS.md").write_text("original", encoding="utf-8")
    monkeypatch.chdir(workspace_dir)

    runner = CliRunner()
    result = runner.invoke(main, ["--repo-root", str(tmp_workspace_repo)])

    assert result.exit_code != 0
    assert "already exists" in result.output
    assert (workspace_dir / "AGENTS.md").read_text(encoding="utf-8") == "original"
