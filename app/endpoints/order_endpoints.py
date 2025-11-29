from fastapi import APIRouter
from app.schemas.order_schema import OrderCreate

order_endpoint = APIRouter()





@order_endpoint.get("/")
def list_orders():
    return "orders"



@order_endpoint.post("/" , response_model=OrderCreate)
def create_order(order_data : OrderCreate):
    return order_data

