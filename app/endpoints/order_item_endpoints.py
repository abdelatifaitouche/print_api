from fastapi import APIRouter
from app.services.order_item_service import OrderItemService
from app.schemas.order_item_schema import OrderItemCreate,OrderItemRead
from app.config.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


order_item_endpoints = APIRouter()
order_item_service = OrderItemService()


@order_item_endpoints.get("/")
def index():
    return "hello order item"



@order_item_endpoints.post("/" , response_model=OrderItemRead)
def create_order_item(order_item_data : OrderItemRead , db : Session = Depends(get_db))->OrderItemRead:
    order = order_item_service.create(order_item_data , db)
    return order
