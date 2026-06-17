from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.services.company_service import CompanyService
from app.dependencies.auth import get_current_user, get_current_admin
from app.models.user import User
from typing import Dict, Any, List

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def create_company(
    company_in: CompanyCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new company (admin only).
    Requires admin authentication.
    """
    try:
        company_service = CompanyService(db)
        result = company_service.create_company(company_in)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create company")


@router.get("", response_model=Dict[str, Any])
def get_all_companies(
    page: int = 1,
    limit: int = 20,
    active_only: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all companies with pagination.
    Requires authentication.
    """
    company_service = CompanyService(db)
    return company_service.get_all_companies(page=page, limit=limit, active_only=active_only)


@router.get("/{company_id}", response_model=Dict[str, Any])
def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get company by ID.
    Requires authentication.
    """
    company_service = CompanyService(db)
    result = company_service.get_company(company_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return result


@router.put("/{company_id}", response_model=Dict[str, Any])
def update_company(
    company_id: int,
    company_in: CompanyUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update company (admin only).
    Requires admin authentication.
    """
    company_service = CompanyService(db)
    result = company_service.update_company(company_id, company_in)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return result


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Delete company (admin only).
    Requires admin authentication.
    """
    company_service = CompanyService(db)
    result = company_service.delete_company(company_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return None


@router.get("/search/{name}", response_model=List[Dict[str, Any]])
def search_companies(
    name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search companies by name.
    Requires authentication.
    """
    company_service = CompanyService(db)
    return company_service.search_companies(name)