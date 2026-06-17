from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database.connection import Base


class ApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    SELECTED = "selected"
    REJECTED = "rejected"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    drive_id = Column(Integer, ForeignKey("placement_drives.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(ApplicationStatus), nullable=False, default=ApplicationStatus.APPLIED, index=True)
    skill_match_percentage = Column(Float, nullable=True)
    eligibility_status = Column(String(50), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="applications")
    placement_drive = relationship("PlacementDrive", back_populates="applications")

    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint('student_id', 'drive_id', name='uq_student_drive'),
        Index('idx_application_status', 'status'),
        Index('idx_application_student_status', 'student_id', 'status'),
    )
