"""
Opt-in integration tests for Codex skill triggering behavior.
"""

import os
import shutil
from pathlib import Path

import pytest

from run_codex_fixture import load_fixture, run_fixture


REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "skill-triggering"


def behavior_tests_enabled() -> bool:
    """Return True when Codex behavior tests are explicitly enabled for opt-in runs."""
    return os.getenv("CODEX_BEHAVIOR_TESTS") == "1" and shutil.which("codex") is not None


pytestmark = pytest.mark.skipif(
    not behavior_tests_enabled(),
    reason="Set CODEX_BEHAVIOR_TESTS=1 and ensure `codex` is installed to run behavior tests.",
)


def assert_expected_tokens(joined: str, expected_tokens):
    """Assert tokens or token groups are present in the agent output."""
    for token in expected_tokens:
        if isinstance(token, list):
            assert any(option.lower() in joined for option in token)
            continue
        assert token.lower() in joined


@pytest.mark.parametrize("fixture_path", sorted(FIXTURE_DIR.glob("*.json")))
def test_codex_skill_triggering_fixture(fixture_path: Path):
    """Each single-turn fixture should contain the expected skill markers promised by its prompt contract."""
    fixture = load_fixture(fixture_path)
    result = run_fixture(fixture_path, repo_root=REPO_ROOT)

    assert len(result["turns"]) == len(fixture["turns"])

    for turn_result, turn_fixture in zip(result["turns"], fixture["turns"]):
        joined = "\n".join(turn_result["agent_messages"]).lower()
        assert turn_result["exit_code"] == 0
        assert_expected_tokens(joined, turn_fixture.get("all_of", []))
