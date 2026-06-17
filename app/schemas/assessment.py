from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AssessmentBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    total_marks: float = Field(..., gt=0)
    passing_marks: float = Field(..., gt=0)


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    total_marks: Optional[float] = Field(None, gt=0)
    passing_marks: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None


class AssessmentResponse(AssessmentBase):
    id: int
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class AssessmentScoreBase(BaseModel):
    assessment_id: int
    score: float = Field(..., ge=0)


class AssessmentScoreCreate(AssessmentScoreBase):
    pass


class AssessmentScoreResponse(AssessmentScoreBase):
    id: int
    student_id: int
    percentage: float
    passed: bool
    completed_at: str
    created_at: str
    assessment_title: Optional[str] = None

    class Config:
        from_attributes = True