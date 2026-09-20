from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.enrollment import EnrollmentStatus, EnrollmentTier

class EnrollmentCreate(BaseModel):
    module_id: UUID
    tier: EnrollmentTier
    payment_reference: str = Field(min_length=2, max_length=120)
    proof_of_payment_storage_path: str = Field(min_length=1, max_length=500)

class EnrollmentResponse(BaseModel):
    id: UUID
    student_id: UUID
    module_id: UUID
    tier: EnrollmentTier
    status: EnrollmentStatus
    expected_price: Decimal
    payment_reference: str | None
    rejection_reason: str | None
    reviewed_at: datetime | None
    reviewed_by: UUID | None
    created_at: datetime

class RejectEnrollmentRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=1000)
