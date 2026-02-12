from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from .order_item_schema import OrderItemRead, OrderItemCreate, OrderItemBase
from typing import List
from app.enums.order_enums import OrderStatus
from app.schemas.user_schema import User


class OrderRead(BaseModel):
    id: UUID
    order_number: str
    order_price: float | None = None
    status: str
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    items: List[OrderItemRead]
    model_config = {"from_attributes": True}


class OrderUpdate(BaseModel):
    status: str


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    model_config = {"from_attributes": True}
