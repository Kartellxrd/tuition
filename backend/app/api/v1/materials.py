from uuid import UUID
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user, require_tutor
from app.core.database import get_db
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.material import Material, MaterialCategory
from app.models.module import Module
from app.models.user import User
from app.services.storage import delete_course_material, signed_course_material_url, upload_course_material

router = APIRouter()

def active_access(db: Session, user: User, module_id: UUID) -> bool:
    return db.scalar(select(Enrollment.id).where(Enrollment.student_id == user.id, Enrollment.module_id == module_id, Enrollment.status == EnrollmentStatus.ACTIVE)) is not None

@router.get("/module/{module_id}")
def list_materials(module_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role.value != "TUTOR" and not active_access(db, user, module_id):
        raise HTTPException(403, "Active enrollment required.")
    return list(db.scalars(select(Material).where(Material.module_id == module_id).order_by(Material.created_at.desc())))

@router.post("/module/{module_id}")
async def upload_material(module_id: UUID, title: str = Form(..., min_length=2, max_length=180), category: MaterialCategory = Form(...), description: str | None = Form(None), file: UploadFile = File(...), tutor: User = Depends(require_tutor), db: Session = Depends(get_db)):
    module = db.get(Module, module_id)
    if not module:
        raise HTTPException(404, "Module not found.")
    path, original = await upload_course_material(file, str(module_id))
    item = Material(module_id=module_id, title=title.strip(), description=description.strip() if description else None, category=category, storage_path=path, original_filename=original, mime_type=file.content_type or "application/octet-stream", uploaded_by=tutor.id)
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/{material_id}/download")
def download_material(material_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.get(Material, material_id)
    if not item:
        raise HTTPException(404, "Material not found.")
    if user.role.value != "TUTOR" and not active_access(db, user, item.module_id):
        raise HTTPException(403, "Active enrollment required.")
    return {"url": signed_course_material_url(item.storage_path), "expires_in": 300, "filename": item.original_filename}

from pydantic import BaseModel, Field
class MaterialUpdate(BaseModel):
    title: str | None = Field(None, min_length=2, max_length=180)
    description: str | None = None
    category: MaterialCategory | None = None

@router.patch("/{material_id}")
def update_material(material_id: UUID, payload: MaterialUpdate, _: User = Depends(require_tutor), db: Session = Depends(get_db)):
    item=db.get(Material,material_id)
    if not item: raise HTTPException(404,"Material not found.")
    for key,value in payload.model_dump(exclude_unset=True).items():
        setattr(item,key,value.strip() if isinstance(value,str) else value)
    db.commit();db.refresh(item);return item

@router.delete("/{material_id}",status_code=204)
def delete_material(material_id: UUID, _: User = Depends(require_tutor), db: Session = Depends(get_db)):
    item=db.get(Material,material_id)
    if not item: raise HTTPException(404,"Material not found.")
    delete_course_material(item.storage_path)
    db.delete(item);db.commit()
