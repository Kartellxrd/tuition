from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.models.module import Module
from app.schemas.module import ModuleResponse

router = APIRouter()

@router.get("", response_model=list[ModuleResponse])
def list_modules(db: Session = Depends(get_db)):
    return list(db.scalars(select(Module).where(Module.active.is_(True)).order_by(Module.code)))

@router.get("/{module_id}", response_model=ModuleResponse)
def get_module(module_id: UUID, db: Session = Depends(get_db)):
    module = db.get(Module, module_id)
    if not module or not module.active:
        raise HTTPException(status_code=404, detail="Module not found.")
    return module
