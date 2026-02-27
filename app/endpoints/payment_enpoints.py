"""
SIMPLE LOGIC FOR THIS WORKFLOW:

    - once the order is created, a quote is generated (quote and facture are the same document that only its states changes )

    - if the quote is accepted, it turns to a facture,
    - the facture has all the data related to an order + montant total ,  montant_payé , montant_restant,
    - si le montant restant == 0 ,  alors la facture est payé => Order payé => items payé

    - pour effectuer un payment et garder une tracabilité, on crée un objet payment(facture_id , montant_total , type de paiment : ccp , cash , cheque + dates) ;

    - on ne peut pas payé une facture (un devis) non accepté, on ne peut pas payé une facture deja payéstatus == payé ,

    - on doit pouvoir voir la totalité des dettes d'un client cumulé, et sur different facture


"""

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
