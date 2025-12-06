from .base import Base
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String




class CompanyModel(Base):
    
    __tablename__="companies"

    name : Mapped[str] = mapped_column(String , nullable=False , unique=True)
    address : Mapped[str] = mapped_column(String , nullable=True)
    email : Mapped[str] = mapped_column(String , nullable=True)
    phone : Mapped[str] = mapped_column(String , nullable=True)
    

    def __repr__(self):
        return f"<Company : {self.name}>"
