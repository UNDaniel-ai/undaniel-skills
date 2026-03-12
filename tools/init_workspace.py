#!/usr/bin/env python3
"""
Initialize a workspace-level AGENTS.md from lulu-skills-common.
"""

from pathlib import Path
from typing import Dict, Optional

import click


def default_repo_root() -> Path:
    """Return the repository root based on this script location."""
    return Path(__file__).resolve().parent.parent


def template_path(repo_root: Path) -> Path:
    """Return the workspace AGENTS template path."""
    return repo_root / "templates" / "workspace" / "AGENTS.md.template"


def shared_skill_paths(repo_root: Path) -> Dict[str, str]:
    """Return placeholder replacements for shared skill paths."""
    repo_root = Path(repo_root).resolve()
    return {
        "{{UND_WORKFLOW_ENTRY_PATH}}": str(
            repo_root / "skills" / "und-workflow-entry" / "SKILL.md"
        ),
        "{{UND_BRAINSTORMING_PATH}}": str(
            repo_root / "skills" / "und-brainstorming" / "SKILL.md"
        ),
        "{{UND_WRITING_PLANS_PATH}}": str(
            repo_root / "skills" / "und-writing-plans" / "SKILL.md"
        ),
        "{{UND_SUBAGENT_DRIVEN_DEVELOPMENT_PATH}}": str(
            repo_root / "skills" / "und-subagent-driven-development" / "SKILL.md"
        ),
        "{{UND_TEST_DRIVEN_DEVELOPMENT_PATH}}": str(
            repo_root / "skills" / "und-test-driven-development" / "SKILL.md"
        ),
        "{{UND_SYSTEMATIC_DEBUGGING_PATH}}": str(
            repo_root / "skills" / "und-systematic-debugging" / "SKILL.md"
        ),
        "{{UND_VERIFICATION_BEFORE_COMPLETION_PATH}}": str(
            repo_root / "skills" / "und-verification-before-completion" / "SKILL.md"
        ),
        "{{COMPLEX_TASK_SOLVER_PATH}}": str(
            repo_root / "skills" / "complex-task-solver" / "SKILL.md"
        ),
        "{{WORKSPACE_STRUCTURE_MANAGER_PATH}}": str(
            repo_root / "skills" / "workspace-structure-manager" / "SKILL.md"
        ),
        "{{SKILLS_MANAGER_PATH}}": str(
            repo_root / "skills" / "skills-manager" / "SKILL.md"
        ),
        "{{UND_WRITING_SKILLS_PATH}}": str(
            repo_root / "skills" / "und-writing-skills" / "SKILL.md"
        ),
    }


def render_template(repo_root: Path) -> str:
    """Render the shared AGENTS template with absolute local paths for this checkout."""
    repo_root = Path(repo_root).resolve()
    template = template_path(repo_root).read_text(encoding="utf-8")

    replacements: Dict[str, str] = {
        "{{LULU_SKILLS_COMMON_ROOT}}": str(repo_root),
    }
    replacements.update(shared_skill_paths(repo_root))

    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    return template


def bootstrap_workspace(
    workspace_dir: Path,
    repo_root: Path,
    force: bool = False,
) -> Path:
    """Write AGENTS.md into the target workspace using the shared bootstrap template."""
    workspace_dir = Path(workspace_dir).resolve()
    repo_root = Path(repo_root).resolve()
    target = workspace_dir / "AGENTS.md"

    if target.exists() and not force:
        raise FileExistsError(f"{target} already exists. Re-run with --force to overwrite.")

    workspace_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(render_template(repo_root), encoding="utf-8")
    return target


@click.command()
@click.argument(
    "target",
    required=False,
    default=".",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--repo-root",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Path to the lulu-skills-common repository. Defaults to the current script repo.",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite an existing AGENTS.md in the target workspace.",
)
def main(target: Path, repo_root: Optional[Path], force: bool):
    """Bootstrap AGENTS.md into TARGET, defaulting to the current directory."""
    resolved_repo_root = default_repo_root() if repo_root is None else repo_root

    try:
        written = bootstrap_workspace(target, resolved_repo_root, force=force)
    except FileExistsError as exc:
        raise click.ClickException(str(exc)) from exc
    except FileNotFoundError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Wrote {written}")


if __name__ == "__main__":
    main()
