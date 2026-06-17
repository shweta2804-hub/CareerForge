"""Repositories module."""

from app.repositories.base import BaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.placement_drive_repository import PlacementDriveRepository
from app.repositories.application_repository import ApplicationRepository
from app.repositories.assessment_repository import AssessmentRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "StudentRepository",
    "CompanyRepository",
    "PlacementDriveRepository",
    "ApplicationRepository",
    "AssessmentRepository",
]