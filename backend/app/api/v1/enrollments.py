from datetime import datetime, timezone
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
from app.api.dependencies import get_current_user, require_tutor
from app.core.database import get_db
from app.models.enrollment import Enrollment, EnrollmentStatus, EnrollmentTier
from app.models.module import Module
from app.models.user import User
from app.schemas.enrollment import EnrollmentResponse, RejectEnrollmentRequest
from app.services.storage import signed_payment_proof_url, upload_payment_proof

router = APIRouter()

def serialize(e: Enrollment) -> EnrollmentResponse:
    return EnrollmentResponse(id=e.id, student_id=e.student_id, module_id=e.module_id, tier=e.tier, status=e.status, expected_price=e.expected_price, payment_reference=e.payment_reference, proof_of_payment_storage_path=e.proof_of_payment_storage_path, rejection_reason=e.rejection_reason, reviewed_at=e.reviewed_at, reviewed_by=e.reviewed_by, created_at=e.created_at)

@router.post("", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def create_enrollment(module_id: UUID = Form(...), tier: EnrollmentTier = Form(...), payment_reference: str = Form(..., min_length=2, max_length=120), proof: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.email_verified:
        raise HTTPException(status_code=403, detail="Verify your email before enrolling.")
    module = db.get(Module, module_id)
    if not module or not module.active:
        raise HTTPException(status_code=404, detail="Module not found.")
    existing = db.scalar(select(Enrollment).where(Enrollment.student_id == user.id, Enrollment.module_id == module.id, Enrollment.status.in_([EnrollmentStatus.PENDING, EnrollmentStatus.ACTIVE])))
    if existing:
        raise HTTPException(status_code=409, detail="You already have a pending or active enrollment for this module.")
    price = module.group_price if tier == EnrollmentTier.GROUP else module.one_on_one_price
    storage_path = await upload_payment_proof(proof, str(user.id))
    enrollment = Enrollment(student_id=user.id, module_id=module.id, tier=tier, status=EnrollmentStatus.PENDING, expected_price=price, payment_reference=payment_reference.strip(), proof_of_payment_storage_path=storage_path)
    db.add(enrollment); db.commit(); db.refresh(enrollment)
    return serialize(enrollment)

@router.get("/me", response_model=list[EnrollmentResponse])
def my_enrollments(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return [serialize(e) for e in db.scalars(select(Enrollment).where(Enrollment.student_id == user.id).order_by(Enrollment.created_at.desc()))]

@router.get("/admin/pending", response_model=list[EnrollmentResponse])
def pending(_: User = Depends(require_tutor), db: Session = Depends(get_db)):
    return [serialize(e) for e in db.scalars(select(Enrollment).where(Enrollment.status == EnrollmentStatus.PENDING).order_by(Enrollment.created_at.asc()))]

@router.get("/admin/{enrollment_id}/proof-url")
def proof_url(enrollment_id: UUID, _: User = Depends(require_tutor), db: Session = Depends(get_db)):
    e = db.get(Enrollment, enrollment_id)
    if not e or not e.proof_of_payment_storage_path:
        raise HTTPException(status_code=404, detail="Payment proof not found.")
    return {"url": signed_payment_proof_url(e.proof_of_payment_storage_path), "expires_in": 300}

@router.post("/admin/{enrollment_id}/approve", response_model=EnrollmentResponse)
def approve(enrollment_id: UUID, tutor: User = Depends(require_tutor), db: Session = Depends(get_db)):
    e = db.get(Enrollment, enrollment_id)
    if not e: raise HTTPException(status_code=404, detail="Enrollment not found.")
    if e.status != EnrollmentStatus.PENDING: raise HTTPException(status_code=409, detail="Only pending enrollments can be approved.")
    e.status = EnrollmentStatus.ACTIVE; e.reviewed_by = tutor.id; e.reviewed_at = datetime.now(timezone.utc); e.rejection_reason = None
    db.commit(); db.refresh(e); return serialize(e)

@router.post("/admin/{enrollment_id}/reject", response_model=EnrollmentResponse)
def reject(enrollment_id: UUID, payload: RejectEnrollmentRequest, tutor: User = Depends(require_tutor), db: Session = Depends(get_db)):
    e = db.get(Enrollment, enrollment_id)
    if not e: raise HTTPException(status_code=404, detail="Enrollment not found.")
    if e.status != EnrollmentStatus.PENDING: raise HTTPException(status_code=409, detail="Only pending enrollments can be rejected.")
    e.status = EnrollmentStatus.REJECTED; e.rejection_reason = payload.reason.strip(); e.reviewed_by = tutor.id; e.reviewed_at = datetime.now(timezone.utc)
    db.commit(); db.refresh(e); return serialize(e)
