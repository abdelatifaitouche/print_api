from .base import Base
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String
from app.enums.company_enums import FolderStatus



class CompanyModel(Base):
    
    __tablename__="companies"

    name : Mapped[str] = mapped_column(String , nullable=False , unique=True)
    address : Mapped[str] = mapped_column(String , nullable=True)
    email : Mapped[str] = mapped_column(String , nullable=True)
    phone : Mapped[str] = mapped_column(String , nullable=True)
    drive_folder_id : Mapped[str] = mapped_column(String , nullable=True)    
    folder_status : Mapped[str] = mapped_column(String , server_default=FolderStatus.PENDING.value , nullable=False)
    def __repr__(self):
        return f"<Company : {self.name}>"
