from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any
from datetime import datetime


class StudentBase(BaseModel):
    branch: str = Field(..., max_length=100)
    cgpa: float = Field(..., ge=0.0, le=10.0)
    graduation_year: int = Field(..., ge=2020, le=2030)
    skills: Optional[List[str]] = None
    projects: Optional[List[Any]] = None

    @field_validator('branch')
    @classmethod
    def validate_branch(cls, v: str) -> str:
        """Validate branch is not empty."""
        if not v or not v.strip():
            raise ValueError('Branch cannot be empty')
        return v.strip()


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    branch: Optional[str] = Field(None, max_length=100)
    cgpa: Optional[float] = Field(None, ge=0.0, le=10.0)
    graduation_year: Optional[int] = Field(None, ge=2020, le=2030)
    skills: Optional[List[str]] = None
    projects: Optional[List[Any]] = None


class StudentResponse(StudentBase):
    id: int
    user_id: int
    resume_url: Optional[str] = None
    placement_readiness_score: float
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class StudentWithUser(StudentResponse):
    user_name: str
    user_email: str

    class Config:
        from_attributes = True