import enum
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class ServiceKind(str, enum.Enum):
    GROUP_TUITION = "GROUP_TUITION"
    ONE_ON_ONE = "ONE_ON_ONE"
    READING_WEEK = "READING_WEEK"
    SUPPLEMENTARY = "SUPPLEMENTARY"

class BillingPeriod(str, enum.Enum):
    MODULE = "MODULE"
    PACKAGE = "PACKAGE"
    WEEK = "WEEK"

class Service(Base):
    __tablename__ = "services"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    kind: Mapped[ServiceKind] = mapped_column(Enum(ServiceKind, name="service_kind"), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    offerings = relationship("ModuleOffering", back_populates="service")

class ModuleOffering(Base):
    __tablename__ = "module_offerings"
    __table_args__ = (UniqueConstraint("module_id","service_id",name="uq_module_service_offering"),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("modules.id"), index=True, nullable=False)
    service_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("services.id"), index=True, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    billing_period: Mapped[BillingPeriod] = mapped_column(Enum(BillingPeriod, name="billing_period"), nullable=False)
    sessions_per_week: Mapped[int | None] = mapped_column(Integer, nullable=True)
    session_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    module = relationship("Module", back_populates="offerings")
    service = relationship("Service", back_populates="offerings")
