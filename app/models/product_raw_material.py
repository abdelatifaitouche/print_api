from sqlalchemy.orm import Mapped , mapped_column
from .base import Base
from sqlalchemy import DECIMAL, String , ForeignKey
from decimal import Decimal


class ProductRawMaterial(Base):
    
    __tablename__="product_material"

    product_id : Mapped[str] = mapped_column(ForeignKey("products.id") , primary_key=True)
    raw_material_id : Mapped[str] = mapped_column(ForeignKey("raw_materials.id") , primary_key=True)
    quantity : Mapped[Decimal] = mapped_column(DECIMAL(10 , 2))


