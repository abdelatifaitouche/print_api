from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.order_item_service import OrderItemService
from app.config.database import get_db
from app.schemas.order_item_schema import OrderItemUpdate

order_items_endpoints = APIRouter()


def get_service(db: Session = Depends(get_db)):
    return OrderItemService(db)


@order_items_endpoints.post("")
def create_item():
    return


def list_items():
    return


@order_items_endpoints.get("/{item_id}")
def get_item_by_id(item_id: str, service: OrderItemService = Depends(get_service)):
    return service.get_by_id(item_id)


def delete_item():
    return


@order_items_endpoints.patch("/{item_id}")
def update_item(
    item_id: str,
    data: OrderItemUpdate,
    service: OrderItemService = Depends(get_service),
):
    updated = service.update(item_id, data)

    return updated
