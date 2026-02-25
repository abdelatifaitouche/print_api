from pydantic import BaseModel, validator
from app.enums.payment_method import PaymentMethod
from typing import Optional
from datetime import datetime
from app.schemas.user_schema import UserSummary


class PaymentCreate(BaseModel):
    amount: float
    payment_method: PaymentMethod
    document_id: str

    @validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Payment amount must be positive")
        return v


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_method: Optional[PaymentMethod] = None

    @validator("amount")
    def amount_must_be_positive(cls, v):
        if v and v <= 0:
            raise ValueError("Payment amount must be positive")
        return v


class PaymentRead(BaseModel):
    id: str
    amount: float
    payment_method: PaymentMethod
    document_id: str
    creator: UserSummary
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentSummary(BaseModel):
    id: str
    amount: float
    payment_method: PaymentMethod
    created_at: datetime

    class Config:
        from_attributes = True
