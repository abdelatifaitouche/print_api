from .base import Base
from sqlalchemy.orm import Mapped , mapped_column , relationship
from uuid import UUID
from sqlalchemy import ForeignKey , Sequence , String , Float , text , Integer
from app.enums.order_items_status import OrderItemStatus

class OrderItem(Base):
    __tablename__="order_items"

    order_id : Mapped[str]= mapped_column(String , ForeignKey("orders.id") ) 
    product_id : Mapped[str] = mapped_column(String , ForeignKey("products.id"))
    item_number: Mapped[str] = mapped_column(
         String(20),
         server_default=text("concat('item#', lpad(nextval('item_number_seq')::text, 5, '0'))")
     )
    quantity : Mapped[int] = mapped_column(Integer , nullable=False)
    status : Mapped[str] = mapped_column(String , server_default=OrderItemStatus.PENDING)
    #add : dims, product_relationship , files_id , price ,  
    item_price : Mapped[Float] = mapped_column(Float , default=0.0 , nullable=True)
    product : Mapped["ProductModel"] = relationship(back_populates="order_items")
    order : Mapped["OrderModel"] = relationship(back_populates="items")
    
