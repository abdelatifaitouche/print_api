from .base import Base
from sqlalchemy import String, Integer, ForeignKey, Sequence, text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.enums.order_enums import OrderStatus


class OrderModel(Base):
    __tablename__ = "orders"
    order_number: Mapped[str] = mapped_column(
        String(20),
        server_default=text(
            "concat('ORD#', lpad(nextval('order_number_seq')::text, 5, '0'))"
        ),
    )
    status: Mapped[str] = mapped_column(
        String, server_default=OrderStatus.PENDING.value
    )
    order_price: Mapped[Float] = mapped_column(Float, nullable=True)
    created_by: Mapped[str] = mapped_column(
        String, ForeignKey("users.id"), nullable=True
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
