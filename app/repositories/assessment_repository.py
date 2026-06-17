from sqlalchemy.orm import Session
from app.models.assessment import Assessment, AssessmentScore
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate, AssessmentScoreCreate
from typing import Optional, List


class AssessmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Assessment]:
        """Get assessment by ID."""
        return self.db.query(Assessment).filter(Assessment.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Assessment]:
        """Get all assessments with pagination."""
        query = self.db.query(Assessment)
        if active_only:
            query = query.filter(Assessment.is_active == True)
        return query.offset(skip).limit(limit).all()

    def create(self, assessment_in: AssessmentCreate) -> Assessment:
        """Create a new assessment."""
        db_assessment = Assessment(
            title=assessment_in.title,
            description=assessment_in.description,
            total_marks=assessment_in.total_marks,
            passing_marks=assessment_in.passing_marks,
        )
        self.db.add(db_assessment)
        self.db.commit()
        self.db.refresh(db_assessment)
        return db_assessment

    def update(self, assessment_id: int, assessment_in: AssessmentUpdate) -> Optional[Assessment]:
        """Update assessment."""
        db_assessment = self.get_by_id(assessment_id)
        if not db_assessment:
            return None
        update_data = assessment_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_assessment, field, value)
        self.db.commit()
        self.db.refresh(db_assessment)
        return db_assessment

    def delete(self, assessment_id: int) -> bool:
        """Delete assessment."""
        db_assessment = self.get_by_id(assessment_id)
        if not db_assessment:
            return False
        self.db.delete(db_assessment)
        self.db.commit()
        return True

    def record_score(self, score_in: AssessmentScoreCreate, student_id: int) -> AssessmentScore:
        """Record assessment score for a student."""
        percentage = (score_in.score / self.get_by_id(score_in.assessment_id).total_marks) * 100
        passed = score_in.score >= self.get_by_id(score_in.assessment_id).passing_marks
        
        db_score = AssessmentScore(
            student_id=student_id,
            assessment_id=score_in.assessment_id,
            score=score_in.score,
            percentage=percentage,
            passed=passed,
        )
        self.db.add(db_score)
        self.db.commit()
        self.db.refresh(db_score)
        return db_score

    def get_scores_by_student(self, student_id: int) -> List[AssessmentScore]:
        """Get all assessment scores for a student."""
        return self.db.query(AssessmentScore).filter(AssessmentScore.student_id == student_id).all()

    def get_scores_by_assessment(self, assessment_id: int) -> List[AssessmentScore]:
        """Get all scores for an assessment."""
        return self.db.query(AssessmentScore).filter(AssessmentScore.assessment_id == assessment_id).all()

    def get_student_score_for_assessment(self, student_id: int, assessment_id: int) -> Optional[AssessmentScore]:
        """Get student's score for a specific assessment."""
        return self.db.query(AssessmentScore).filter(
            AssessmentScore.student_id == student_id,
            AssessmentScore.assessment_id == assessment_id
        ).first()