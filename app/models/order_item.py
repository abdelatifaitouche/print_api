from .base import Base
from sqlalchemy.orm import Mapped , mapped_column , relationship
from uuid import UUID
from sqlalchemy import ForeignKey , Integer , String
from app.enums.order_items_status import OrderItemStatus

class OrderItem(Base):
    __tablename__="order_items"

    order_id : Mapped[str]= mapped_column(String , ForeignKey("orders.id") ) 
    item_name : Mapped[str] = mapped_column(String , nullable=False)
    quantity : Mapped[int] = mapped_column(Integer , nullable=False)
    status : Mapped[str] = mapped_column(String , server_default=OrderItemStatus.PENDING)
    #add : dims, product_relationship , files_id , price ,   
    order : Mapped["OrderModel"] = relationship(back_populates="items")
