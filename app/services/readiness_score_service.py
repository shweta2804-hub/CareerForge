from typing import Dict, Any, List
from app.services.skill_match_engine import SkillMatchEngine


class ReadinessScoreService:
    """Service to calculate placement readiness score."""

    @staticmethod
    def calculate_readiness_score(
        cgpa: float,
        skills: List[str],
        projects: List[Dict[str, Any]],
        assessment_scores: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate placement readiness score from 0-100.
        Components:
        - CGPA: 30% weight
        - Skills: 30% weight
        - Projects: 20% weight
        - Assessment Scores: 20% weight
        """
        # CGPA Score (30% weight)
        # CGPA is typically on 10-point scale
        cgpa_score = (cgpa / 10.0) * 30

        # Skills Score (30% weight)
        # Base score of 10, plus 2 points per skill up to 10 skills
        num_skills = len(skills)
        skills_score = min(10 + (num_skills * 2), 30) if num_skills > 0 else 10

        # Projects Score (20% weight)
        # Base score of 5, plus 3 points per project up to 5 projects
        num_projects = len(projects)
        projects_score = min(5 + (num_projects * 3), 20) if num_projects > 0 else 5

        # Assessment Scores (20% weight)
        assessment_score = 0
        if assessment_scores:
            total_percentage = sum(score.get("percentage", 0) for score in assessment_scores)
            avg_percentage = total_percentage / len(assessment_scores)
            assessment_score = (avg_percentage / 100.0) * 20
        else:
            assessment_score = 10  # Default if no assessments

        # Calculate total score
        total_score = cgpa_score + skills_score + projects_score + assessment_score
        total_score = min(total_score, 100)  # Cap at 100

        # Get readiness category
        category = SkillMatchEngine.get_readiness_category(total_score)

        return {
            "score": round(total_score, 2),
            "category": category,
            "breakdown": {
                "cgpa_score": round(cgpa_score, 2),
                "skills_score": round(skills_score, 2),
                "projects_score": round(projects_score, 2),
                "assessment_score": round(assessment_score, 2),
            }
        }

    @staticmethod
    def get_score_insights(score: float) -> Dict[str, Any]:
        """Get insights and recommendations based on readiness score."""
        category = SkillMatchEngine.get_readiness_category(score)
        
        insights = {
            "Beginner": {
                "message": "Focus on building foundational skills and improving CGPA",
                "recommendations": [
                    "Work on improving CGPA through consistent academic performance",
                    "Learn core programming languages and frameworks",
                    "Complete at least 2-3 projects to build practical experience",
                    "Take online courses to strengthen technical skills"
                ]
            },
            "Developing": {
                "message": "Good progress! Continue building skills and experience",
                "recommendations": [
                    "Add more specialized skills to your profile",
                    "Work on complex projects to demonstrate problem-solving",
                    "Prepare for technical interviews",
                    "Consider certifications in your domain"
                ]
            },
            "Placement Ready": {
                "message": "You're ready for placements! Focus on interview preparation",
                "recommendations": [
                    "Practice coding problems and data structures",
                    "Prepare for system design interviews",
                    "Build a strong LinkedIn profile",
                    "Network with industry professionals"
                ]
            },
            "Highly Competitive": {
                "message": "Excellent profile! You're a top candidate",
                "recommendations": [
                    "Target top-tier companies",
                    "Contribute to open source projects",
                    "Build a personal brand through blogging or talks",
                    "Mentor other students to strengthen leadership skills"
                ]
            }
        }

        return {
            "score": score,
            "category": category,
            "message": insights[category]["message"],
            "recommendations": insights[category]["recommendations"]
        }