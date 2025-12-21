from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from .order_item_schema import OrderItemRead,OrderItemCreate , OrderItemBase
from typing import List
from app.enums.order_enums import OrderStatus


class OrderRead(BaseModel):
    id : UUID
    order_name : str
    order_price: int
    status : OrderStatus = OrderStatus.PENDING
    created_at : datetime
    updated_at : datetime
    created_by : UUID
    items : List[OrderItemRead]
    model_config = {
            "from_attributes" : True
            }

class OrderCreate(BaseModel): 
    order_name : str
    order_price : int
    items : List[OrderItemBase]
    model_config = {"from_attributes" : True}
