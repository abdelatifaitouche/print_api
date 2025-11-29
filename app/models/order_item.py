from .base import Base
from sqlalchemy.orm import Mapped , mapped_column , relationship
from uuid import UUID
from sqlalchemy import ForeignKey , Integer , String


class OrderItem(Base):
    __tablename__="order_items"

    order_id : Mapped[str]= mapped_column(String , ForeignKey("orders.id") ) 
    item_name : Mapped[str] = mapped_column(String , nullable=False)
    quantity : Mapped[int] = mapped_column(Integer , nullable=False)
    

    order : Mapped["OrderModel"] = relationship(back_populates="items")
