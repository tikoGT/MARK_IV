# app/api/__init__.py
from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.courses import router as courses_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(courses_router, prefix="/courses", tags=["courses"])