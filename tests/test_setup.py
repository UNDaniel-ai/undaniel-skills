"""
Basic tests to verify test infrastructure is working.
"""

from pathlib import Path


def test_tmp_skills_dir(tmp_skills_dir):
    """Test tmp_skills_dir fixture creates a directory."""
    assert tmp_skills_dir.exists()
    assert tmp_skills_dir.is_dir()
    assert tmp_skills_dir.name == "skills"


def test_tmp_logs_dir(tmp_logs_dir):
    """Test tmp_logs_dir fixture creates a directory."""
    assert tmp_logs_dir.exists()
    assert tmp_logs_dir.is_dir()


def test_tmp_repo_root(tmp_repo_root, tmp_skills_dir):
    """Test tmp_repo_root fixture points to parent of skills_dir."""
    assert tmp_repo_root.exists()
    assert (tmp_repo_root / "skills").exists()
    assert (tmp_repo_root / "skills") == tmp_skills_dir


def test_sample_skill_content(sample_skill_content):
    """Test sample_skill_content fixture provides content."""
    assert "valid" in sample_skill_content
    assert "missing_name" in sample_skill_content
    assert "---" in sample_skill_content["valid"]
    assert "name:" in sample_skill_content["valid"]
