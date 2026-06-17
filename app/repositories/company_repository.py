from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from typing import Optional, List


class CompanyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Company]:
        """Get company by ID."""
        return self.db.query(Company).filter(Company.id == id).first()

    def get_by_name(self, name: str) -> Optional[Company]:
        """Get company by name."""
        return self.db.query(Company).filter(Company.name == name).first()

    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Company]:
        """Get all companies with pagination."""
        query = self.db.query(Company)
        if active_only:
            query = query.filter(Company.is_active == True)
        return query.offset(skip).limit(limit).all()

    def create(self, company_in: CompanyCreate) -> Company:
        """Create a new company."""
        db_company = Company(
            name=company_in.name,
            package_offered=company_in.package_offered,
            location=company_in.location,
            minimum_cgpa=company_in.minimum_cgpa,
            required_skills=company_in.required_skills,
            job_description=company_in.job_description,
        )
        self.db.add(db_company)
        self.db.commit()
        self.db.refresh(db_company)
        return db_company

    def update(self, company_id: int, company_in: CompanyUpdate) -> Optional[Company]:
        """Update company."""
        db_company = self.get_by_id(company_id)
        if not db_company:
            return None
        update_data = company_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_company, field, value)
        self.db.commit()
        self.db.refresh(db_company)
        return db_company

    def delete(self, company_id: int) -> bool:
        """Delete company."""
        db_company = self.get_by_id(company_id)
        if not db_company:
            return False
        self.db.delete(db_company)
        self.db.commit()
        return True

    def search_by_name(self, name: str) -> List[Company]:
        """Search companies by name."""
        return self.db.query(Company).filter(Company.name.ilike(f"%{name}%")).all()