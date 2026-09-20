from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user, require_tutor
from app.core.database import get_db
from app.models.announcement import Announcement
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.user import User
router=APIRouter()
class AnnouncementCreate(BaseModel):
    title:str=Field(min_length=2,max_length=180); message:str=Field(min_length=2,max_length=5000); important:bool=False

def active_access(db,user,module_id):
    return db.scalar(select(Enrollment.id).where(Enrollment.student_id==user.id,Enrollment.module_id==module_id,Enrollment.status==EnrollmentStatus.ACTIVE)) is not None
@router.get("/{module_id}")
def list_announcements(module_id:UUID,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if user.role.value!="TUTOR" and not active_access(db,user,module_id): raise HTTPException(403,"Active enrollment required.")
    return list(db.scalars(select(Announcement).where(Announcement.module_id==module_id).order_by(Announcement.important.desc(),Announcement.created_at.desc())))
@router.post("/{module_id}")
def create_announcement(module_id:UUID,payload:AnnouncementCreate,tutor:User=Depends(require_tutor),db:Session=Depends(get_db)):
    item=Announcement(module_id=module_id,title=payload.title.strip(),message=payload.message.strip(),important=payload.important,created_by=tutor.id);db.add(item);db.commit();db.refresh(item);return item
