"""
Pytest configuration and shared fixtures.
"""

import sys
import tempfile
import shutil
from pathlib import Path
from typing import Generator

import pytest

# Add tools directory to Python path for imports
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))


@pytest.fixture
def tmp_skills_dir() -> Generator[Path, None, None]:
    """
    Create a temporary skills directory for testing.

    Yields:
        Path to temporary skills directory

    Cleanup:
        Automatically removed after test
    """
    tmp_dir = Path(tempfile.mkdtemp())
    skills_dir = tmp_dir / "skills"
    skills_dir.mkdir()

    yield skills_dir

    # Cleanup
    shutil.rmtree(tmp_dir)


@pytest.fixture
def tmp_logs_dir() -> Generator[Path, None, None]:
    """
    Create a temporary logs directory for testing.

    Yields:
        Path to temporary logs directory

    Cleanup:
        Automatically removed after test
    """
    tmp_dir = Path(tempfile.mkdtemp())

    yield tmp_dir

    # Cleanup
    shutil.rmtree(tmp_dir)


@pytest.fixture
def tmp_repo_root(tmp_skills_dir: Path) -> Path:
    """
    Create a temporary repository root with skills directory.

    Args:
        tmp_skills_dir: Temporary skills directory fixture

    Returns:
        Path to temporary repo root
    """
    return tmp_skills_dir.parent


@pytest.fixture
def sample_skill_content() -> dict:
    """
    Provide sample SKILL.md content variations for testing.

    Returns:
        Dict of content_name -> content_string
    """
    return {
        "valid": """---
name: test-skill
description: A valid test skill
homepage: https://example.com
metadata: {"version": "1.0"}
---

# Test Skill

This is a valid skill.

```bash
echo "Hello"
```

[Link](https://example.com)
""",
        "missing_name": """---
description: Missing name field
---

# Test
""",
        "missing_description": """---
name: test-skill
---

# Test
""",
        "unclosed_code_block": """---
name: test-skill
description: Unclosed code block
---

# Test

```bash
echo "This is unclosed"
""",
        "invalid_json": """---
name: test-skill
description: Invalid JSON in code block
---

# Test

```json
{
  "key": "value"
  "missing": "comma"
}
```
""",
        "heading_jump": """---
name: test-skill
description: Heading level jump
---

# H1

### H3 Without H2
""",
        "broken_link": """---
name: test-skill
description: Broken internal link
---

# Test

[Broken Link](../nonexistent/SKILL.md)
""",
    }
