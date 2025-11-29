
from pydantic import BaseModel
from uuid import UUID



class OrderItemRead(BaseModel):
    id : UUID
    order_id : UUID
    item_name : str
    quantity : int
    model_config = {"from_attributes":True}
