from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate, AssessmentScoreCreate, AssessmentScoreResponse
from app.services.assessment_service import AssessmentService
from app.dependencies.auth import get_current_user, get_current_admin, get_current_active_student
from app.models.user import User
from typing import Dict, Any, List

router = APIRouter(prefix="/assessments", tags=["Assessments"])


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def create_assessment(
    assessment_in: AssessmentCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new assessment (admin only).
    Requires admin authentication.
    """
    try:
        assessment_service = AssessmentService(db)
        result = assessment_service.create_assessment(assessment_in)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create assessment")


@router.get("", response_model=List[Dict[str, Any]])
def get_all_assessments(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all assessments.
    Requires authentication.
    """
    assessment_service = AssessmentService(db)
    return assessment_service.get_all_assessments(skip=skip, limit=limit)


@router.get("/{assessment_id}", response_model=Dict[str, Any])
def get_assessment(
    assessment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get assessment by ID.
    Requires authentication.
    """
    assessment_service = AssessmentService(db)
    result = assessment_service.get_assessment(assessment_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")
    return result


@router.put("/{assessment_id}", response_model=Dict[str, Any])
def update_assessment(
    assessment_id: int,
    assessment_in: AssessmentUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update assessment (admin only).
    Requires admin authentication.
    """
    assessment_service = AssessmentService(db)
    result = assessment_service.update_assessment(assessment_id, assessment_in)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")
    return result


@router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assessment(
    assessment_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Delete assessment (admin only).
    Requires admin authentication.
    """
    assessment_service = AssessmentService(db)
    result = assessment_service.delete_assessment(assessment_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")
    return None


@router.post("/{assessment_id}/submit", response_model=Dict[str, Any])
def submit_assessment(
    assessment_id: int,
    score_in: AssessmentScoreCreate,
    current_user: User = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    """
    Submit assessment score (student only).
    Requires student authentication.
    """
    try:
        from app.repositories.student_repository import StudentRepository
        student_repo = StudentRepository(db)
        student = student_repo.get_by_user_id(current_user.id)
        
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
        
        assessment_service = AssessmentService(db)
        result = assessment_service.record_score(score_in, student.id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to submit assessment")


@router.get("/my-scores", response_model=List[Dict[str, Any]])
def get_my_assessment_scores(
    current_user: User = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    """
    Get current student's assessment scores.
    Requires student authentication.
    """
    from app.repositories.student_repository import StudentRepository
    student_repo = StudentRepository(db)
    student = student_repo.get_by_user_id(current_user.id)
    
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    assessment_service = AssessmentService(db)
    return assessment_service.get_student_scores(student.id)


@router.get("/{assessment_id}/scores", response_model=List[Dict[str, Any]])
def get_assessment_scores(
    assessment_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get all scores for an assessment (admin only).
    Requires admin authentication.
    """
    assessment_service = AssessmentService(db)
    return assessment_service.get_assessment_scores(assessment_id)