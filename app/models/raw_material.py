from sqlalchemy.orm import Mapped, mapped_column , relationship
from sqlalchemy import DECIMAL , String
from decimal import Decimal
from typing import List
from .base import Base



class RawMaterial(Base):

    __tablename__="raw_materials"

    name : Mapped[str] = mapped_column(String(255) , nullable=False)
    stock_quantity : Mapped[Decimal] = mapped_column(DECIMAL(10 , 2) , nullable=True) 
    cost_per_unit : Mapped[Decimal] = mapped_column(DECIMAL(10 ,2) , nullable=True)
    products : Mapped[List["Product"]] = relationship(secondary="product_material" , back_populates="raw_materials")

