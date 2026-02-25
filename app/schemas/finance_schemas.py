from pydantic import BaseModel
from app.enums.document_type import DocumentStatus, DocumentType
from typing import Optional
from datetime import datetime
from app.schemas.payment_schemas import PaymentSummary
from app.schemas.user_schema import UserSummary
from app.schemas.company_schema import CompanySummary
from app.schemas.order_schema import OrderSummary


class DocumentCreate(BaseModel):
    document_type: DocumentType = DocumentType.DEVIS
    order_id: str
    company_id: str


class DocumentUpdate(BaseModel):
    total_ht: Optional[float] = None
    total: Optional[float] = None
    status: Optional[DocumentStatus] = None
    # total_paid and total_remaining intentionally excluded
    # document_type, order_id, company_id intentionally excluded


class DocumentApprove(BaseModel):
    # approver is taken from authenticated user
    # no client fields needed
    pass


class DocumentRead(BaseModel):
    id: str
    document_number: str
    document_type: DocumentType
    status: DocumentStatus

    total_ht: float
    total: float
    total_paid: float
    total_remaining: float

    order: OrderSummary
    company: CompanySummary
    creator: UserSummary

    approver: Optional[UserSummary] = None
    approved_at: Optional[datetime] = None

    devis_id: Optional[str] = None

    payments: list[PaymentSummary] = []

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentSummary(BaseModel):
    id: str
    document_number: str
    document_type: DocumentType
    status: DocumentStatus
    total: float
    total_ht: float
    total_paid: float
    total_remaining: float
    company_id: str
    created_at: datetime

    class Config:
        from_attributes = True
