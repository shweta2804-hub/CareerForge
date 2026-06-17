from fastapi import APIRouter
from app.api.v1.endpoints import auth, students, companies, placement_drives, applications, assessments, analytics

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(students.router)
api_router.include_router(companies.router)
api_router.include_router(placement_drives.router)
api_router.include_router(applications.router)
api_router.include_router(assessments.router)
api_router.include_router(analytics.router)