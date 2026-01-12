from app.models.base import Base 
from sqlalchemy.orm import Mapped , mapped_column , relationship
from sqlalchemy import String , ForeignKey
from app.enums.file_enums import FileStatus

class UploadedFile(Base):
    
    __tablename__="uploaded_file"
 
    google_file_id : Mapped[str] = mapped_column(String , nullable=True)
    file_name : Mapped[str] = mapped_column(String , nullable=False)
    status : Mapped[str] = mapped_column(String , server_default=FileStatus.PENDING.value)
    parent_drive_folder : Mapped[str] = mapped_column(String , nullable=False)
    
    order_item_id : Mapped[str] = mapped_column(
        String , 
        ForeignKey("order_items.id"),
        unique = True , 
        nullable=False
    )

    order_item : Mapped["OrderItem"] = relationship(
        "OrderItem" ,
        back_populates = "file" , 
        uselist=False , 
        passive_deletes = True
    )

    

    def __str__(self):
        return f"<File : {self.file_name}>"
