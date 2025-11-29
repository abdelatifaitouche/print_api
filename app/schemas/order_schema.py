from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from .order_item_schema import OrderItemRead
from typing import List
class OrderRead(BaseModel):
    id : UUID
    order_name : str
    order_price: int
    created_at : datetime
    updated_at : datetime
    items : List[OrderItemRead]
    model_config = {
            "from_attributes" : True
            }

class OrderCreate(BaseModel): 
    order_name : str
    order_price : int
