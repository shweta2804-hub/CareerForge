from sqlalchemy.orm import Session
from app.repositories.placement_drive_repository import PlacementDriveRepository
from app.repositories.company_repository import CompanyRepository
from app.schemas.placement_drive import PlacementDriveCreate, PlacementDriveUpdate
from typing import Optional, Dict, Any, List
from datetime import datetime


class PlacementDriveService:
    def __init__(self, db: Session):
        self.db = db
        self.drive_repo = PlacementDriveRepository(db)
        self.company_repo = CompanyRepository(db)

    def create_drive(self, drive_in: PlacementDriveCreate) -> Dict[str, Any]:
        """Create a new placement drive."""
        company = self.company_repo.get_by_id(drive_in.company_id)
        if not company:
            raise ValueError("Company not found")

        drive = self.drive_repo.create(drive_in)
        return self._format_drive_response(drive)

    def get_drive(self, drive_id: int) -> Optional[Dict[str, Any]]:
        """Get placement drive by ID."""
        drive = self.drive_repo.get_by_id(drive_id)
        if not drive:
            return None
        return self._format_drive_response(drive)

    def get_all_drives(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all placement drives."""
        from app.models.placement_drive import DriveStatus
        drive_status = DriveStatus(status) if status else None
        drives = self.drive_repo.get_all(skip=skip, limit=limit, status=drive_status)
        return [self._format_drive_response(drive) for drive in drives]

    def get_published_drives(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get published placement drives."""
        drives = self.drive_repo.get_published_drives(skip=skip, limit=limit)
        return [self._format_drive_response(drive) for drive in drives]

    def update_drive(self, drive_id: int, drive_in: PlacementDriveUpdate) -> Optional[Dict[str, Any]]:
        """Update placement drive."""
        drive = self.drive_repo.update(drive_id, drive_in)
        if not drive:
            return None
        return self._format_drive_response(drive)

    def publish_drive(self, drive_id: int) -> Optional[Dict[str, Any]]:
        """Publish a placement drive."""
        drive = self.drive_repo.publish(drive_id)
        if not drive:
            return None
        return self._format_drive_response(drive)

    def close_drive(self, drive_id: int) -> Optional[Dict[str, Any]]:
        """Close a placement drive."""
        drive = self.drive_repo.close(drive_id)
        if not drive:
            return None
        return self._format_drive_response(drive)

    def delete_drive(self, drive_id: int) -> bool:
        """Delete placement drive."""
        return self.drive_repo.delete(drive_id)

    def get_drives_by_company(self, company_id: int) -> List[Dict[str, Any]]:
        """Get placement drives by company."""
        drives = self.drive_repo.get_by_company_id(company_id)
        return [self._format_drive_response(drive) for drive in drives]

    def _format_drive_response(self, drive) -> Dict[str, Any]:
        """Format drive response."""
        company = self.company_repo.get_by_id(drive.company_id)
        return {
            "id": drive.id,
            "company_id": drive.company_id,
            "company_name": company.name if company else "",
            "drive_date": drive.drive_date.isoformat() if drive.drive_date else "",
            "application_deadline": drive.application_deadline.isoformat() if drive.application_deadline else "",
            "open_positions": drive.open_positions,
            "status": drive.status.value,
            "description": drive.description,
            "created_at": drive.created_at.isoformat() if drive.created_at else "",
            "updated_at": drive.updated_at.isoformat() if drive.updated_at else "",
        }