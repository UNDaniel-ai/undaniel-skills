"""
Comprehensive tests for quick_validate.py

Test coverage:
- ValidatorConfig class
- ValidationError class
- SkillValidator YAML validation
- SkillValidator Markdown structure validation
- SkillValidator code block validation
- SkillValidator link validation
- collect_skills_to_validate function
- CLI integration
"""

import pytest
from pathlib import Path
from click.testing import CliRunner

# Import the modules under test
import quick_validate
from quick_validate import (
    ValidatorConfig,
    ValidationError,
    SkillValidator,
    collect_skills_to_validate,
    main,
)


# ==============================================================================
# ValidatorConfig Tests
# ==============================================================================

class TestValidatorConfig:
    """Tests for ValidatorConfig class."""

    def test_default_config_detects_repo_root(self):
        """Test ValidatorConfig with no arguments detects repo root."""
        config = ValidatorConfig()
        assert config.repo_root.exists()
        assert config.skills_dir == config.repo_root / "skills"

    def test_custom_repo_root(self, tmp_repo_root):
        """Test ValidatorConfig with custom repo root."""
        config = ValidatorConfig(repo_root=tmp_repo_root)
        assert config.repo_root == tmp_repo_root
        assert config.skills_dir == tmp_repo_root / "skills"

    def test_repo_root_as_string(self, tmp_repo_root):
        """Test ValidatorConfig accepts repo_root as string."""
        config = ValidatorConfig(repo_root=str(tmp_repo_root))
        assert config.repo_root == Path(tmp_repo_root)


# ==============================================================================
# ValidationError Tests
# ==============================================================================

class TestValidationError:
    """Tests for ValidationError class."""

    def test_error_with_line_number(self):
        """Test ValidationError formatting with line number."""
        err = ValidationError("ERROR", 42, "Test error message")
        assert str(err) == "  [ERROR] Line 42: Test error message"

    def test_error_without_line_number(self):
        """Test ValidationError formatting without line number."""
        err = ValidationError("WARN", None, "Test warning")
        assert str(err) == "  [WARN] Test warning"

    def test_error_attributes(self):
        """Test ValidationError attributes."""
        err = ValidationError("ERROR", 10, "Message")
        assert err.level == "ERROR"
        assert err.line == 10
        assert err.message == "Message"


# ==============================================================================
# SkillValidator - YAML Validation Tests
# ==============================================================================

class TestSkillValidatorYAML:
    """Tests for YAML frontmatter validation."""

    def test_valid_yaml(self, tmp_skills_dir, sample_skill_content):
        """Test validation passes for valid YAML."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(sample_skill_content["valid"])

        validator = SkillValidator(skill_dir)
        result = validator.validate()

        assert result is True
        assert len(validator.errors) == 0

    def test_missing_yaml_start_delimiter(self, tmp_skills_dir):
        """Test error when YAML doesn't start with ---."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = "name: test\ndescription: test\n---\n# Content"
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.errors) > 0
        assert any("must start with '---'" in str(e) for e in validator.errors)

    def test_missing_yaml_end_delimiter(self, tmp_skills_dir):
        """Test error when YAML closing --- is missing."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = "---\nname: test\ndescription: test\n# Content"
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.errors) > 0
        assert any("closing '---' not found" in str(e) for e in validator.errors)

    def test_invalid_yaml_syntax(self, tmp_skills_dir):
        """Test error for invalid YAML syntax."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = "---\nname: test\ndescription: [invalid yaml\n---\n# Content"
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.errors) > 0
        assert any("Invalid YAML syntax" in str(e) for e in validator.errors)

    def test_missing_required_field_name(self, tmp_skills_dir, sample_skill_content):
        """Test error when 'name' field is missing."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(sample_skill_content["missing_name"])

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.errors) > 0
        assert any("missing required field 'name'" in str(e) for e in validator.errors)

    def test_missing_required_field_description(self, tmp_skills_dir, sample_skill_content):
        """Test error when 'description' field is missing."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(sample_skill_content["missing_description"])

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.errors) > 0
        assert any("missing required field 'description'" in str(e) for e in validator.errors)

    def test_invalid_homepage_url(self, tmp_skills_dir):
        """Test warning for invalid homepage URL."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
homepage: not-a-url
---
# Content
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.warnings) > 0
        assert any("should be a valid URL" in str(w) for w in validator.warnings)

    def test_valid_homepage_url(self, tmp_skills_dir):
        """Test valid homepage URL doesn't trigger warning."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
homepage: https://example.com
---
# Content
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        # Should not have homepage-related warnings
        assert not any("homepage" in str(w) for w in validator.warnings)


# ==============================================================================
# SkillValidator - Markdown Structure Tests
# ==============================================================================

class TestSkillValidatorMarkdown:
    """Tests for Markdown structure validation."""

    def test_unclosed_code_block(self, tmp_skills_dir, sample_skill_content):
        """Test error for unclosed code block."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(sample_skill_content["unclosed_code_block"])

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.errors) > 0
        assert any("Code block not closed" in str(e) for e in validator.errors)

    def test_properly_closed_code_blocks(self, tmp_skills_dir):
        """Test multiple properly closed code blocks pass validation."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

```bash
echo "first"
```

```python
print("second")
```
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert validator.stats["code_blocks"] == 2
        assert not any("Code block not closed" in str(e) for e in validator.errors)

    def test_heading_level_jump(self, tmp_skills_dir, sample_skill_content):
        """Test warning for heading level jump."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(sample_skill_content["heading_jump"])

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.warnings) > 0
        assert any("Heading level jump" in str(w) for w in validator.warnings)

    def test_proper_heading_hierarchy(self, tmp_skills_dir):
        """Test proper heading hierarchy doesn't trigger warning."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

# H1

## H2

### H3

## Another H2
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert not any("Heading level jump" in str(w) for w in validator.warnings)

    def test_odd_backticks(self, tmp_skills_dir):
        """Test warning for odd number of backticks."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

# Test

This line has an `odd number of backticks
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.warnings) > 0
        assert any("Odd number of backticks" in str(w) for w in validator.warnings)

    def test_even_backticks(self, tmp_skills_dir):
        """Test even number of backticks doesn't warn."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

# Test

This line has `even` backticks `properly` closed
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert not any("Odd number of backticks" in str(w) for w in validator.warnings)


# ==============================================================================
# SkillValidator - Code Block Content Tests
# ==============================================================================

class TestSkillValidatorCodeBlocks:
    """Tests for code block content validation."""

    def test_valid_json_code_block(self, tmp_skills_dir):
        """Test valid JSON code block passes."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

```json
{
  "key": "value",
  "number": 123
}
```
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert validator.stats["code_blocks"] == 1
        assert not any("Invalid JSON" in str(e) for e in validator.errors)

    def test_invalid_json_code_block(self, tmp_skills_dir, sample_skill_content):
        """Test invalid JSON code block triggers error."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(sample_skill_content["invalid_json"])

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.errors) > 0
        assert any("Invalid JSON" in str(e) for e in validator.errors)

    def test_bash_unclosed_double_quote(self, tmp_skills_dir):
        """Test bash code with unclosed double quote."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

```bash
echo "unclosed
```
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.warnings) > 0
        assert any("Unclosed double quote" in str(w) for w in validator.warnings)

    def test_bash_unclosed_single_quote(self, tmp_skills_dir):
        """Test bash code with unclosed single quote."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

```bash
echo 'unclosed
```
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.warnings) > 0
        assert any("Unclosed single quote" in str(w) for w in validator.warnings)

    def test_bash_properly_quoted(self, tmp_skills_dir):
        """Test properly quoted bash code passes."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

```bash
echo "properly closed"
echo 'also closed'
```
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert not any("Unclosed" in str(w) for w in validator.warnings)

    def test_curl_without_url(self, tmp_skills_dir):
        """Test curl command without URL triggers warning."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

```bash
curl -X POST
```
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.warnings) > 0
        assert any("curl command without valid URL" in str(w) for w in validator.warnings)

    def test_curl_with_url(self, tmp_skills_dir):
        """Test curl command with URL passes."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

```bash
curl -X POST https://api.example.com/endpoint
```
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert not any("curl command without" in str(w) for w in validator.warnings)

    def test_multiple_code_blocks_different_languages(self, tmp_skills_dir):
        """Test validation of multiple code blocks with different languages."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

```bash
echo "bash"
```

```python
print("python")
```

```json
{"key": "value"}
```
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert validator.stats["code_blocks"] == 3
        assert len(validator.errors) == 0


# ==============================================================================
# SkillValidator - Link Validation Tests
# ==============================================================================

class TestSkillValidatorLinks:
    """Tests for link validation."""

    def test_valid_external_link(self, tmp_skills_dir):
        """Test valid external link passes."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

[External Link](https://example.com)
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert validator.stats["links"] == 1
        assert len(validator.errors) == 0

    def test_external_link_with_spaces(self, tmp_skills_dir):
        """Test external link with spaces triggers error."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

[Bad Link](https://example .com/broken url)
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.errors) > 0
        assert any("contains spaces" in str(e) for e in validator.errors)

    def test_broken_internal_link(self, tmp_skills_dir, sample_skill_content):
        """Test broken internal link triggers warning."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(sample_skill_content["broken_link"])

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert len(validator.warnings) > 0
        assert any("Internal link target not found" in str(w) for w in validator.warnings)

    def test_valid_internal_link(self, tmp_skills_dir):
        """Test valid internal link passes."""
        # Create target skill
        target_skill = tmp_skills_dir / "target-skill"
        target_skill.mkdir()
        (target_skill / "SKILL.md").write_text("# Target")

        # Create linking skill
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

[Target Skill](../target-skill/SKILL.md)
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert not any("Internal link target not found" in str(w) for w in validator.warnings)

    def test_anchor_link(self, tmp_skills_dir):
        """Test anchor links (#section) are not validated as files."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        content = """---
name: test-skill
description: Test
---

[Jump to Section](#section)

## Section
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        # Anchor links shouldn't trigger warnings
        assert not any("Internal link target not found" in str(w) for w in validator.warnings)


# ==============================================================================
# SkillValidator - Skill Contract Validation Tests
# ==============================================================================

class TestSkillValidatorContracts:
    """Tests for skill-specific contract validation."""

    @pytest.mark.parametrize("skill_name", [
        "complex-task-solver",
        "workspace-structure-manager",
        "skills-manager",
        "und-brainstorming",
        "und-test-driven-development",
        "und-systematic-debugging",
        "und-verification-before-completion",
        "und-workflow-entry",
        "und-writing-plans",
        "und-writing-skills",
    ])
    def test_missing_required_contract_tokens_triggers_error(self, tmp_skills_dir, skill_name):
        """Target governance skills must include required contract tokens."""
        skill_dir = tmp_skills_dir / skill_name
        skill_dir.mkdir()
        content = f"""---
name: {skill_name}
description: Test
---
# Test
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert any(
            "Skill contract missing required section/text" in str(e)
            for e in validator.errors
        )

    @pytest.mark.parametrize("skill_name,content", [
        (
            "complex-task-solver",
            """---
name: complex-task-solver
description: Test
---
## 首轮技能识别协议（防漏触发）
命中的 skill 列表
使用顺序
跳过理由
复杂度预检清单（强制）
阶段门禁协议（Route B / Route C 强制）
显式确认信号协议（双重确定）
带目标阶段名的明确确认语句
不构成阶段确认
未完成 `requirements-alignment.md` 且未获得确认，不得创建 `design.md`。
未完成 `implementation-plan.md` 且未获得确认，不得开始代码编写。
und-brainstorming
und-writing-plans
方法型 skill 调度规则
session-summary.md
""",
        ),
        (
            "workspace-structure-manager",
            """---
name: workspace-structure-manager
description: Test
---
## 触发前置检查（防漏触发）
前置检查清单（强制）
session 策略
用户是否指定路径但任务本质仍是开发任务
## Workspace AGENTS.md Bootstrap
tools/init_workspace.py
## Session 门禁策略（强制）
门禁确认记录（强制）
AI 发起确认消息
用户确认原话
当前阶段
是否允许编码
session-summary.md
""",
        ),
        (
            "skills-manager",
            """---
name: skills-manager
description: Test
---
## Skill 识别失败修复流程
机制问题
执行漏触发
tools/skillctl validate --skill <skill-name>
und-writing-skills
automatic trigger
explicit request
multi-turn
fresh verification evidence
Mechanism Completeness Check
tools/init_workspace.py
tests/test_init_workspace.py
tools/quick_validate.py
Knowledge Drift Check
knowledge/*.md
""",
        ),
        (
            "und-brainstorming",
            """---
name: und-brainstorming
description: |
  TRIGGER when:
    - Route C brainstorming is needed

  DO NOT TRIGGER when:
    - Atomic edit
---
requirements gap scan
option comparison
design challenge
complex-task-solver
workspace-structure-manager
automatic trigger
explicit request
multi-turn
""",
        ),
        (
            "und-workflow-entry",
            """---
name: und-workflow-entry
description: |
  TRIGGER when:
    - Start a workflow

  DO NOT TRIGGER when:
    - Atomic edit
---
use / skip / why / order
session strategy
complex-task-solver
workspace-structure-manager
skills-manager
und-writing-skills
Before the assessment is complete, do not start design, implementation planning, coding, validation, or completion claims.
""",
        ),
        (
            "und-writing-plans",
            """---
name: und-writing-plans
description: |
  TRIGGER when:
    - Implementation planning is needed

  DO NOT TRIGGER when:
    - Coding already started
---
前置输入
验证命令
预期结果
Step Acceptance
postcondition
complex-task-solver
workspace-structure-manager
automatic trigger
multi-turn
""",
        ),
        (
            "und-writing-skills",
            """---
name: und-writing-skills
description: |
  TRIGGER when:
    - Create a skill

  DO NOT TRIGGER when:
    - Product-only code
---
description 只写触发条件
automatic trigger
explicit request
multi-turn
semantic assertions
equivalent wording
tools/run_codex_fixture.py
tests/test_init_workspace.py
tools/skillctl validate --skill <skill-name>
Integration Surface Checklist
templates/workspace/AGENTS.md.template
tools/init_workspace.py
tools/quick_validate.py
dispatch / gate
knowledge/*.md
""",
        ),
        (
            "und-test-driven-development",
            """---
name: und-test-driven-development
description: |
  TRIGGER when:
    - TDD execution is needed

  DO NOT TRIGGER when:
    - Design work only
---
Verify RED
Verify GREEN
TDD 例外
mock
test-only methods
incomplete mocks
complex-task-solver
workspace-structure-manager
automatic trigger
multi-turn
""",
        ),
        (
            "und-subagent-driven-development",
            """---
name: und-subagent-driven-development
description: |
  TRIGGER when:
    - Subagent execution must be evaluated

  DO NOT TRIGGER when:
    - Planning only
---
Capability Detection
tooling_supported
workspace_supported
review_supported
Task Eligibility
Status Model
DONE_WITH_CONCERNS
NEEDS_CONTEXT
BLOCKED
Spec Compliance Review
Code Quality Review
Fallback Protocol
complex-task-solver
workspace-structure-manager
automatic trigger
explicit request
multi-turn
""",
        ),
        (
            "und-systematic-debugging",
            """---
name: und-systematic-debugging
description: |
  TRIGGER when:
    - Debugging is needed

  DO NOT TRIGGER when:
    - Planning only
---
Root Cause Investigation
Pattern Analysis
Hypothesis And Testing
condition-based waiting
defense-in-depth
complex-task-solver
workspace-structure-manager
automatic trigger
explicit request
multi-turn
""",
        ),
        (
            "und-verification-before-completion",
            """---
name: und-verification-before-completion
description: |
  TRIGGER when:
    - Verification is needed before completion

  DO NOT TRIGGER when:
    - Active implementation only
---
claim -> command -> output -> evidence
fresh verification evidence
partial verification
agent success report
complex-task-solver
workspace-structure-manager
automatic trigger
explicit request
multi-turn
""",
        ),
    ])
    def test_required_contract_tokens_pass_validation(self, tmp_skills_dir, skill_name, content):
        """Validation should pass contract check when required tokens exist."""
        skill_dir = tmp_skills_dir / skill_name
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert not any(
            "Skill contract missing required section/text" in str(e)
            for e in validator.errors
        )


class TestPhase4KnowledgeContracts:
    """Regression checks for Phase 4 planning and progress contracts."""

    REPO_ROOT = Path(__file__).resolve().parent.parent

    def test_phase4_plan_contract_fields_exist(self):
        """Implementation-plan knowledge should require Phase 4 execution-mode fields."""
        content = (
            self.REPO_ROOT
            / "skills"
            / "complex-task-solver"
            / "knowledge"
            / "12-implementation-plan.md"
        ).read_text(encoding="utf-8")

        for token in ["执行模式", "Subagent Eligibility", "Review Contract"]:
            assert token in content

    def test_phase4_progress_tracking_mentions_subagent_facts(self):
        """Progress-tracking knowledge should record subagent dispatch and fallback evidence."""
        content = (
            self.REPO_ROOT
            / "skills"
            / "complex-task-solver"
            / "knowledge"
            / "13-progress-tracking.md"
        ).read_text(encoding="utf-8")

        for token in ["当前执行模式", "subagent dispatch", "fallback"]:
            assert token in content

    def test_phase4_workspace_templates_include_subagent_sections(self):
        """Workspace templates should expose subagent execution and review sections."""
        content = (
            self.REPO_ROOT
            / "skills"
            / "workspace-structure-manager"
            / "knowledge"
            / "4-document-templates.md"
        ).read_text(encoding="utf-8")

        for token in [
            "执行模式",
            "Subagent Eligibility",
            "Review Contract",
            "Subagent Dispatch Log",
            "Review Loop",
            "Fallback Record",
        ]:
            assert token in content


class TestSkillValidatorUndMetadata:
    """Tests for und-* metadata conventions."""

    def test_valid_und_description_passes(self, tmp_skills_dir):
        """und-* skills should accept trigger-first descriptions."""
        skill_dir = tmp_skills_dir / "und-sample"
        skill_dir.mkdir()
        content = """---
name: und-sample
description: |
  TRIGGER when:
    - Start a workflow task

  DO NOT TRIGGER when:
    - Atomic edit
---
# Sample
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert not any("und-* skill description" in str(e) for e in validator.errors)

    def test_und_description_requires_trigger_prefix(self, tmp_skills_dir):
        """und-* descriptions must start with trigger wording."""
        skill_dir = tmp_skills_dir / "und-sample"
        skill_dir.mkdir()
        content = """---
name: und-sample
description: This skill coordinates workflow entry.
---
# Sample
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert any("must start with trigger wording" in str(e) for e in validator.errors)

    def test_und_description_requires_do_not_trigger(self, tmp_skills_dir):
        """und-* descriptions must include a do-not-trigger section."""
        skill_dir = tmp_skills_dir / "und-sample"
        skill_dir.mkdir()
        content = """---
name: und-sample
description: |
  TRIGGER when:
    - Start a workflow task
---
# Sample
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert any("DO NOT TRIGGER" in str(e) for e in validator.errors)

    def test_und_folder_name_must_match_frontmatter(self, tmp_skills_dir):
        """und-* skill folders should match the frontmatter name."""
        skill_dir = tmp_skills_dir / "und-folder"
        skill_dir.mkdir()
        content = """---
name: und-other
description: |
  TRIGGER when:
    - Start a workflow task

  DO NOT TRIGGER when:
    - Atomic edit
---
# Sample
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert any("folder name must match" in str(e) for e in validator.errors)

    def test_non_target_skill_skips_contract_check(self, tmp_skills_dir):
        """Skills outside the contract map should not fail contract checks."""
        skill_dir = tmp_skills_dir / "generic-skill"
        skill_dir.mkdir()
        content = """---
name: generic-skill
description: Test
---
# Generic
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        validator.validate()

        assert not any(
            "Skill contract missing required section/text" in str(e)
            for e in validator.errors
        )


# ==============================================================================
# SkillValidator - File I/O Tests
# ==============================================================================

class TestSkillValidatorFileIO:
    """Tests for file reading and error handling."""

    def test_missing_skill_md_file(self, tmp_skills_dir):
        """Test error when SKILL.md doesn't exist."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        # Don't create SKILL.md

        validator = SkillValidator(skill_dir)
        result = validator.validate()

        assert result is False
        assert len(validator.errors) > 0
        assert any("SKILL.md not found" in str(e) for e in validator.errors)

    def test_content_injection_for_testing(self):
        """Test content can be injected for testing without file I/O."""
        content = """---
name: test
description: test
---
# Test
"""
        # Use a non-existent path, but provide content
        validator = SkillValidator(Path("/fake/path"), content=content)
        result = validator.validate()

        assert result is True
        assert len(validator.errors) == 0

    def test_report_with_no_errors(self, tmp_skills_dir, sample_skill_content):
        """Test report generation for successful validation."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(sample_skill_content["valid"])

        validator = SkillValidator(skill_dir)
        validator.validate()
        report = validator.report()

        assert "✅" in report
        assert "validated successfully" in report
        assert "code blocks validated" in report

    def test_report_with_errors(self, tmp_skills_dir, sample_skill_content):
        """Test report generation with errors."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(sample_skill_content["missing_name"])

        validator = SkillValidator(skill_dir)
        validator.validate()
        report = validator.report()

        assert "❌" in report
        assert "Validation failed" in report
        assert "ERROR" in report


# ==============================================================================
# collect_skills_to_validate Tests
# ==============================================================================

class TestCollectSkillsToValidate:
    """Tests for collect_skills_to_validate function."""

    def test_validate_all_skills(self, tmp_repo_root):
        """Test --all flag collects all skills."""
        skills_dir = tmp_repo_root / "skills"

        # Create multiple skills
        for name in ["skill1", "skill2", "skill3"]:
            skill_dir = skills_dir / name
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("# Test")

        config = ValidatorConfig(repo_root=tmp_repo_root)
        skills = collect_skills_to_validate(config, validate_all=True)

        assert len(skills) == 3
        assert all(s.is_dir() for s in skills)

    def test_validate_all_skips_hidden_dirs(self, tmp_repo_root):
        """Test --all flag skips directories starting with dot."""
        skills_dir = tmp_repo_root / "skills"

        # Create regular and hidden skills
        (skills_dir / "regular-skill").mkdir()
        (skills_dir / ".hidden-skill").mkdir()

        config = ValidatorConfig(repo_root=tmp_repo_root)
        skills = collect_skills_to_validate(config, validate_all=True)

        assert len(skills) == 1
        assert skills[0].name == "regular-skill"

    def test_validate_specific_skill(self, tmp_repo_root):
        """Test --skill flag validates specific skill."""
        skills_dir = tmp_repo_root / "skills"
        skill_dir = skills_dir / "test-skill"
        skill_dir.mkdir()

        config = ValidatorConfig(repo_root=tmp_repo_root)
        skills = collect_skills_to_validate(config, skill="test-skill")

        assert len(skills) == 1
        assert skills[0].name == "test-skill"

    def test_validate_skill_not_found(self, tmp_repo_root):
        """Test error when specified skill doesn't exist."""
        config = ValidatorConfig(repo_root=tmp_repo_root)

        with pytest.raises(ValueError, match="Skill not found"):
            collect_skills_to_validate(config, skill="nonexistent")

    def test_validate_by_path(self, tmp_skills_dir):
        """Test validation by direct path."""
        skill_dir = tmp_skills_dir / "test-skill"
        skill_dir.mkdir()

        config = ValidatorConfig()
        skills = collect_skills_to_validate(config, path=str(skill_dir))

        assert len(skills) == 1
        assert skills[0] == skill_dir

    def test_validate_path_not_directory(self, tmp_repo_root):
        """Test error when path is not a directory."""
        file_path = tmp_repo_root / "file.txt"
        file_path.write_text("test")

        config = ValidatorConfig()

        with pytest.raises(ValueError, match="Not a directory"):
            collect_skills_to_validate(config, path=str(file_path))

    def test_no_arguments_raises_error(self, tmp_repo_root):
        """Test error when no arguments provided."""
        config = ValidatorConfig(repo_root=tmp_repo_root)

        with pytest.raises(ValueError, match="Must specify"):
            collect_skills_to_validate(config)

    def test_skills_dir_not_found(self, tmp_repo_root):
        """Test error when skills directory doesn't exist."""
        # Remove skills directory
        (tmp_repo_root / "skills").rmdir()

        config = ValidatorConfig(repo_root=tmp_repo_root)

        with pytest.raises(ValueError, match="Skills directory not found"):
            collect_skills_to_validate(config, validate_all=True)


# ==============================================================================
# CLI Integration Tests
# ==============================================================================

class TestCLI:
    """Tests for CLI integration."""

    def test_cli_validate_specific_skill(self, tmp_repo_root, sample_skill_content):
        """Test CLI validation of specific skill."""
        skills_dir = tmp_repo_root / "skills"
        skill_dir = skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(sample_skill_content["valid"])

        # Use path argument to directly validate the skill
        runner = CliRunner()
        result = runner.invoke(main, [str(skill_dir)])

        assert result.exit_code == 0
        assert "✅" in result.output or "validated successfully" in result.output.lower()

    def test_cli_validate_all(self, tmp_repo_root):
        """Test CLI validation of all skills."""
        skills_dir = tmp_repo_root / "skills"

        # Create two valid skills
        for name in ["skill1", "skill2"]:
            skill_dir = skills_dir / name
            skill_dir.mkdir()
            content = """---
name: {name}
description: Test skill
---
# Test
""".format(name=name)
            (skill_dir / "SKILL.md").write_text(content)

        runner = CliRunner()
        # Use path argument to avoid detection issues
        result = runner.invoke(main, [str(skills_dir / "skill1")])

        assert result.exit_code == 0

    def test_cli_invalid_skill_fails(self, tmp_repo_root, sample_skill_content):
        """Test CLI exits with error for invalid skill."""
        skills_dir = tmp_repo_root / "skills"
        skill_dir = skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(sample_skill_content["missing_name"])

        runner = CliRunner()
        result = runner.invoke(main, [str(skill_dir)])

        assert result.exit_code == 1
        assert "❌" in result.output or "failed" in result.output.lower()

    def test_cli_no_arguments_shows_error(self):
        """Test CLI shows error when no arguments provided."""
        runner = CliRunner()
        result = runner.invoke(main, [])

        assert result.exit_code == 1
        assert "Error" in result.output
        assert "Usage examples" in result.output
