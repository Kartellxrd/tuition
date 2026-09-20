from datetime import datetime, timezone
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import or_, select
from sqlalchemy.orm import Session as DBSession
from app.api.dependencies import get_current_user, require_tutor
from app.core.database import get_db
from app.models.enrollment import Enrollment, EnrollmentStatus, EnrollmentTier
from app.models.session import Session, SessionMode, SessionStatus
from app.models.user import User
router=APIRouter()
class SessionCreate(BaseModel):
    module_id:UUID; tier:EnrollmentTier; enrollment_id:UUID|None=None; title:str=Field(min_length=2,max_length=180); notes:str|None=None; start_at:datetime; end_at:datetime; mode:SessionMode; location:str|None=None; meeting_link:str|None=None
    @model_validator(mode="after")
    def validate_session(self):
        if self.end_at<=self.start_at: raise ValueError("end_at must be after start_at")
        if self.tier==EnrollmentTier.ONE_ON_ONE and not self.enrollment_id: raise ValueError("One-on-one sessions require an enrollment.")
        if self.tier==EnrollmentTier.GROUP and self.enrollment_id: raise ValueError("Group sessions cannot target one enrollment.")
        return self
@router.post("")
def create_session(payload:SessionCreate,tutor:User=Depends(require_tutor),db:DBSession=Depends(get_db)):
    if payload.tier==EnrollmentTier.ONE_ON_ONE:
        e=db.get(Enrollment,payload.enrollment_id)
        if not e or e.status!=EnrollmentStatus.ACTIVE or e.module_id!=payload.module_id or e.tier!=EnrollmentTier.ONE_ON_ONE: raise HTTPException(400,"A matching active one-on-one enrollment is required.")
    item=Session(**payload.model_dump(),created_by=tutor.id);db.add(item);db.commit();db.refresh(item);return item
@router.get("/me/upcoming")
def upcoming(user:User=Depends(get_current_user),db:DBSession=Depends(get_db)):
    active=list(db.scalars(select(Enrollment).where(Enrollment.student_id==user.id,Enrollment.status==EnrollmentStatus.ACTIVE)))
    if not active:return []
    group_modules=[e.module_id for e in active if e.tier==EnrollmentTier.GROUP]; private_ids=[e.id for e in active if e.tier==EnrollmentTier.ONE_ON_ONE]
    conditions=[]
    if group_modules: conditions.append((Session.tier==EnrollmentTier.GROUP)&Session.module_id.in_(group_modules))
    if private_ids: conditions.append((Session.tier==EnrollmentTier.ONE_ON_ONE)&Session.enrollment_id.in_(private_ids))
    if not conditions:return []
    return list(db.scalars(select(Session).where(or_(*conditions),Session.status==SessionStatus.SCHEDULED,Session.start_at>=datetime.now(timezone.utc)).order_by(Session.start_at)))
