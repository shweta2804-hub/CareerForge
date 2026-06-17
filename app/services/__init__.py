"""Services module."""

from app.services.auth_service import AuthService
from app.services.student_service import StudentService
from app.services.company_service import CompanyService
from app.services.placement_drive_service import PlacementDriveService
from app.services.application_service import ApplicationService
from app.services.assessment_service import AssessmentService
from app.services.analytics_service import AnalyticsService
from app.services.email_service import EmailService
from app.services.resume_service import ResumeService
from app.services.eligibility_engine import EligibilityEngine
from app.services.skill_match_engine import SkillMatchEngine
from app.services.readiness_score_service import ReadinessScoreService

__all__ = [
    "AuthService",
    "StudentService",
    "CompanyService",
    "PlacementDriveService",
    "ApplicationService",
    "AssessmentService",
    "AnalyticsService",
    "EmailService",
    "ResumeService",
    "EligibilityEngine",
    "SkillMatchEngine",
    "ReadinessScoreService",
]