from typing import Dict, Any, List, Tuple
import json


class EligibilityEngine:
    """Engine to check student eligibility for placement drives."""

    @staticmethod
    def check_eligibility(student: Dict[str, Any], company: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Check if student is eligible for a company/drive.
        Returns (is_eligible, reason).
        """
        reasons = []

        # Check CGPA
        if student.get("cgpa", 0) < company.get("minimum_cgpa", 0):
            reasons.append(f"CGPA {student.get('cgpa')} is less than required {company.get('minimum_cgpa')}")

        # Check required skills
        student_skills = set(skill.lower() for skill in student.get("skills", []))
        required_skills = set(skill.lower() for skill in company.get("required_skills", []))

        missing_skills = required_skills - student_skills
        if missing_skills:
            reasons.append(f"Missing required skills: {', '.join(missing_skills)}")

        is_eligible = len(reasons) == 0
        reason = "; ".join(reasons) if reasons else "Eligible"

        return is_eligible, reason

    @staticmethod
    def get_eligibility_details(student: Dict[str, Any], company: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed eligibility information."""
        is_eligible, reason = EligibilityEngine.check_eligibility(student, company)

        student_skills = set(skill.lower() for skill in student.get("skills", []))
        required_skills = set(skill.lower() for skill in company.get("required_skills", []))
        matched_skills = required_skills & student_skills
        missing_skills = required_skills - student_skills

        return {
            "is_eligible": is_eligible,
            "reason": reason,
            "cgpa_match": student.get("cgpa", 0) >= company.get("minimum_cgpa", 0),
            "student_cgpa": student.get("cgpa"),
            "required_cgpa": company.get("minimum_cgpa"),
            "matched_skills": list(matched_skills),
            "missing_skills": list(missing_skills),
            "skill_match_percentage": (len(matched_skills) / len(required_skills) * 100) if required_skills else 100,
        }