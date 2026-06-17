"""Tests for readiness score service."""

import pytest
from app.services.readiness_score_service import ReadinessScoreService
from app.services.skill_match_engine import SkillMatchEngine


@pytest.fixture
def readiness_score_service():
    """Create readiness score service instance."""
    return ReadinessScoreService()


def test_calculate_readiness_score_high_performer(readiness_score_service: ReadinessScoreService):
    """Test readiness score for high-performing student."""
    score_result = readiness_score_service.calculate_readiness_score(
        cgpa=9.0,
        skills=["Python", "SQL", "Docker", "Git", "React", "FastAPI", "AWS"],
        projects=[
            {"name": "Project 1", "tech": ["Python", "React"]},
            {"name": "Project 2", "tech": ["FastAPI", "Docker"]},
            {"name": "Project 3", "tech": ["AWS", "Python"]},
        ],
        assessment_scores=[
            {"percentage": 85.0},
            {"percentage": 90.0},
        ]
    )
    
    assert "score" in score_result
    assert "category" in score_result
    assert "breakdown" in score_result
    assert 0 <= score_result["score"] <= 100
    assert score_result["category"] in ["Beginner", "Developing", "Placement Ready", "Highly Competitive"]


def test_calculate_readiness_score_beginner(readiness_score_service: ReadinessScoreService):
    """Test readiness score for beginner student."""
    score_result = readiness_score_service.calculate_readiness_score(
        cgpa=6.5,
        skills=["Python"],
        projects=[],
        assessment_scores=[]
    )
    
    assert score_result["score"] < 40
    assert score_result["category"] == "Beginner"


def test_calculate_readiness_score_no_assessments(readiness_score_service: ReadinessScoreService):
    """Test readiness score with no assessments."""
    score_result = readiness_score_service.calculate_readiness_score(
        cgpa=8.0,
        skills=["Python", "SQL", "Docker"],
        projects=[{"name": "Project 1", "tech": ["Python"]}],
        assessment_scores=[]
    )
    
    assert score_result["score"] > 0
    assert "assessment_score" in score_result["breakdown"]


def test_get_score_insights_beginner(readiness_score_service: ReadinessScoreService):
    """Test insights for beginner score."""
    insights = readiness_score_service.get_score_insights(25.0)
    
    assert insights["score"] == 25.0
    assert insights["category"] == "Beginner"
    assert "message" in insights
    assert "recommendations" in insights
    assert len(insights["recommendations"]) > 0


def test_get_score_insights_highly_competitive(readiness_score_service: ReadinessScoreService):
    """Test insights for highly competitive score."""
    insights = readiness_score_service.get_score_insights(95.0)
    
    assert insights["score"] == 95.0
    assert insights["category"] == "Highly Competitive"
    assert "message" in insights
    assert "recommendations" in insights
    assert len(insights["recommendations"]) > 0


def test_score_breakdown_components(readiness_score_service: ReadinessScoreService):
    """Test that all score components are present."""
    score_result = readiness_score_service.calculate_readiness_score(
        cgpa=8.0,
        skills=["Python", "SQL"],
        projects=[{"name": "P1", "tech": ["Python"]}],
        assessment_scores=[{"percentage": 75.0}]
    )
    
    breakdown = score_result["breakdown"]
    assert "cgpa_score" in breakdown
    assert "skills_score" in breakdown
    assert "projects_score" in breakdown
    assert "assessment_score" in breakdown
    
    # Verify scores are within expected ranges
    assert 0 <= breakdown["cgpa_score"] <= 30
    assert 0 <= breakdown["skills_score"] <= 30
    assert 0 <= breakdown["projects_score"] <= 20
    assert 0 <= breakdown["assessment_score"] <= 20