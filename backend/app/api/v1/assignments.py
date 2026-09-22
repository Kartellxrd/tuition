from datetime import datetime
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user,require_tutor
from app.core.database import get_db
from app.models.assignment import Assignment,AssignmentStatus,AssignmentSubmission
from app.models.enrollment import Enrollment,EnrollmentStatus
from app.models.module import Module
from app.models.user import User

router=APIRouter()

class AssignmentCreate(BaseModel):
    module_id:UUID
    title:str=Field(min_length=2,max_length=180)
    instructions:str|None=None
    due_at:datetime|None=None

@router.post("/admin")
def create_assignment(payload:AssignmentCreate,tutor:User=Depends(require_tutor),db:Session=Depends(get_db)):
    if not db.get(Module,payload.module_id): raise HTTPException(404,"Module not found.")
    item=Assignment(**payload.model_dump(),created_by=tutor.id)
    db.add(item);db.commit();db.refresh(item);return item

@router.post("/admin/{assignment_id}/publish")
def publish(assignment_id:UUID,_:User=Depends(require_tutor),db:Session=Depends(get_db)):
    item=db.get(Assignment,assignment_id)
    if not item: raise HTTPException(404,"Assignment not found.")
    item.status=AssignmentStatus.PUBLISHED;db.commit();return {"id":item.id,"status":item.status}

@router.get("/me/todo")
def my_todo(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    active_modules=select(Enrollment.module_id).where(Enrollment.student_id==user.id,Enrollment.status==EnrollmentStatus.ACTIVE)
    submitted=select(AssignmentSubmission.id).where(AssignmentSubmission.assignment_id==Assignment.id,AssignmentSubmission.student_id==user.id).exists()
    rows=db.execute(select(Assignment,Module.code,Module.name).join(Module,Module.id==Assignment.module_id).where(Assignment.status==AssignmentStatus.PUBLISHED,Assignment.module_id.in_(active_modules),~submitted).order_by(Assignment.due_at.asc().nullslast(),Assignment.created_at.desc())).all()
    return [{"id":a.id,"type":"ASSIGNMENT","module_id":a.module_id,"module_code":code,"module_name":name,"title":a.title,"instructions":a.instructions,"due_at":a.due_at} for a,code,name in rows]
