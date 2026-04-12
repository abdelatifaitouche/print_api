from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.payment_schemas import PaymentCreate
from app.services.payment_service import PaymentService
from app.config.database import get_db
from app.auth.permissions_api import require_permission
from app.enums.permissions import Permissions
from app.auth.permission_context import PermissionContext

payment_endpoints = APIRouter()


def get_service(db: Session = Depends(get_db)):
    return PaymentService(db)


@payment_endpoints.post("/{facture_id}/payment/create/")
def create_payment(
    facture_id: str,
    data: PaymentCreate,
    service: PaymentService = Depends(get_service),
    ctx: PermissionContext = Depends(require_permission(Permissions.CAN_CREATE_ALL)),
):
    return service.create(facture_id, data, ctx)
