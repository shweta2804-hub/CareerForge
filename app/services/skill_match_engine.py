from typing import Dict, Any, List, Tuple


class SkillMatchEngine:
    """Engine to calculate skill match between student and company requirements."""

    @staticmethod
    def calculate_skill_match(student_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
        """
        Calculate skill match percentage.
        Returns match details including percentage, matched skills, and missing skills.
        """
        if not required_skills:
            return {
                "match_percentage": 100.0,
                "matched_skills": [],
                "missing_skills": [],
                "total_required": 0,
                "total_matched": 0,
            }

        student_skills_lower = set(skill.lower().strip() for skill in student_skills)
        required_skills_lower = [skill.lower().strip() for skill in required_skills]

        matched_skills = []
        missing_skills = []

        for skill in required_skills_lower:
            if skill in student_skills_lower:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        match_percentage = (len(matched_skills) / len(required_skills_lower)) * 100

        return {
            "match_percentage": round(match_percentage, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "total_required": len(required_skills_lower),
            "total_matched": len(matched_skills),
        }

    @staticmethod
    def get_readiness_category(score: float) -> str:
        """
        Get placement readiness category based on score.
        Categories: Beginner, Developing, Placement Ready, Highly Competitive
        """
        if score < 40:
            return "Beginner"
        elif score < 60:
            return "Developing"
        elif score < 80:
            return "Placement Ready"
        else:
            return "Highly Competitive"