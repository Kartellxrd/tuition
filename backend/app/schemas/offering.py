from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel
from app.models.service import BillingPeriod, ServiceKind

class OfferingResponse(BaseModel):
    id: UUID
    service_id: UUID
    service_code: str
    service_name: str
    kind: ServiceKind
    description: str | None
    price: Decimal
    billing_period: BillingPeriod
    sessions_per_week: int | None
    session_minutes: int | None
    active: bool
