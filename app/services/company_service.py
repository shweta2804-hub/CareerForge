from sqlalchemy.orm import Session
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.models.company import Company
from typing import Optional, Dict, Any, List


class CompanyService:
    def __init__(self, db: Session):
        self.db = db
        self.company_repo = CompanyRepository(db)

    def create_company(self, company_in: CompanyCreate) -> Dict[str, Any]:
        """Create a new company."""
        existing_company = self.company_repo.get_by_name(company_in.name)
        if existing_company:
            raise ValueError("Company with this name already exists")

        company = self.company_repo.create(company_in)
        return self._format_company_response(company)

    def get_company(self, company_id: int) -> Optional[Dict[str, Any]]:
        """Get company by ID."""
        company = self.company_repo.get_by_id(company_id)
        if not company:
            return None
        return self._format_company_response(company)

    def get_all_companies(self, page: int = 1, limit: int = 20, active_only: bool = True) -> Dict[str, Any]:
        """
        Get all companies with pagination.
        
        Args:
            page: Page number (1-indexed)
            limit: Items per page (max 100)
            active_only: Only return active companies
        
        Returns:
            Dict with items, page, limit, total, pages
        """
        # Validate and sanitize parameters
        page = max(1, page)
        limit = min(max(1, limit), 100)  # Max 100 items per page
        
        # Calculate skip
        skip = (page - 1) * limit
        
        # Get paginated data
        companies = self.company_repo.get_all(skip=skip, limit=limit, active_only=active_only)
        total = self.company_repo.count() if not active_only else self.company_repo.db.query(Company).filter(Company.is_active == True).count()
        
        # Calculate total pages
        pages = (total + limit - 1) // limit  # Ceiling division
        
        return {
            "items": [self._format_company_response(company) for company in companies],
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        }

    def update_company(self, company_id: int, company_in: CompanyUpdate) -> Optional[Dict[str, Any]]:
        """Update company."""
        company = self.company_repo.update(company_id, company_in)
        if not company:
            return None
        return self._format_company_response(company)

    def delete_company(self, company_id: int) -> bool:
        """Delete company."""
        return self.company_repo.delete(company_id)

    def search_companies(self, name: str) -> List[Dict[str, Any]]:
        """Search companies by name."""
        companies = self.company_repo.search_by_name(name)
        return [self._format_company_response(company) for company in companies]

    def _format_company_response(self, company) -> Dict[str, Any]:
        """Format company response."""
        return {
            "id": company.id,
            "name": company.name,
            "package_offered": company.package_offered,
            "location": company.location,
            "minimum_cgpa": company.minimum_cgpa,
            "required_skills": company.required_skills,
            "job_description": company.job_description,
            "is_active": company.is_active,
            "created_at": company.created_at.isoformat() if company.created_at else "",
            "updated_at": company.updated_at.isoformat() if company.updated_at else "",
        }