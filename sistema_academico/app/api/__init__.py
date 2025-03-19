# app/api/__init__.py
from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.courses import router as courses_router
from app.api.students import router as students_router
from app.api.sections import router as sections_router
from app.api.enrollments import router as enrollments_router
from app.api.exams import router as exams_router
from app.api.materials import router as materials_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(courses_router, prefix="/courses", tags=["courses"])
api_router.include_router(students_router, prefix="/students", tags=["students"])
api_router.include_router(sections_router, prefix="/sections", tags=["sections"])
api_router.include_router(enrollments_router, prefix="/enrollments", tags=["enrollments"])
api_router.include_router(exams_router, prefix="/exams", tags=["exams"])
api_router.include_router(materials_router, prefix="/materials", tags=["materials"])