from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from sqlalchemy import ForeignKey, Sequence, String, Float, text, Integer, Enum
from app.enums.order_items_status import OrderItemStatus


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id: Mapped[str] = mapped_column(String, ForeignKey("orders.id"))
    product_id: Mapped[str] = mapped_column(String, ForeignKey("products.id"))
    item_number: Mapped[str] = mapped_column(
        String(20),
        server_default=text(
            "concat('item#', lpad(nextval('item_number_seq')::text, 5, '0'))"
        ),
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[OrderItemStatus] = mapped_column(
        Enum(OrderItemStatus, name="order_item_status_enum", native_enum=False),
        server_default=text(f"'{OrderItemStatus.PENDING}'"),
    )
    # add : dims, product_relationship , files_id , price ,
    item_price: Mapped[Float] = mapped_column(Float, default=0.0, nullable=True)
    product: Mapped["ProductModel"] = relationship(back_populates="order_items")
    order: Mapped["OrderModel"] = relationship(back_populates="items")

    file: Mapped["UploadedFile"] = relationship(
        "UploadedFile",
        back_populates="order_item",
        uselist=False,
        cascade="all, delete-orphan",
    )
