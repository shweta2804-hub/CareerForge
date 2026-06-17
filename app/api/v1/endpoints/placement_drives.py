from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.placement_drive import PlacementDriveCreate, PlacementDriveUpdate
from app.services.placement_drive_service import PlacementDriveService
from app.dependencies.auth import get_current_user, get_current_admin
from app.models.user import User
from typing import Dict, Any, List

router = APIRouter(prefix="/drives", tags=["Placement Drives"])


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def create_drive(
    drive_in: PlacementDriveCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new placement drive (admin only).
    Requires admin authentication.
    """
    try:
        drive_service = PlacementDriveService(db)
        result = drive_service.create_drive(drive_in)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create drive")


@router.get("", response_model=List[Dict[str, Any]])
def get_all_drives(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all placement drives.
    Requires authentication.
    """
    drive_service = PlacementDriveService(db)
    return drive_service.get_all_drives(skip=skip, limit=limit, status=status)


@router.get("/published", response_model=List[Dict[str, Any]])
def get_published_drives(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get published placement drives.
    Requires authentication.
    """
    drive_service = PlacementDriveService(db)
    return drive_service.get_published_drives(skip=skip, limit=limit)


@router.get("/{drive_id}", response_model=Dict[str, Any])
def get_drive(
    drive_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get placement drive by ID.
    Requires authentication.
    """
    drive_service = PlacementDriveService(db)
    result = drive_service.get_drive(drive_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drive not found")
    return result


@router.put("/{drive_id}", response_model=Dict[str, Any])
def update_drive(
    drive_id: int,
    drive_in: PlacementDriveUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update placement drive (admin only).
    Requires admin authentication.
    """
    drive_service = PlacementDriveService(db)
    result = drive_service.update_drive(drive_id, drive_in)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drive not found")
    return result


@router.post("/{drive_id}/publish", response_model=Dict[str, Any])
def publish_drive(
    drive_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Publish a placement drive (admin only).
    Requires admin authentication.
    """
    drive_service = PlacementDriveService(db)
    result = drive_service.publish_drive(drive_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drive not found")
    return result


@router.post("/{drive_id}/close", response_model=Dict[str, Any])
def close_drive(
    drive_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Close a placement drive (admin only).
    Requires admin authentication.
    """
    drive_service = PlacementDriveService(db)
    result = drive_service.close_drive(drive_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drive not found")
    return result


@router.delete("/{drive_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_drive(
    drive_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Delete placement drive (admin only).
    Requires admin authentication.
    """
    drive_service = PlacementDriveService(db)
    result = drive_service.delete_drive(drive_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drive not found")
    return None