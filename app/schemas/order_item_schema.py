
from pydantic import BaseModel
from uuid import UUID
from app.enums.order_items_status import OrderItemStatus


class OrderItemBase(BaseModel):
    item_name : str
    quantity : int

    model_config = {"from_attributes" : True}


class OrderItemCreate(BaseModel):
    order_id : str
    item_name : str
    quantity : int

    model_config = {"from_attributes" : True}



class OrderItemRead(BaseModel):
    id : UUID
    order_id :str
    item_name : str
    status : OrderItemStatus = OrderItemStatus.PENDING
    quantity : int
    model_config = {"from_attributes":True}
