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
from typing import List, Tuple, Optional

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

        # Validate Markdown structure
        self._validate_markdown_structure(content)

        # Validate code blocks
        self._validate_code_blocks(content)

        # Validate links
        self._validate_links(content)

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
