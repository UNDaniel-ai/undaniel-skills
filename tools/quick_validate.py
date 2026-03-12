#!/usr/bin/env python3
"""
Quick validation tool for SKILL.md files.

Validates:
- YAML frontmatter format and required fields
- Markdown structure (code blocks, heading levels)
- Code block content (bash syntax, JSON format)
- Link integrity (internal and external)
"""

import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml
    import mistune
    import click
except ImportError as e:
    print(f"Error: Missing required dependency: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)


class ValidatorConfig:
    """Configuration for the validator."""

    def __init__(self, repo_root: Optional[Path] = None):
        if repo_root is None:
            # Default: detect from script location
            script_dir = Path(__file__).parent
            repo_root = script_dir.parent

        self.repo_root = Path(repo_root)
        self.skills_dir = self.repo_root / "skills"


# Skill-specific contract checks for high-impact governance skills.
# Each listed token must appear in the corresponding SKILL.md.
SKILL_CONTRACT_RULES = {
    "complex-task-solver": [
        "## 首轮技能识别协议（防漏触发）",
        "命中的 skill 列表",
        "使用顺序",
        "跳过理由",
        "复杂度预检清单（强制）",
        "阶段门禁协议（Route B / Route C 强制）",
        "显式确认信号协议（双重确定）",
        "带目标阶段名的明确确认语句",
        "不构成阶段确认",
        "未完成 `requirements-alignment.md` 且未获得确认，不得创建 `design.md`。",
        "未完成 `implementation-plan.md` 且未获得确认，不得开始代码编写。",
        "und-brainstorming",
        "und-writing-plans",
        "方法型 skill 调度规则",
        "session-summary.md",
    ],
    "workspace-structure-manager": [
        "## 触发前置检查（防漏触发）",
        "前置检查清单（强制）",
        "session 策略",
        "用户是否指定路径但任务本质仍是开发任务",
        "## Workspace AGENTS.md Bootstrap",
        "tools/init_workspace.py",
        "## Session 门禁策略（强制）",
        "门禁确认记录（强制）",
        "AI 发起确认消息",
        "用户确认原话",
        "当前阶段",
        "是否允许编码",
        "session-summary.md",
    ],
    "skills-manager": [
        "## Skill 识别失败修复流程",
        "机制问题",
        "执行漏触发",
        "tools/skillctl validate --skill <skill-name>",
        "und-writing-skills",
        "automatic trigger",
        "explicit request",
        "multi-turn",
        "fresh verification evidence",
        "Mechanism Completeness Check",
        "tools/init_workspace.py",
        "tests/test_init_workspace.py",
        "tools/quick_validate.py",
        "Knowledge Drift Check",
        "knowledge/*.md",
    ],
    "und-workflow-entry": [
        "use / skip / why / order",
        "session strategy",
        "complex-task-solver",
        "workspace-structure-manager",
        "skills-manager",
        "und-writing-skills",
        "Before the assessment is complete, do not start design, implementation planning, coding, validation, or completion claims.",
    ],
    "und-writing-skills": [
        "description 只写触发条件",
        "automatic trigger",
        "explicit request",
        "multi-turn",
        "semantic assertions",
        "equivalent wording",
        "tools/run_codex_fixture.py",
        "tests/test_init_workspace.py",
        "tools/skillctl validate --skill <skill-name>",
        "Integration Surface Checklist",
        "templates/workspace/AGENTS.md.template",
        "tools/init_workspace.py",
        "tools/quick_validate.py",
        "dispatch / gate",
        "knowledge/*.md",
    ],
    "und-brainstorming": [
        "requirements gap scan",
        "option comparison",
        "design challenge",
        "complex-task-solver",
        "workspace-structure-manager",
        "automatic trigger",
        "explicit request",
        "multi-turn",
    ],
    "und-writing-plans": [
        "前置输入",
        "验证命令",
        "预期结果",
        "Step Acceptance",
        "postcondition",
        "complex-task-solver",
        "workspace-structure-manager",
        "automatic trigger",
        "multi-turn",
    ],
    "und-test-driven-development": [
        "Verify RED",
        "Verify GREEN",
        "TDD 例外",
        "mock",
        "test-only methods",
        "incomplete mocks",
        "complex-task-solver",
        "workspace-structure-manager",
        "automatic trigger",
        "multi-turn",
    ],
    "und-subagent-driven-development": [
        "Capability Detection",
        "tooling_supported",
        "workspace_supported",
        "review_supported",
        "Task Eligibility",
        "Status Model",
        "DONE_WITH_CONCERNS",
        "NEEDS_CONTEXT",
        "BLOCKED",
        "Spec Compliance Review",
        "Code Quality Review",
        "Fallback Protocol",
        "complex-task-solver",
        "workspace-structure-manager",
        "automatic trigger",
        "explicit request",
        "multi-turn",
    ],
    "und-systematic-debugging": [
        "Root Cause Investigation",
        "Pattern Analysis",
        "Hypothesis And Testing",
        "condition-based waiting",
        "defense-in-depth",
        "complex-task-solver",
        "workspace-structure-manager",
        "automatic trigger",
        "explicit request",
        "multi-turn",
    ],
    "und-verification-before-completion": [
        "claim -> command -> output -> evidence",
        "fresh verification evidence",
        "partial verification",
        "agent success report",
        "complex-task-solver",
        "workspace-structure-manager",
        "automatic trigger",
        "explicit request",
        "multi-turn",
    ],
}


class ValidationError:
    """Represents a validation error or warning."""

    def __init__(self, level: str, line: Optional[int], message: str):
        self.level = level  # ERROR or WARN
        self.line = line
        self.message = message

    def __str__(self):
        if self.line:
            return f"  [{self.level}] Line {self.line}: {self.message}"
        return f"  [{self.level}] {self.message}"


class SkillValidator:
    """Validates a single SKILL.md file."""

    def __init__(self, skill_path: Path, content: Optional[str] = None):
        """
        Initialize validator.

        Args:
            skill_path: Path to the skill directory
            content: Optional pre-loaded SKILL.md content for testing
        """
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"
        self._content = content  # For testing: allows injection of content
        self.frontmatter: Dict[str, object] = {}
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
        self.stats = {
            "code_blocks": 0,
            "links": 0,
        }

    def error(self, line: Optional[int], message: str):
        """Add an error."""
        self.errors.append(ValidationError("ERROR", line, message))

    def warn(self, line: Optional[int], message: str):
        """Add a warning."""
        self.warnings.append(ValidationError("WARN", line, message))

    def _read_content(self) -> Optional[str]:
        """Read SKILL.md content. Returns None if file doesn't exist."""
        if self._content is not None:
            # Use injected content (for testing)
            return self._content

        if not self.skill_md.exists():
            return None

        return self.skill_md.read_text(encoding="utf-8")

    def validate(self) -> bool:
        """Run all validation checks. Returns True if no errors."""
        content = self._read_content()

        if content is None:
            self.error(None, f"SKILL.md not found at {self.skill_md}")
            return False

        # Validate YAML frontmatter
        self._validate_yaml_frontmatter(content)
        self._validate_skill_metadata_rules()

        # Validate Markdown structure
        self._validate_markdown_structure(content)

        # Validate code blocks
        self._validate_code_blocks(content)

        # Validate links
        self._validate_links(content)

        # Validate required contracts for specific governance skills
        self._validate_skill_contracts(content)

        return len(self.errors) == 0

    def _validate_yaml_frontmatter(self, content: str):
        """Validate YAML frontmatter format and required fields."""
        # Check for YAML delimiters
        if not content.startswith("---\n"):
            self.error(1, "YAML frontmatter must start with '---'")
            return

        # Find the closing delimiter
        lines = content.split("\n")
        closing_idx = None
        for idx, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                closing_idx = idx
                break

        if closing_idx is None:
            self.error(None, "YAML frontmatter closing '---' not found")
            return

        # Extract YAML content
        yaml_content = "\n".join(lines[1:closing_idx])

        # Parse YAML
        try:
            data = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            self.error(None, f"Invalid YAML syntax: {e}")
            return

        if not isinstance(data, dict):
            self.error(None, "YAML frontmatter must be a dictionary")
            return

        self.frontmatter = data

        # Check required fields
        if "name" not in data or not data["name"]:
            self.error(None, "YAML frontmatter: missing required field 'name'")

        if "description" not in data or not data["description"]:
            self.error(None, "YAML frontmatter: missing required field 'description'")

        # Check optional fields
        if "homepage" in data and data["homepage"]:
            url = data["homepage"]
            if not re.match(r'^https?://', url):
                self.warn(None, f"YAML frontmatter: 'homepage' should be a valid URL: {url}")

        if "metadata" in data and data["metadata"]:
            try:
                json.dumps(data["metadata"])
            except (TypeError, ValueError) as e:
                self.error(None, f"YAML frontmatter: 'metadata' is not valid JSON: {e}")

    def _validate_skill_metadata_rules(self):
        """Validate repo-specific metadata conventions."""
        name = self.frontmatter.get("name")
        description = self.frontmatter.get("description")

        if not isinstance(name, str) or not isinstance(description, str):
            return

        if not name.startswith("und-"):
            return

        if self.skill_path.name != name:
            self.error(
                None,
                f"und-* skill folder name must match frontmatter name: {self.skill_path.name} != {name}",
            )

        normalized = description.strip().lower()
        if not (
            normalized.startswith("trigger when:")
            or normalized.startswith("use when:")
        ):
            self.error(
                None,
                "und-* skill description must start with trigger wording such as 'TRIGGER when:' or 'Use when:'",
            )

        if "do not trigger when:" not in normalized:
            self.error(
                None,
                "und-* skill description must include 'DO NOT TRIGGER when:'",
            )

    def _validate_markdown_structure(self, content: str):
        """Validate Markdown structure."""
        lines = content.split("\n")

        # Check for unclosed code blocks
        in_code_block = False
        code_block_start = None

        for idx, line in enumerate(lines, start=1):
            if line.strip().startswith("```"):
                if in_code_block:
                    in_code_block = False
                    code_block_start = None
                else:
                    in_code_block = True
                    code_block_start = idx

        if in_code_block and code_block_start:
            self.error(code_block_start, "Code block not closed (missing ```)")

        # Check heading levels
        prev_level = 0
        for idx, line in enumerate(lines, start=1):
            if line.startswith("#"):
                match = re.match(r'^(#+)\s', line)
                if match:
                    level = len(match.group(1))
                    if prev_level > 0 and level > prev_level + 1:
                        self.warn(idx, f"Heading level jump (h{prev_level} -> h{level})")
                    prev_level = level

        # Check for isolated backticks (potential rendering errors)
        for idx, line in enumerate(lines, start=1):
            # Skip lines that are part of code blocks
            if line.strip().startswith("```"):
                continue

            # Count backticks
            backticks = line.count("`")
            if backticks % 2 != 0:
                self.warn(idx, "Odd number of backticks (may cause rendering issues)")

    def _validate_code_blocks(self, content: str):
        """Validate code block content."""
        # Extract code blocks with language tags
        code_block_pattern = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)

        for match in code_block_pattern.finditer(content):
            self.stats["code_blocks"] += 1
            lang = match.group(1).lower()
            code = match.group(2)

            # Find line number
            line_num = content[:match.start()].count("\n") + 1

            # Validate based on language
            if lang == "json":
                try:
                    json.loads(code)
                except json.JSONDecodeError as e:
                    self.error(line_num, f"Invalid JSON in code block: {e}")

            elif lang in ["bash", "sh", "shell"]:
                # Basic bash syntax checks
                self._validate_bash_syntax(code, line_num)

    def _validate_bash_syntax(self, code: str, start_line: int):
        """Basic bash syntax validation."""
        lines = code.split("\n")

        for idx, line in enumerate(lines, start=start_line):
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Check for unclosed quotes
            single_quotes = line.count("'") - line.count("\\'")
            double_quotes = line.count('"') - line.count('\\"')

            if single_quotes % 2 != 0:
                self.warn(idx, "Unclosed single quote in bash code")
            if double_quotes % 2 != 0:
                self.warn(idx, "Unclosed double quote in bash code")

            # Check curl commands for URL format
            if line.startswith("curl "):
                if not re.search(r'https?://', line):
                    self.warn(idx, "curl command without valid URL")

    def _validate_links(self, content: str):
        """Validate Markdown links."""
        # Extract links [text](url)
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')

        for match in link_pattern.finditer(content):
            self.stats["links"] += 1
            text = match.group(1)
            url = match.group(2)

            # Find line number
            line_num = content[:match.start()].count("\n") + 1

            # Check internal links (relative paths)
            if not url.startswith(("http://", "https://", "#")):
                target_path = self.skill_path / url
                if not target_path.exists():
                    self.warn(line_num, f"Internal link target not found: {url}")

            # Check external link format
            elif url.startswith(("http://", "https://")):
                if " " in url:
                    self.error(line_num, f"Invalid URL format (contains spaces): {url}")

    def _validate_skill_contracts(self, content: str):
        """Validate required contract tokens for selected skills."""
        required_tokens = SKILL_CONTRACT_RULES.get(self.skill_path.name)
        if not required_tokens:
            return

        for token in required_tokens:
            if token not in content:
                self.error(
                    None,
                    f"Skill contract missing required section/text: {token}"
                )

    def report(self) -> str:
        """Generate validation report."""
        if len(self.errors) == 0 and len(self.warnings) == 0:
            lines = [
                f"✅ SKILL.md validated successfully",
                "",
                "Checks performed:",
                f"  ✓ YAML frontmatter valid",
                f"  ✓ Required fields present (name, description)",
                f"  ✓ {self.stats['code_blocks']} code blocks validated",
                f"  ✓ Markdown structure valid",
                f"  ✓ {self.stats['links']} links checked",
            ]
            return "\n".join(lines)

        lines = [f"❌ Validation failed with {len(self.errors)} errors"]
        if len(self.warnings) > 0:
            lines[0] += f" and {len(self.warnings)} warnings"
        lines.append("")

        for err in self.errors:
            lines.append(str(err))

        for warn in self.warnings:
            lines.append(str(warn))

        return "\n".join(lines)


def collect_skills_to_validate(
    config: ValidatorConfig,
    skill: Optional[str] = None,
    validate_all: bool = False,
    path: Optional[str] = None
) -> List[Path]:
    """
    Collect skill paths to validate based on arguments.

    Args:
        config: ValidatorConfig instance
        skill: Specific skill name
        validate_all: Validate all skills flag
        path: Direct path to skill

    Returns:
        List of skill paths to validate

    Raises:
        ValueError: If arguments are invalid or paths don't exist
    """
    skills_to_validate = []

    if validate_all:
        # Validate all skills
        if not config.skills_dir.exists():
            raise ValueError(f"Skills directory not found: {config.skills_dir}")

        for skill_path in sorted(config.skills_dir.iterdir()):
            if skill_path.is_dir() and not skill_path.name.startswith("."):
                skills_to_validate.append(skill_path)

    elif skill:
        # Validate specific skill by name
        skill_path = config.skills_dir / skill
        if not skill_path.exists():
            raise ValueError(f"Skill not found: {skill_path}")
        skills_to_validate.append(skill_path)

    elif path:
        # Validate using direct path
        skill_path = Path(path)
        if not skill_path.is_dir():
            raise ValueError(f"Not a directory: {skill_path}")
        skills_to_validate.append(skill_path)

    else:
        raise ValueError("Must specify --skill <name>, --all, or provide a path")

    return skills_to_validate


@click.command()
@click.option("--skill", help="Skill name to validate (relative to skills/)")
@click.option("--all", "validate_all", is_flag=True, help="Validate all skills")
@click.argument("path", required=False, type=click.Path(exists=True))
def main(skill: Optional[str], validate_all: bool, path: Optional[str]):
    """
    Validate SKILL.md files for format and syntax errors.

    Examples:

        # Validate a specific skill by name
        tools/quick_validate.py --skill AIWay

        # Validate all skills
        tools/quick_validate.py --all

        # Validate using direct path
        tools/quick_validate.py /path/to/skill/folder
    """
    # Initialize config (uses default repo root detection)
    config = ValidatorConfig()

    # Collect skills to validate
    try:
        skills_to_validate = collect_skills_to_validate(config, skill, validate_all, path)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("\nUsage examples:", err=True)
        click.echo("  tools/quick_validate.py --skill AIWay", err=True)
        click.echo("  tools/quick_validate.py --all", err=True)
        click.echo("  tools/quick_validate.py /path/to/skill", err=True)
        sys.exit(1)

    # Validate each skill
    all_passed = True

    for skill_path in skills_to_validate:
        if len(skills_to_validate) > 1:
            click.echo(f"\n{'='*60}")
            click.echo(f"Validating: {skill_path.name}")
            click.echo(f"{'='*60}")

        validator = SkillValidator(skill_path)
        passed = validator.validate()

        click.echo(validator.report())

        if not passed:
            all_passed = False

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
