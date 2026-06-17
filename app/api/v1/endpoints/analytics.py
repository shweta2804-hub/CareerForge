from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.analytics_service import AnalyticsService
from app.dependencies.auth import get_current_user, get_current_admin
from app.models.user import User
from typing import Dict, Any, List

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview", response_model=Dict[str, Any])
def get_overview_analytics(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get overview analytics (admin only).
    Requires admin authentication.
    """
    analytics_service = AnalyticsService(db)
    return analytics_service.get_overview_analytics()


@router.get("/top-companies", response_model=List[Dict[str, Any]])
def get_top_hiring_companies(
    limit: int = 10,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get top hiring companies (admin only).
    Requires admin authentication.
    """
    analytics_service = AnalyticsService(db)
    return analytics_service.get_top_hiring_companies(limit=limit)


@router.get("/branch-stats", response_model=List[Dict[str, Any]])
def get_branch_wise_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get branch-wise placement statistics (admin only).
    Requires admin authentication.
    """
    analytics_service = AnalyticsService(db)
    return analytics_service.get_branch_wise_stats()


@router.get("/full-report", response_model=Dict[str, Any])
def get_full_analytics_report(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get complete analytics report (admin only).
    Requires admin authentication.
    """
    analytics_service = AnalyticsService(db)
    return analytics_service.get_full_analytics()