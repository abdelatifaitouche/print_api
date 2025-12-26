from .base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String 



class PrintingType(Base):
    __tablename__="printingtypes"
 
    name : Mapped[str] = mapped_column(String(length=50) , nullable=False)
    description : Mapped[str] = mapped_column(String(length=200) , nullable=True)


    def __str__(self):
        return f"Printing Type : {self.name}"


