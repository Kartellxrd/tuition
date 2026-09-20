from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.modules import router as modules_router
from app.api.v1.enrollments import router as enrollments_router
from app.api.v1.announcements import router as announcements_router
api_router=APIRouter()
api_router.include_router(health_router,prefix="/health",tags=["Health"])
api_router.include_router(auth_router,prefix="/auth",tags=["Authentication"])
api_router.include_router(modules_router,prefix="/modules",tags=["Modules"])
api_router.include_router(enrollments_router,prefix="/enrollments",tags=["Enrollments"])
api_router.include_router(announcements_router,prefix="/announcements",tags=["Announcements"])
