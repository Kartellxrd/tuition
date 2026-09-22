from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.api.dependencies import require_tutor
from app.core.database import get_db
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.material import Material
from app.models.module import Module
from app.models.quiz import Quiz, QuizAttempt
from app.models.session import Session, SessionStatus
from app.models.user import User, UserRole

router=APIRouter()

@router.get("/dashboard")
def dashboard(_:User=Depends(require_tutor),db:Session=Depends(get_db)):
    students=db.scalar(select(func.count(User.id)).where(User.role==UserRole.STUDENT,User.active.is_(True))) or 0
    pending=db.scalar(select(func.count(Enrollment.id)).where(Enrollment.status==EnrollmentStatus.PENDING)) or 0
    active=db.scalar(select(func.count(Enrollment.id)).where(Enrollment.status==EnrollmentStatus.ACTIVE)) or 0
    materials=db.scalar(select(func.count(Material.id))) or 0
    quizzes=db.scalar(select(func.count(Quiz.id))) or 0
    attempts=db.scalar(select(func.count(QuizAttempt.id))) or 0
    upcoming=db.scalar(select(func.count(Session.id)).where(Session.status==SessionStatus.SCHEDULED)) or 0
    modules=[{"id":m.id,"code":m.code,"name":m.name,"active":m.active} for m in db.scalars(select(Module).order_by(Module.code))]
    return {"students":students,"pending_enrollments":pending,"active_enrollments":active,"materials":materials,"quizzes":quizzes,"quiz_attempts":attempts,"scheduled_sessions":upcoming,"modules":modules}
