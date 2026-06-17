from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentUpdate
from typing import Optional, List
import json


class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> Optional[Student]:
        """Get student by user ID."""
        return self.db.query(Student).filter(Student.user_id == user_id).first()

    def get_by_id(self, id: int) -> Optional[Student]:
        """Get student by ID."""
        return self.db.query(Student).filter(Student.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Student]:
        """Get all students with pagination."""
        return self.db.query(Student).offset(skip).limit(limit).all()

    def create(self, student_in: StudentCreate, user_id: int) -> Student:
        """Create a new student profile."""
        db_student = Student(
            user_id=user_id,
            branch=student_in.branch,
            cgpa=student_in.cgpa,
            graduation_year=student_in.graduation_year,
            skills=json.dumps(student_in.skills) if student_in.skills else None,
            projects=json.dumps(student_in.projects) if student_in.projects else None,
        )
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def update(self, student_id: int, student_in: StudentUpdate) -> Optional[Student]:
        """Update student profile."""
        db_student = self.get_by_id(student_id)
        if not db_student:
            return None
        update_data = student_in.model_dump(exclude_unset=True)
        if "skills" in update_data and update_data["skills"] is not None:
            update_data["skills"] = json.dumps(update_data["skills"])
        if "projects" in update_data and update_data["projects"] is not None:
            update_data["projects"] = json.dumps(update_data["projects"])
        for field, value in update_data.items():
            setattr(db_student, field, value)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def update_resume_url(self, student_id: int, resume_url: str) -> Optional[Student]:
        """Update student resume URL."""
        db_student = self.get_by_id(student_id)
        if not db_student:
            return None
        db_student.resume_url = resume_url
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def update_readiness_score(self, student_id: int, score: float) -> Optional[Student]:
        """Update placement readiness score."""
        db_student = self.get_by_id(student_id)
        if not db_student:
            return None
        db_student.placement_readiness_score = score
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def get_students_by_branch(self, branch: str) -> List[Student]:
        """Get students by branch."""
        return self.db.query(Student).filter(Student.branch == branch).all()

    def get_students_by_graduation_year(self, year: int) -> List[Student]:
        """Get students by graduation year."""
        return self.db.query(Student).filter(Student.graduation_year == year).all()