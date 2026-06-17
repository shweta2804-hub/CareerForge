from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    SELECTED = "selected"
    REJECTED = "rejected"


class ApplicationBase(BaseModel):
    drive_id: int


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    rejection_reason: Optional[str] = None


class ApplicationResponse(ApplicationBase):
    id: int
    student_id: int
    status: ApplicationStatus
    skill_match_percentage: Optional[float] = None
    eligibility_status: Optional[str] = None
    rejection_reason: Optional[str] = None
    applied_at: str
    updated_at: str
    company_name: Optional[str] = None
    drive_date: Optional[str] = None

    class Config:
        from_attributes = True


class ApplicationWithDetails(ApplicationResponse):
    student_name: str
    student_email: str
    student_branch: str
    student_cgpa: float

    class Config:
        from_attributes = True