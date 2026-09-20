from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.modules import router as modules_router
from app.api.v1.enrollments import router as enrollments_router
from app.api.v1.announcements import router as announcements_router
from app.api.v1.sessions import router as sessions_router
from app.api.v1.quizzes import router as quizzes_router
from app.api.v1.materials import router as materials_router
from app.api.v1.admin import router as admin_router
api_router=APIRouter()
api_router.include_router(health_router,prefix="/health",tags=["Health"])
api_router.include_router(auth_router,prefix="/auth",tags=["Authentication"])
api_router.include_router(modules_router,prefix="/modules",tags=["Modules"])
api_router.include_router(enrollments_router,prefix="/enrollments",tags=["Enrollments"])
api_router.include_router(announcements_router,prefix="/announcements",tags=["Announcements"])

api_router.include_router(sessions_router,prefix="/sessions",tags=["Sessions"])

api_router.include_router(quizzes_router,prefix="/quizzes",tags=["Quizzes"])

api_router.include_router(materials_router,prefix="/materials",tags=["Materials"])

api_router.include_router(admin_router,prefix="/admin",tags=["Tutor Admin"])
