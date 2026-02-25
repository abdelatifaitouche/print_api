from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from .order_item_schema import OrderItemRead, OrderItemCreate, OrderItemBase
from typing import List
from app.enums.order_enums import OrderStatus
from app.schemas.user_schema import User, CompanyBase


class OrderRead(BaseModel):
    id: UUID
    order_number: str
    order_price: float | None = None
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    company_id: UUID | None = None
    creator: User | None = None
    company: CompanyBase | None = None
    items: List[OrderItemRead]
    model_config = {"from_attributes": True}


class OrderUpdate(BaseModel):
    status: str


class OrderCreate(BaseModel):
    status: OrderStatus = OrderStatus.PENDING
    items: List[OrderItemCreate]
    model_config = {"from_attributes": True}


class OrderSummary(BaseModel):
    id: str
    order_number: str
    status: str

    model_config = {"from_attributes": True}
