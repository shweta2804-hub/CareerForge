"""Tests for eligibility engine."""

import pytest
from app.services.eligibility_engine import EligibilityEngine


@pytest.fixture
def eligibility_engine():
    """Create eligibility engine instance."""
    return EligibilityEngine()


def test_check_eligibility_eligible(eligibility_engine: EligibilityEngine):
    """Test eligibility check for eligible student."""
    student = {
        "cgpa": 8.5,
        "skills": ["Python", "SQL", "Docker", "Git"]
    }
    company = {
        "minimum_cgpa": 7.5,
        "required_skills": ["Python", "SQL", "Docker"]
    }
    
    is_eligible, reason = eligibility_engine.check_eligibility(student, company)
    
    assert is_eligible is True
    assert reason == "Eligible"


def test_check_eligibility_low_cgpa(eligibility_engine: EligibilityEngine):
    """Test eligibility check with low CGPA."""
    student = {
        "cgpa": 7.0,
        "skills": ["Python", "SQL", "Docker"]
    }
    company = {
        "minimum_cgpa": 8.0,
        "required_skills": ["Python", "SQL"]
    }
    
    is_eligible, reason = eligibility_engine.check_eligibility(student, company)
    
    assert is_eligible is False
    assert "CGPA" in reason


def test_check_eligibility_missing_skills(eligibility_engine: EligibilityEngine):
    """Test eligibility check with missing skills."""
    student = {
        "cgpa": 8.5,
        "skills": ["Python", "SQL"]
    }
    company = {
        "minimum_cgpa": 7.5,
        "required_skills": ["Python", "SQL", "Docker", "Git"]
    }
    
    is_eligible, reason = eligibility_engine.check_eligibility(student, company)
    
    assert is_eligible is False
    assert "Missing required skills" in reason


def test_check_eligibility_multiple_issues(eligibility_engine: EligibilityEngine):
    """Test eligibility check with multiple issues."""
    student = {
        "cgpa": 7.0,
        "skills": ["Python"]
    }
    company = {
        "minimum_cgpa": 8.0,
        "required_skills": ["Python", "SQL", "Docker"]
    }
    
    is_eligible, reason = eligibility_engine.check_eligibility(student, company)
    
    assert is_eligible is False
    assert "CGPA" in reason
    assert "Missing required skills" in reason


def test_get_eligibility_details(eligibility_engine: EligibilityEngine):
    """Test getting detailed eligibility information."""
    student = {
        "cgpa": 8.5,
        "skills": ["Python", "SQL", "Docker", "Git"]
    }
    company = {
        "minimum_cgpa": 7.5,
        "required_skills": ["Python", "SQL", "Docker", "React"]
    }
    
    details = eligibility_engine.get_eligibility_details(student, company)
    
    assert details["is_eligible"] is False
    assert details["cgpa_match"] is True
    assert len(details["matched_skills"]) == 3
    assert len(details["missing_skills"]) == 1
    assert details["skill_match_percentage"] == 75.0