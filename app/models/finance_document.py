from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Text, text, String, Float, Enum, ForeignKey
from app.enums.document_type import DocumentType, DocumentStatus
from datetime import datetime


class DocumentModel(Base):
    __tablename__ = "documents"

    document_number: Mapped[str] = mapped_column(
        String(20),
        server_default=text(
            "concat('#', lpad(nextval('document_number_seq')::text, 5, '0'))"
        ),
    )

    document_type: Mapped[DocumentType] = mapped_column(
        Enum(DocumentType, name="document_type_enum", native_enum=False),
        server_default=text(f"'{DocumentType.DEVIS}'"),
    )

    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus, name="document_status_enum", native_enum=False),
        server_default=text(f"'{DocumentStatus.DRAFT}'"),
    )

    total_ht: Mapped[float] = mapped_column(Float)
    total: Mapped[float] = mapped_column(Float)
    total_paid: Mapped[float] = mapped_column(Float, default=0.0)
    total_remaining: Mapped[float] = mapped_column(Float, default=0.0)

    # when a devis is approved and becomes a facture,
    # the facture keeps a reference to the original devis
    devis_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("documents.id"), nullable=True
    )
    devis: Mapped["DocumentModel | None"] = relationship(
        "DocumentModel", remote_side="DocumentModel.id", foreign_keys=[devis_id]
    )

    # order
    order_id: Mapped[str] = mapped_column(String, ForeignKey("orders.id"))
    order: Mapped["OrderModel"] = relationship(
        back_populates="documents", foreign_keys=[order_id]
    )

    # company
    company_id: Mapped[str] = mapped_column(String, ForeignKey("companies.id"))
    company: Mapped["CompanyModel"] = relationship(
        back_populates="documents", foreign_keys=[company_id]
    )

    # created by
    created_by: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    creator: Mapped["User"] = relationship(
        back_populates="created_documents", foreign_keys=[created_by]
    )

    # approved by — nullable, only set when approved
    approved_by: Mapped[str | None] = mapped_column(
        String, ForeignKey("users.id"), nullable=True
    )
    approver: Mapped["User | None"] = relationship(
        back_populates="approved_documents", foreign_keys=[approved_by]
    )

    approved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    payments: Mapped[list["PaymentModel"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )
