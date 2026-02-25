from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Float, Enum
from .base import Base
from app.enums.payment_method import PaymentMethod


class PaymentModel(Base):
    __tablename__ = "payments"

    amount: Mapped[float] = mapped_column(Float, nullable=False)

    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod, name="payment_method_enum", native_enum=False),
        nullable=False,
    )

    document_id: Mapped[str] = mapped_column(
        String, ForeignKey("documents.id"), nullable=False
    )
    document: Mapped["DocumentModel"] = relationship(back_populates="payments")

    created_by: Mapped[str] = mapped_column(
        String, ForeignKey("users.id"), nullable=False
    )
    creator: Mapped["User"] = relationship(
        back_populates="created_payments", foreign_keys=[created_by]
    )
