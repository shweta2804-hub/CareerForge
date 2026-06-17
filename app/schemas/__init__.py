"""Pydantic schemas module."""

from app.schemas.user import UserRole, UserBase, UserCreate, UserUpdate, UserResponse, Token, TokenPayload
from app.schemas.student import StudentBase, StudentCreate, StudentUpdate, StudentResponse, StudentWithUser
from app.schemas.company import CompanyBase, CompanyCreate, CompanyUpdate, CompanyResponse
from app.schemas.placement_drive import DriveStatus, PlacementDriveBase, PlacementDriveCreate, PlacementDriveUpdate, PlacementDriveResponse
from app.schemas.application import ApplicationStatus, ApplicationBase, ApplicationCreate, ApplicationUpdate, ApplicationResponse, ApplicationWithDetails
from app.schemas.assessment import AssessmentBase, AssessmentCreate, AssessmentUpdate, AssessmentResponse, AssessmentScoreBase, AssessmentScoreCreate, AssessmentScoreResponse
from app.schemas.analytics import AnalyticsOverview, TopHiringCompany, BranchPlacementStats, AnalyticsResponse

__all__ = [
    "UserRole",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "Token",
    "TokenPayload",
    "StudentBase",
    "StudentCreate",
    "StudentUpdate",
    "StudentResponse",
    "StudentWithUser",
    "CompanyBase",
    "CompanyCreate",
    "CompanyUpdate",
    "CompanyResponse",
    "DriveStatus",
    "PlacementDriveBase",
    "PlacementDriveCreate",
    "PlacementDriveUpdate",
    "PlacementDriveResponse",
    "ApplicationStatus",
    "ApplicationBase",
    "ApplicationCreate",
    "ApplicationUpdate",
    "ApplicationResponse",
    "ApplicationWithDetails",
    "AssessmentBase",
    "AssessmentCreate",
    "AssessmentUpdate",
    "AssessmentResponse",
    "AssessmentScoreBase",
    "AssessmentScoreCreate",
    "AssessmentScoreResponse",
    "AnalyticsOverview",
    "TopHiringCompany",
    "BranchPlacementStats",
    "AnalyticsResponse",
]