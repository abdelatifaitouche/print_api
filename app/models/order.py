from .base import Base
from sqlalchemy import String , Integer
from sqlalchemy.orm import Mapped , mapped_column




class OrderModel(Base):
    __tablename__="orders"

    order_name:Mapped[str] = mapped_column(String , nullable=False)
    order_price:Mapped[int] = mapped_column(Integer , nullable=False)
