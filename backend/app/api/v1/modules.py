from decimal import Decimal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import require_tutor
from app.core.database import get_db
from app.models.module import Module
from app.models.user import User
from app.schemas.module import ModuleResponse
router=APIRouter()
class ModuleAdminUpdate(BaseModel):
    name:str|None=Field(None,min_length=2,max_length=160); description:str|None=None
    group_price:Decimal|None=Field(None,gt=0); one_on_one_price:Decimal|None=Field(None,gt=0); active:bool|None=None

@router.get("/admin/all",response_model=list[ModuleResponse])
def admin_modules(_:User=Depends(require_tutor),db:Session=Depends(get_db)): return list(db.scalars(select(Module).order_by(Module.code)))

@router.patch("/admin/{module_id}",response_model=ModuleResponse)
def update_module(module_id:UUID,payload:ModuleAdminUpdate,_:User=Depends(require_tutor),db:Session=Depends(get_db)):
    module=db.get(Module,module_id)
    if not module: raise HTTPException(404,"Module not found.")
    for key,value in payload.model_dump(exclude_unset=True).items(): setattr(module,key,value.strip() if isinstance(value,str) else value)
    db.commit();db.refresh(module);return module

@router.get("",response_model=list[ModuleResponse])
def list_modules(db:Session=Depends(get_db)): return list(db.scalars(select(Module).where(Module.active.is_(True)).order_by(Module.code)))

@router.get("/{module_id}",response_model=ModuleResponse)
def get_module(module_id:UUID,db:Session=Depends(get_db)):
    module=db.get(Module,module_id)
    if not module or not module.active: raise HTTPException(404,"Module not found.")
    return module
