from fastapi import APIRouter
from app.schemas.order_schema import OrderCreate , OrderRead
from app.config.database import get_db
from fastapi import Depends
from app.services.order_service import OrderService
from sqlalchemy.orm import Session
from typing import List
from app.utils.private_route import PrivateRoute

order_endpoint = APIRouter(
    dependencies = [Depends(PrivateRoute()),]
)
order_service = OrderService()




@order_endpoint.get("/" , response_model=List[OrderRead])
def list_orders(db : Session= Depends(get_db)):
    orders = order_service.list(db)
    return orders


@order_endpoint.get("/{order_id}" , response_model=OrderRead)
def get_order_by_id(order_id : str , db : Session = Depends(get_db)):
    order = order_service.get_by_id(db , order_id)
    return order




@order_endpoint.post("/" , response_model=OrderRead)
def create_order(order_data : OrderCreate , db:Session = Depends(get_db)) -> OrderRead:
    order = order_service.create(db , order_data)
    return order

