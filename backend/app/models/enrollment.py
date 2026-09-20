import enum
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class EnrollmentTier(str, enum.Enum):
    GROUP = "GROUP"
    ONE_ON_ONE = "ONE_ON_ONE"

class EnrollmentStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"

class Enrollment(Base):
    __tablename__ = "enrollments"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)
    module_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("modules.id"), index=True, nullable=False)
    tier: Mapped[EnrollmentTier] = mapped_column(Enum(EnrollmentTier, name="enrollment_tier"), nullable=False)
    status: Mapped[EnrollmentStatus] = mapped_column(Enum(EnrollmentStatus, name="enrollment_status"), default=EnrollmentStatus.PENDING, index=True, nullable=False)
    expected_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payment_reference: Mapped[str | None] = mapped_column(String(120), nullable=True)
    proof_of_payment_storage_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    student = relationship("User", foreign_keys=[student_id], back_populates="enrollments")
    module = relationship("Module", back_populates="enrollments")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
