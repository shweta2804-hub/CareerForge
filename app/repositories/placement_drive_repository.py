from sqlalchemy.orm import Session
from app.models.placement_drive import PlacementDrive, DriveStatus
from app.schemas.placement_drive import PlacementDriveCreate, PlacementDriveUpdate
from typing import Optional, List
from datetime import datetime


class PlacementDriveRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[PlacementDrive]:
        """Get placement drive by ID."""
        return self.db.query(PlacementDrive).filter(PlacementDrive.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100, status: Optional[DriveStatus] = None) -> List[PlacementDrive]:
        """Get all placement drives with pagination and optional status filter."""
        query = self.db.query(PlacementDrive)
        if status:
            query = query.filter(PlacementDrive.status == status)
        return query.offset(skip).limit(limit).all()

    def get_by_company_id(self, company_id: int) -> List[PlacementDrive]:
        """Get placement drives by company ID."""
        return self.db.query(PlacementDrive).filter(PlacementDrive.company_id == company_id).all()

    def get_published_drives(self, skip: int = 0, limit: int = 100) -> List[PlacementDrive]:
        """Get published placement drives."""
        return self.db.query(PlacementDrive).filter(PlacementDrive.status == DriveStatus.PUBLISHED).offset(skip).limit(limit).all()

    def create(self, drive_in: PlacementDriveCreate) -> PlacementDrive:
        """Create a new placement drive."""
        db_drive = PlacementDrive(
            company_id=drive_in.company_id,
            drive_date=drive_in.drive_date,
            application_deadline=drive_in.application_deadline,
            open_positions=drive_in.open_positions,
            description=drive_in.description,
        )
        self.db.add(db_drive)
        self.db.commit()
        self.db.refresh(db_drive)
        return db_drive

    def update(self, drive_id: int, drive_in: PlacementDriveUpdate) -> Optional[PlacementDrive]:
        """Update placement drive."""
        db_drive = self.get_by_id(drive_id)
        if not db_drive:
            return None
        update_data = drive_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_drive, field, value)
        self.db.commit()
        self.db.refresh(db_drive)
        return db_drive

    def publish(self, drive_id: int) -> Optional[PlacementDrive]:
        """Publish a placement drive."""
        db_drive = self.get_by_id(drive_id)
        if not db_drive:
            return None
        db_drive.status = DriveStatus.PUBLISHED
        self.db.commit()
        self.db.refresh(db_drive)
        return db_drive

    def close(self, drive_id: int) -> Optional[PlacementDrive]:
        """Close a placement drive."""
        db_drive = self.get_by_id(drive_id)
        if not db_drive:
            return None
        db_drive.status = DriveStatus.CLOSED
        self.db.commit()
        self.db.refresh(db_drive)
        return db_drive

    def delete(self, drive_id: int) -> bool:
        """Delete placement drive."""
        db_drive = self.get_by_id(drive_id)
        if not db_drive:
            return False
        self.db.delete(db_drive)
        self.db.commit()
        return True

    def is_deadline_passed(self, drive_id: int) -> bool:
        """Check if application deadline has passed."""
        db_drive = self.get_by_id(drive_id)
        if not db_drive:
            return True
        return datetime.utcnow() > db_drive.application_deadline