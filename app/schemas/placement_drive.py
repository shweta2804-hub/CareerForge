from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class DriveStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class PlacementDriveBase(BaseModel):
    company_id: int
    drive_date: datetime
    application_deadline: datetime
    open_positions: int = Field(..., gt=0)
    description: Optional[str] = None

    @field_validator('application_deadline')
    @classmethod
    def validate_deadline(cls, v: datetime, info) -> datetime:
        """Validate that application deadline is before drive date."""
        if 'drive_date' in info.data and v >= info.data['drive_date']:
            raise ValueError('Application deadline must be before drive date')
        return v


class PlacementDriveCreate(PlacementDriveBase):
    pass


class PlacementDriveUpdate(BaseModel):
    drive_date: Optional[datetime] = None
    application_deadline: Optional[datetime] = None
    open_positions: Optional[int] = Field(None, gt=0)
    status: Optional[DriveStatus] = None
    description: Optional[str] = None


class PlacementDriveResponse(PlacementDriveBase):
    id: int
    status: DriveStatus
    created_at: str
    updated_at: str
    company_name: Optional[str] = None

    class Config:
        from_attributes = True