from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.module import Module
from app.models.service import ModuleOffering, Service
from app.schemas.offering import OfferingResponse

router=APIRouter()

def serialize(o:ModuleOffering)->OfferingResponse:
    return OfferingResponse(id=o.id,service_id=o.service_id,service_code=o.service.code,service_name=o.service.name,kind=o.service.kind,description=o.service.description,price=o.price,billing_period=o.billing_period,sessions_per_week=o.sessions_per_week,session_minutes=o.session_minutes,active=o.active)

@router.get("/module/{module_id}",response_model=list[OfferingResponse])
def module_offerings(module_id:UUID,db:Session=Depends(get_db)):
    module=db.get(Module,module_id)
    if not module or not module.active: raise HTTPException(404,"Module not found.")
    q=select(ModuleOffering).join(Service).where(ModuleOffering.module_id==module_id,ModuleOffering.active.is_(True),Service.active.is_(True)).order_by(Service.name)
    return [serialize(x) for x in db.scalars(q)]
