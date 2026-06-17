from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from app.services.application_service import ApplicationService
from app.services.eligibility_engine import EligibilityEngine
from app.services.skill_match_engine import SkillMatchEngine
from app.dependencies.auth import get_current_user, get_current_active_student, get_current_admin
from app.models.user import User
from typing import Dict, Any, List

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def apply_to_drive(
    application_in: ApplicationCreate,
    current_user: User = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    """
    Apply to a placement drive.
    Requires student authentication.
    """
    try:
        application_service = ApplicationService(db)
        result = application_service.apply_to_drive(current_user.id, application_in.drive_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to apply to drive")


@router.get("/my-applications", response_model=List[Dict[str, Any]])
def get_my_applications(
    current_user: User = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    """
    Get current student's applications.
    Requires student authentication.
    """
    from app.repositories.student_repository import StudentRepository
    student_repo = StudentRepository(db)
    student = student_repo.get_by_user_id(current_user.id)
    
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    application_service = ApplicationService(db)
    return application_service.get_student_applications(student.id)


@router.get("/drive/{drive_id}", response_model=List[Dict[str, Any]])
def get_drive_applications(
    drive_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get all applications for a drive (admin only).
    Requires admin authentication.
    """
    application_service = ApplicationService(db)
    return application_service.get_drive_applications(drive_id)


@router.get("/{application_id}", response_model=Dict[str, Any])
def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get application by ID.
    Requires authentication.
    """
    application_service = ApplicationService(db)
    result = application_service.get_application(application_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return result


@router.put("/{application_id}/status", response_model=Dict[str, Any])
def update_application_status(
    application_id: int,
    status: str,
    rejection_reason: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update application status (admin only).
    Requires admin authentication.
    """
    application_service = ApplicationService(db)
    result = application_service.update_application_status(application_id, status, rejection_reason)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return result


@router.get("", response_model=Dict[str, Any])
def get_all_applications(
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get all applications with pagination (admin only).
    Requires admin authentication.
    """
    application_service = ApplicationService(db)
    return application_service.get_all_applications(page=page, limit=limit)
