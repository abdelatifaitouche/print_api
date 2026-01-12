
from pydantic import BaseModel
from uuid import UUID
from app.enums.order_items_status import OrderItemStatus
from .product_schema import ProductLightRead
from typing import Optional
from .uploadedfile_schema import UploadedFileRead
class OrderItemBase(BaseModel):
    item_name : str
    quantity : int

    model_config = {"from_attributes" : True}


class OrderItemCreate(BaseModel):
    product_id : str
    quantity : int

    model_config = {"from_attributes" : True}



class OrderItemRead(BaseModel):
    id : UUID
    order_id :UUID  
    item_number : str
    item_price : float
    product :ProductLightRead
    status : OrderItemStatus = OrderItemStatus.PENDING
    quantity : int
    file : UploadedFileRead = None
    model_config = {"from_attributes":True}
