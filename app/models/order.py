from .base import Base
from sqlalchemy import String , Integer
from sqlalchemy.orm import Mapped , mapped_column , relationship
from app.enums.order_enums import OrderStatus


class OrderModel(Base):
    __tablename__="orders"

    order_name:Mapped[str] = mapped_column(String , nullable=False)
    status : Mapped[str] = mapped_column(String , server_default=OrderStatus.PENDING.value)
    
    order_price:Mapped[int] = mapped_column(Integer , nullable=False)
    
    #add client_id , delivery_date , 

    items : Mapped[list["OrderItem"]] = relationship(
                back_populates = "order" , cascade="all , delete-orphan"
            )
