from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.student import StudentCreate, StudentUpdate
from app.services.student_service import StudentService
from app.services.resume_service import ResumeService
from app.dependencies.auth import get_current_user, get_current_active_student, get_current_admin
from app.models.user import User
from typing import Dict, Any, List

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/profile", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def create_student_profile(
    student_in: StudentCreate,
    current_user: User = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    """
    Create student profile.
    Requires student authentication.
    """
    try:
        student_service = StudentService(db)
        result = student_service.create_student_profile(current_user.id, student_in)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create profile")


@router.get("/profile", response_model=Dict[str, Any])
def get_student_profile(
    current_user: User = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    """
    Get current student's profile.
    Requires student authentication.
    """
    student_service = StudentService(db)
    result = student_service.get_student_profile(current_user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return result


@router.put("/profile", response_model=Dict[str, Any])
def update_student_profile(
    student_in: StudentUpdate,
    current_user: User = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    """
    Update student profile.
    Requires student authentication.
    """
    try:
        student_service = StudentService(db)
        result = student_service.update_student_profile(current_user.id, student_in)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update profile")


@router.post("/resume", response_model=Dict[str, Any])
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    """
    Upload resume (PDF only, max 5MB).
    Requires student authentication.
    """
    try:
        # Validate file
        file_content = await file.read()
        ResumeService.validate_resume_file(file.filename, len(file_content))

        # Upload to Cloudinary
        student_service = StudentService(db)
        student = student_service.get_student_profile(current_user.id)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

        upload_result = ResumeService.upload_resume(file_content, file.filename, student["id"])
        
        # Update student profile with resume URL
        updated_student = student_service.update_resume(current_user.id, upload_result["url"])
        return {
            "message": "Resume uploaded successfully",
            "resume_url": upload_result["url"],
            "student": updated_student
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload resume")


@router.get("/all", response_model=Dict[str, Any])
def get_all_students(
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get all students with pagination (admin only).
    Requires admin authentication.
    """
    student_service = StudentService(db)
    return student_service.get_all_students(page=page, limit=limit)


@router.get("/{student_id}", response_model=Dict[str, Any])
def get_student_by_id(
    student_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get student by ID (admin only).
    Requires admin authentication.
    """
    student_service = StudentService(db)
    result = student_service.get_student_by_id(student_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return result