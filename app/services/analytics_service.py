from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.student import Student
from app.models.company import Company
from app.models.application import Application, ApplicationStatus
from app.models.assessment import AssessmentScore
from typing import Dict, Any, List


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_overview_analytics(self) -> Dict[str, Any]:
        """Get overview analytics."""
        total_students = self.db.query(Student).count()
        total_companies = self.db.query(Company).count()
        total_applications = self.db.query(Application).count()

        # Placement rate
        selected_applications = self.db.query(Application).filter(
            Application.status == ApplicationStatus.SELECTED
        ).count()
        placement_rate = (selected_applications / total_applications * 100) if total_applications > 0 else 0

        # Package statistics
        companies_with_package = self.db.query(Company).filter(Company.package_offered.isnot(None)).all()
        packages = [c.package_offered for c in companies_with_package if c.package_offered]
        
        highest_package = max(packages) if packages else None
        average_package = sum(packages) / len(packages) if packages else None

        return {
            "total_students": total_students,
            "total_companies": total_companies,
            "total_applications": total_applications,
            "placement_rate": round(placement_rate, 2),
            "highest_package": highest_package,
            "average_package": round(average_package, 2) if average_package else None,
        }

    def get_top_hiring_companies(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top hiring companies based on selected candidates."""
        from app.repositories.company_repository import CompanyRepository
        company_repo = CompanyRepository(self.db)
        
        # Get all companies
        companies = company_repo.get_all(limit=1000, active_only=False)
        
        top_companies = []
        for company in companies:
            selected_count = self.db.query(Application).filter(
                Application.status == ApplicationStatus.SELECTED
            ).count()
            
            if selected_count > 0:
                top_companies.append({
                    "company_name": company.name,
                    "total_hired": selected_count,
                })
        
        # Sort by total hired
        top_companies.sort(key=lambda x: x["total_hired"], reverse=True)
        return top_companies[:limit]

    def get_branch_wise_stats(self) -> List[Dict[str, Any]]:
        """Get branch-wise placement statistics."""
        # Get all students grouped by branch
        students = self.db.query(Student).all()
        
        branch_stats = {}
        for student in students:
            branch = student.branch
            if branch not in branch_stats:
                branch_stats[branch] = {
                    "branch": branch,
                    "total_students": 0,
                    "placed_students": 0,
                }
            branch_stats[branch]["total_students"] += 1

        # Count placed students per branch
        placed_applications = self.db.query(Application).filter(
            Application.status == ApplicationStatus.SELECTED
        ).all()
        
        for app in placed_applications:
            student = self.db.query(Student).filter(Student.id == app.student_id).first()
            if student:
                branch = student.branch
                if branch in branch_stats:
                    branch_stats[branch]["placed_students"] += 1

        # Calculate percentages
        result = []
        for stats in branch_stats.values():
            placement_percentage = (
                (stats["placed_students"] / stats["total_students"] * 100)
                if stats["total_students"] > 0
                else 0
            )
            result.append({
                "branch": stats["branch"],
                "total_students": stats["total_students"],
                "placed_students": stats["placed_students"],
                "placement_percentage": round(placement_percentage, 2),
            })

        return result

    def get_full_analytics(self) -> Dict[str, Any]:
        """Get complete analytics report."""
        overview = self.get_overview_analytics()
        top_companies = self.get_top_hiring_companies()
        branch_stats = self.get_branch_wise_stats()

        return {
            "overview": overview,
            "top_hiring_companies": top_companies,
            "branch_wise_stats": branch_stats,
        }