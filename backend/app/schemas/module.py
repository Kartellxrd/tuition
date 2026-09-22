from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class ModuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    code: str
    name: str
    description: str | None
    group_price: Decimal
    one_on_one_price: Decimal
    active: bool
