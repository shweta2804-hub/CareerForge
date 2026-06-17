from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database.connection import Base


class DriveStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class PlacementDrive(Base):
    __tablename__ = "placement_drives"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    drive_date = Column(DateTime, nullable=False)
    application_deadline = Column(DateTime, nullable=False)
    open_positions = Column(Integer, nullable=False)
    status = Column(Enum(DriveStatus), nullable=False, default=DriveStatus.DRAFT, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="placement_drives")
    applications = relationship("Application", back_populates="placement_drive", cascade="all, delete-orphan")

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint('open_positions > 0', name='ck_open_positions_positive'),
        Index('idx_drive_company_status', 'company_id', 'status'),
        Index('idx_drive_deadline', 'application_deadline'),
    )
