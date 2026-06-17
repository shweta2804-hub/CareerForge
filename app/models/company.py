from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    package_offered = Column(Float, nullable=True)
    location = Column(String(255), nullable=False, index=True)
    minimum_cgpa = Column(Float, nullable=False)
    required_skills = Column(Text, nullable=True)  # JSON string of skills list
    job_description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    placement_drives = relationship("PlacementDrive", back_populates="company", cascade="all, delete-orphan")

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint('minimum_cgpa >= 0 AND minimum_cgpa <= 10', name='ck_cgpa_range'),
        CheckConstraint('package_offered IS NULL OR package_offered >= 0', name='ck_package_positive'),
        Index('idx_company_active', 'is_active', 'created_at'),
    )
