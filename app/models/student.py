from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    branch = Column(String(100), nullable=False, index=True)
    cgpa = Column(Float, nullable=False)
    graduation_year = Column(Integer, nullable=False, index=True)
    skills = Column(Text, nullable=True)  # JSON string of skills list
    projects = Column(Text, nullable=True)  # JSON string of projects list
    resume_url = Column(String(500), nullable=True)
    placement_readiness_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="student_profile")
    applications = relationship("Application", back_populates="student", cascade="all, delete-orphan")
    assessment_scores = relationship("AssessmentScore", back_populates="student", cascade="all, delete-orphan")

    # Additional indexes
    __table_args__ = (
        Index('idx_student_branch_year', 'branch', 'graduation_year'),
    )
