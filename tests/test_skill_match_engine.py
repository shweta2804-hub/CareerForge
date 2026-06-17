"""Tests for skill match engine."""

import pytest
from app.services.skill_match_engine import SkillMatchEngine


@pytest.fixture
def skill_match_engine():
    """Create skill match engine instance."""
    return SkillMatchEngine()


def test_calculate_skill_match_perfect_match(skill_match_engine: SkillMatchEngine):
    """Test skill match with perfect match."""
    student_skills = ["Python", "SQL", "Docker", "Git"]
    required_skills = ["Python", "SQL", "Docker"]
    
    result = skill_match_engine.calculate_skill_match(student_skills, required_skills)
    
    assert result["match_percentage"] == 100.0
    assert len(result["matched_skills"]) == 3
    assert len(result["missing_skills"]) == 0
    assert result["total_required"] == 3
    assert result["total_matched"] == 3


def test_calculate_skill_match_partial_match(skill_match_engine: SkillMatchEngine):
    """Test skill match with partial match."""
    student_skills = ["Python", "SQL", "Git"]
    required_skills = ["Python", "SQL", "Docker", "Git"]
    
    result = skill_match_engine.calculate_skill_match(student_skills, required_skills)
    
    assert result["match_percentage"] == 75.0
    assert len(result["matched_skills"]) == 3
    assert len(result["missing_skills"]) == 1
    assert "docker" in result["missing_skills"]


def test_calculate_skill_match_no_match(skill_match_engine: SkillMatchEngine):
    """Test skill match with no match."""
    student_skills = ["Python", "SQL"]
    required_skills = ["Java", "AWS", "Docker"]
    
    result = skill_match_engine.calculate_skill_match(student_skills, required_skills)
    
    assert result["match_percentage"] == 0.0
    assert len(result["matched_skills"]) == 0
    assert len(result["missing_skills"]) == 3


def test_calculate_skill_match_empty_required(skill_match_engine: SkillMatchEngine):
    """Test skill match with no required skills."""
    student_skills = ["Python", "SQL"]
    required_skills = []
    
    result = skill_match_engine.calculate_skill_match(student_skills, required_skills)
    
    assert result["match_percentage"] == 100.0
    assert len(result["matched_skills"]) == 0
    assert len(result["missing_skills"]) == 0


def test_calculate_skill_match_case_insensitive(skill_match_engine: SkillMatchEngine):
    """Test skill match is case insensitive."""
    student_skills = ["Python", "SQL", "DOCKER"]
    required_skills = ["python", "sql", "docker"]
    
    result = skill_match_engine.calculate_skill_match(student_skills, required_skills)
    
    assert result["match_percentage"] == 100.0
    assert len(result["matched_skills"]) == 3


def test_get_readiness_category_beginner(skill_match_engine: SkillMatchEngine):
    """Test readiness category for beginner."""
    category = skill_match_engine.get_readiness_category(25.0)
    assert category == "Beginner"


def test_get_readiness_category_developing(skill_match_engine: SkillMatchEngine):
    """Test readiness category for developing."""
    category = skill_match_engine.get_readiness_category(50.0)
    assert category == "Developing"


def test_get_readiness_category_placement_ready(skill_match_engine: SkillMatchEngine):
    """Test readiness category for placement ready."""
    category = skill_match_engine.get_readiness_category(70.0)
    assert category == "Placement Ready"


def test_get_readiness_category_highly_competitive(skill_match_engine: SkillMatchEngine):
    """Test readiness category for highly competitive."""
    category = skill_match_engine.get_readiness_category(90.0)
    assert category == "Highly Competitive"