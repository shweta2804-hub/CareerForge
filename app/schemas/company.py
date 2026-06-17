from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class CompanyBase(BaseModel):
    name: str = Field(..., max_length=255)
    package_offered: Optional[float] = Field(None, ge=0.0)
    location: str = Field(..., max_length=255)
    minimum_cgpa: float = Field(..., ge=0.0, le=10.0)
    required_skills: Optional[List[str]] = None
    job_description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate company name is not empty."""
        if not v or not v.strip():
            raise ValueError('Company name cannot be empty')
        return v.strip()

    @field_validator('location')
    @classmethod
    def validate_location(cls, v: str) -> str:
        """Validate location is not empty."""
        if not v or not v.strip():
            raise ValueError('Location cannot be empty')
        return v.strip()


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    package_offered: Optional[float] = None
    location: Optional[str] = Field(None, max_length=255)
    minimum_cgpa: Optional[float] = Field(None, ge=0.0, le=10.0)
    required_skills: Optional[List[str]] = None
    job_description: Optional[str] = None
    is_active: Optional[bool] = None


class CompanyResponse(CompanyBase):
    id: int
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True