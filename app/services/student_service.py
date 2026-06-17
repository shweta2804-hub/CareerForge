from sqlalchemy.orm import Session
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.student import StudentCreate, StudentUpdate
from typing import Optional, Dict, Any, List
import json


class StudentService:
    def __init__(self, db: Session):
        self.db = db
        self.student_repo = StudentRepository(db)
        self.user_repo = UserRepository(db)

    def create_student_profile(self, user_id: int, student_in: StudentCreate) -> Dict[str, Any]:
        """Create student profile."""
        existing_student = self.student_repo.get_by_user_id(user_id)
        if existing_student:
            raise ValueError("Student profile already exists")

        student = self.student_repo.create(student_in, user_id)
        return self._format_student_response(student)

    def get_student_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get student profile by user ID."""
        student = self.student_repo.get_by_user_id(user_id)
        if not student:
            return None
        return self._format_student_response(student)

    def get_student_by_id(self, student_id: int) -> Optional[Dict[str, Any]]:
        """Get student by ID."""
        student = self.student_repo.get_by_id(student_id)
        if not student:
            return None
        return self._format_student_response(student)

    def update_student_profile(self, user_id: int, student_in: StudentUpdate) -> Optional[Dict[str, Any]]:
        """Update student profile."""
        student = self.student_repo.get_by_user_id(user_id)
        if not student:
            return None
        updated_student = self.student_repo.update(student.id, student_in)
        if not updated_student:
            return None
        return self._format_student_response(updated_student)

    def update_resume(self, user_id: int, resume_url: str) -> Optional[Dict[str, Any]]:
        """Update student resume URL."""
        student = self.student_repo.get_by_user_id(user_id)
        if not student:
            return None
        updated_student = self.student_repo.update_resume_url(student.id, resume_url)
        if not updated_student:
            return None
        return self._format_student_response(updated_student)

    def get_all_students(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """
        Get all students with pagination.
        
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
        students = self.student_repo.get_all(skip=skip, limit=limit)
        total = self.student_repo.count()
        
        # Calculate total pages
        pages = (total + limit - 1) // limit  # Ceiling division
        
        return {
            "items": [self._format_student_response(student) for student in students],
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        }

    def _format_student_response(self, student) -> Dict[str, Any]:
        """Format student response."""
        user = self.user_repo.get_by_id(student.user_id)
        return {
            "id": student.id,
            "user_id": student.user_id,
            "user_name": user.full_name if user else "",
            "user_email": user.email if user else "",
            "branch": student.branch,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year,
            "skills": json.loads(student.skills) if student.skills else [],
            "projects": json.loads(student.projects) if student.projects else [],
            "resume_url": student.resume_url,
            "placement_readiness_score": student.placement_readiness_score,
            "created_at": student.created_at.isoformat() if student.created_at else "",
            "updated_at": student.updated_at.isoformat() if student.updated_at else "",
        }