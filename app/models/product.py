from .base import Base
from sqlalchemy.orm import Mapped , mapped_column , relationship 
from sqlalchemy import String , Float
from typing import List


class ProductModel(Base) : 
    __tablename__="products"

    name : Mapped[str] = mapped_column(String , nullable=False)
    description : Mapped[str] = mapped_column(String , nullable=True)
    base_price : Mapped[Float] = mapped_column(Float , nullable=True)

    raw_materials : Mapped[List["RawMaterial"]] = relationship(secondary="product_material" , back_populates="products")

    order_items: Mapped[List["OrderItem"]] = relationship(
        back_populates="product"
    )


