from pydantic import BaseModel, validator
from app.enums.payment_method import PaymentMethod
from typing import Optional
from datetime import datetime
from app.schemas.user_schema import UserSummary


class PaymentCreate(BaseModel):
    amount: float
    payment_method: PaymentMethod


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_method: Optional[PaymentMethod] = None


class PaymentRead(BaseModel):
    id: str
    amount: float
    payment_method: PaymentMethod
    document_id: str
    creator: UserSummary
    created_at: datetime

    model_config = {"from_attributes": True}


class PaymentSummary(BaseModel):
    id: str
    amount: float
    payment_method: PaymentMethod
    created_at: datetime

    model_config = {"from_attributes": True}
