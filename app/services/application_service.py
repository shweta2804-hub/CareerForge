from sqlalchemy.orm import Session
from app.repositories.application_repository import ApplicationRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.placement_drive_repository import PlacementDriveRepository
from app.repositories.company_repository import CompanyRepository
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from typing import Optional, Dict, Any, List
from datetime import datetime


class ApplicationService:
    def __init__(self, db: Session):
        self.db = db
        self.app_repo = ApplicationRepository(db)
        self.student_repo = StudentRepository(db)
        self.drive_repo = PlacementDriveRepository(db)
        self.company_repo = CompanyRepository(db)

    def apply_to_drive(self, student_id: int, drive_id: int) -> Dict[str, Any]:
        """Apply to a placement drive."""
        # Check if already applied
        existing_application = self.app_repo.get_by_student_and_drive(student_id, drive_id)
        if existing_application:
            raise ValueError("Already applied to this drive")

        # Check if drive exists and is published
        drive = self.drive_repo.get_by_id(drive_id)
        if not drive:
            raise ValueError("Placement drive not found")
        if drive.status.value != "published":
            raise ValueError("Drive is not published")
        if self.drive_repo.is_deadline_passed(drive_id):
            raise ValueError("Application deadline has passed")

        # Create application
        application_in = ApplicationCreate(drive_id=drive_id)
        application = self.app_repo.create(application_in, student_id)
        
        return self._format_application_response(application)

    def get_student_applications(self, student_id: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all applications for a student."""
        applications = self.app_repo.get_by_student_id(student_id, skip=skip, limit=limit)
        return [self._format_application_response(app) for app in applications]

    def get_drive_applications(self, drive_id: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all applications for a drive."""
        applications = self.app_repo.get_by_drive_id(drive_id, skip=skip, limit=limit)
        return [self._format_application_response(app) for app in applications]

    def get_application(self, application_id: int) -> Optional[Dict[str, Any]]:
        """Get application by ID."""
        application = self.app_repo.get_by_id(application_id)
        if not application:
            return None
        return self._format_application_response(application)

    def update_application_status(self, application_id: int, status: str, rejection_reason: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update application status."""
        from app.models.application import ApplicationStatus
        app_status = ApplicationStatus(status)
        application = self.app_repo.update_status(application_id, app_status, rejection_reason)
        if not application:
            return None
        return self._format_application_response(application)

    def get_all_applications(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """
        Get all applications with pagination.
        
        Args:
            page: Page number (1-indexed)
            limit: Items per page (max 100)
        
        Returns:
            Dict with items, page, limit, total, pages
        """
        # Validate and sanitize parameters
        page = max(1, page)
        limit = min(max(1, limit), 100)  # Max 100 items per page
        
        # Calculate skip
        skip = (page - 1) * limit
        
        # Get paginated data
        applications = self.app_repo.get_all(skip=skip, limit=limit)
        total = self.app_repo.count()
        
        # Calculate total pages
        pages = (total + limit - 1) // limit  # Ceiling division
        
        return {
            "items": [self._format_application_response(app) for app in applications],
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        }

    def _format_application_response(self, application) -> Dict[str, Any]:
        """Format application response."""
        student = self.student_repo.get_by_id(application.student_id)
        drive = self.drive_repo.get_by_id(application.drive_id)
        company = self.company_repo.get_by_id(drive.company_id) if drive else None
        
        user = None
        if student:
            from app.repositories.user_repository import UserRepository
            user_repo = UserRepository(self.db)
            user = user_repo.get_by_id(student.user_id)

        return {
            "id": application.id,
            "student_id": application.student_id,
            "drive_id": application.drive_id,
            "status": application.status.value,
            "skill_match_percentage": application.skill_match_percentage,
            "eligibility_status": application.eligibility_status,
            "rejection_reason": application.rejection_reason,
            "applied_at": application.applied_at.isoformat() if application.applied_at else "",
            "updated_at": application.updated_at.isoformat() if application.updated_at else "",
            "company_name": company.name if company else "",
            "drive_date": drive.drive_date.isoformat() if drive and drive.drive_date else "",
            "student_name": user.full_name if user else "",
            "student_email": user.email if user else "",
            "student_branch": student.branch if student else "",
            "student_cgpa": student.cgpa if student else 0.0,
        }