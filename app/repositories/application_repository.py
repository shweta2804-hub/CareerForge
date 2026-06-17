from sqlalchemy.orm import Session
from app.models.application import Application, ApplicationStatus
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from typing import Optional, List


class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Application]:
        """Get application by ID."""
        return self.db.query(Application).filter(Application.id == id).first()

    def get_by_student_and_drive(self, student_id: int, drive_id: int) -> Optional[Application]:
        """Get application by student and drive ID."""
        return self.db.query(Application).filter(
            Application.student_id == student_id,
            Application.drive_id == drive_id
        ).first()

    def get_by_student_id(self, student_id: int, skip: int = 0, limit: int = 100) -> List[Application]:
        """Get applications by student ID."""
        return self.db.query(Application).filter(Application.student_id == student_id).offset(skip).limit(limit).all()

    def get_by_drive_id(self, drive_id: int, skip: int = 0, limit: int = 100) -> List[Application]:
        """Get applications by drive ID."""
        return self.db.query(Application).filter(Application.drive_id == drive_id).offset(skip).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Application]:
        """Get all applications with pagination."""
        return self.db.query(Application).offset(skip).limit(limit).all()

    def create(self, application_in: ApplicationCreate, student_id: int, skill_match_percentage: float = None, eligibility_status: str = None) -> Application:
        """Create a new application."""
        db_application = Application(
            student_id=student_id,
            drive_id=application_in.drive_id,
            skill_match_percentage=skill_match_percentage,
            eligibility_status=eligibility_status,
        )
        self.db.add(db_application)
        self.db.commit()
        self.db.refresh(db_application)
        return db_application

    def update(self, application_id: int, application_in: ApplicationUpdate) -> Optional[Application]:
        """Update application."""
        db_application = self.get_by_id(application_id)
        if not db_application:
            return None
        update_data = application_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_application, field, value)
        self.db.commit()
        self.db.refresh(db_application)
        return db_application

    def update_status(self, application_id: int, status: ApplicationStatus, rejection_reason: str = None) -> Optional[Application]:
        """Update application status."""
        db_application = self.get_by_id(application_id)
        if not db_application:
            return None
        db_application.status = status
        if rejection_reason:
            db_application.rejection_reason = rejection_reason
        self.db.commit()
        self.db.refresh(db_application)
        return db_application

    def has_applied(self, student_id: int, drive_id: int) -> bool:
        """Check if student has already applied to a drive."""
        return self.db.query(Application).filter(
            Application.student_id == student_id,
            Application.drive_id == drive_id
        ).first() is not None

    def count_by_status(self, status: ApplicationStatus) -> int:
        """Count applications by status."""
        return self.db.query(Application).filter(Application.status == status).count()