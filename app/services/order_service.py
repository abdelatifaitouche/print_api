from .interface import ServiceInterface
from app.models.order import OrderModel
from app.schemas.order_schema import OrderCreate , OrderRead
from app.repositories.order_repo import OrderRepository
from sqlalchemy.orm import Session
from typing import List
from fastapi.exceptions import HTTPException
from fastapi import status , UploadFile
from app.services.order_item_service import OrderItemService
from app.schemas.order_item_schema import OrderItemCreate
from app.models.order_item import OrderItem as OrderItemDb
from app.models.uploaded_file import UploadedFile as UploadedFileDb
import uuid
from app.utils.tasks import process_file_upload
from pathlib import Path
import shutil
class OrderService(ServiceInterface) :
    
    def __init__(self):
        self.__order_repo = OrderRepository()
        self.__order_item_service = OrderItemService()
        self.UPLOAD_DIR = Path("/app/uploads")
        self.UPLOAD_DIR.mkdir(parents=True , exist_ok=True)
    def list(self , db : Session , user_id : str | None = None ) -> List[OrderRead]:
        orders : List[OrderModel] = self.__order_repo.list(db , user_id)
        
        order_list : List[OrderRead] = [OrderRead.from_orm(order) for order in orders]

        return order_list
    
    def __add_to_db(self , model ,   db : Session):
        db.add(model)
        db.flush()
        db.refresh(model)
        return model
    
    def __calculate_item_price(self , product_id , quantity , db:Session):
        from app.services.product_service import ProductService
        from app.schemas.product_schema import ProductRead
        
        product_service = ProductService()

        product : ProductRead = product_service.get_by_id(product_id , db)
        
        if not product : 
            raise Exception(f"Could not get the product with the id {product_id}")

        if product.base_price <= 0 or quantity <= 0 : 
            raise Exception("Invalid Data while calculating the item price")

        return product.base_price* quantity 

    def __order_item_create(self , order_id : str ,  order_item , file , db : Session) : 
        if not order_item.quantity or order_item.quantity <= 0 : 
            raise Exception("Invalid Data for Order Item")
        
        item_price : float = self.__calculate_item_price(order_item.product_id , order_item.quantity , db)

        order_item_db : OrderItemDb = OrderItemDb(
            order_id = order_id , 
            product_id = order_item.product_id,
            quantity = order_item.quantity , 
            item_price = item_price
        )

        return self.__add_to_db(order_item_db ,db)
    
    def __process_file(self , file):
        """
            generate a unique file name and create the file path
        """    
        file_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = self.UPLOAD_DIR / file_name
        
        try :
            #this is not good, gotta make it async using aiofiles
            with file_path.open("wb") as buffer : 
                shutil.copyfileobj(file.file , buffer)
        except Exception as e : 
            raise e
        file.file.seek(0)

        size = file_path.stat().st_size
        if size == 0 : 
            raise ValueError(f"Empty file saved {file.filename}")
        return file_name , file_path

    def create(self, db: Session, order_data: OrderCreate, user: dict, files) -> OrderRead:
        from app.services.company_service import CompanyService
        from app.schemas.company_schema import CompanyRead
        company_service = CompanyService()
        company_data : CompanyRead = company_service.get_by_id(user["company_id"] , db)
        
        if not company_data : 
            raise ValueError("No company found with this id")
        
        if not company_data.drive_folder_id or company_data.folder_status != "CREATED" : 
            raise Exception("Folder blocked for this company")
            
        drive_folder : str = company_data.drive_folder_id 
        
        try:
            order = OrderModel(created_by=user["id"])
            order_id = self.__add_to_db(order, db).id
        
            if order_id: 
                for item, file in zip(order_data.items, files):
                # Create order item
                    order_item = self.__order_item_create(order_id, item, file, db)
                
                # Process and save file
                    file_name, file_path = self.__process_file(file)
                
                # Create uploaded file record
                    uploaded_file = UploadedFileDb(
                        file_name=file_name,
                        status="pending",
                        order_item_id=order_item.id,
                        parent_drive_folder=str(drive_folder)
                    )
                    uploaded_file_id = self.__add_to_db(uploaded_file, db).id
                
                # CRITICAL: Commit here so Celery can find the record
                    db.commit()
                    db.refresh(uploaded_file)
                
                
                    # Dispatch Celery task - ensure ID is string
                    task = process_file_upload.delay(
                        uploaded_file_id=str(uploaded_file_id),
                        file_name=file_name,
                        file_path=str(file_path)
                        )
            
                 # Final commit for the order
                db.commit()
                db.refresh(order)
            
            
                return OrderRead.from_orm(order)
            
        except Exception as e:
            db.rollback()
        
            # Clean up any uploaded files on failure
            try:
                for file in files:
                    file.file.seek(0)  # Reset file pointer
            except:
                pass
            
            raise e
    def get_by_id(self , db : Session , order_id : str)->OrderRead:
        order = self.__order_repo.get_by_id(order_id , db)
        
        if not order : 
            raise HTTPException(detail="Order doesnt exists" , status_code = status.HTTP_400_BAD_REQUEST)

        return OrderRead.from_orm(order)


    def delete():
        return


    def update():
        return
