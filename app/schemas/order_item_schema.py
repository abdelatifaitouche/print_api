
from pydantic import BaseModel
from uuid import UUID


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
    quantity : int
    model_config = {"from_attributes":True}
