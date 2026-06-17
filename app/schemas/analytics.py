from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class AnalyticsOverview(BaseModel):
    total_students: int
    total_companies: int
    total_applications: int
    placement_rate: float
    highest_package: Optional[float] = None
    average_package: Optional[float] = None


class TopHiringCompany(BaseModel):
    company_name: str
    total_hired: int


class BranchPlacementStats(BaseModel):
    branch: str
    total_students: int
    placed_students: int
    placement_percentage: float


class AnalyticsResponse(BaseModel):
    overview: AnalyticsOverview
    top_hiring_companies: List[TopHiringCompany]
    branch_wise_stats: List[BranchPlacementStats]