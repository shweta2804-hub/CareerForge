from sqlalchemy.orm import Session
from app.repositories.assessment_repository import AssessmentRepository
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate, AssessmentScoreCreate
from typing import Dict, Any, List


class AssessmentService:
    def __init__(self, db: Session):
        self.db = db
        self.assessment_repo = AssessmentRepository(db)

    def create_assessment(self, assessment_in: AssessmentCreate) -> Dict[str, Any]:
        """Create a new assessment."""
        assessment = self.assessment_repo.create(assessment_in)
        return self._format_assessment_response(assessment)

    def get_assessment(self, assessment_id: int) -> Dict[str, Any]:
        """Get assessment by ID."""
        assessment = self.assessment_repo.get_by_id(assessment_id)
        if not assessment:
            return None
        return self._format_assessment_response(assessment)

    def get_all_assessments(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all assessments."""
        assessments = self.assessment_repo.get_all(skip=skip, limit=limit)
        return [self._format_assessment_response(assessment) for assessment in assessments]

    def update_assessment(self, assessment_id: int, assessment_in: AssessmentUpdate) -> Dict[str, Any]:
        """Update assessment."""
        assessment = self.assessment_repo.update(assessment_id, assessment_in)
        if not assessment:
            return None
        return self._format_assessment_response(assessment)

    def delete_assessment(self, assessment_id: int) -> bool:
        """Delete assessment."""
        return self.assessment_repo.delete(assessment_id)

    def record_score(self, score_in: AssessmentScoreCreate, student_id: int) -> Dict[str, Any]:
        """Record assessment score."""
        score = self.assessment_repo.record_score(score_in, student_id)
        return self._format_score_response(score)

    def get_student_scores(self, student_id: int) -> List[Dict[str, Any]]:
        """Get all scores for a student."""
        scores = self.assessment_repo.get_scores_by_student(student_id)
        return [self._format_score_response(score) for score in scores]

    def get_assessment_scores(self, assessment_id: int) -> List[Dict[str, Any]]:
        """Get all scores for an assessment."""
        scores = self.assessment_repo.get_scores_by_assessment(assessment_id)
        return [self._format_score_response(score) for score in scores]

    def _format_assessment_response(self, assessment) -> Dict[str, Any]:
        """Format assessment response."""
        return {
            "id": assessment.id,
            "title": assessment.title,
            "description": assessment.description,
            "total_marks": assessment.total_marks,
            "passing_marks": assessment.passing_marks,
            "is_active": assessment.is_active,
            "created_at": assessment.created_at.isoformat() if assessment.created_at else "",
            "updated_at": assessment.updated_at.isoformat() if assessment.updated_at else "",
        }

    def _format_score_response(self, score) -> Dict[str, Any]:
        """Format score response."""
        return {
            "id": score.id,
            "student_id": score.student_id,
            "assessment_id": score.assessment_id,
            "assessment_title": score.assessment.title if score.assessment else "",
            "score": score.score,
            "percentage": score.percentage,
            "passed": score.passed,
            "completed_at": score.completed_at.isoformat() if score.completed_at else "",
            "created_at": score.created_at.isoformat() if score.created_at else "",
        }