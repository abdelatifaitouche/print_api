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
class OrderService(ServiceInterface) :
    
    def __init__(self):
        self.__order_repo = OrderRepository()
        self.__order_item_service = OrderItemService()

    def list(self , db : Session , user_id : str | None = None ) -> List[OrderRead]:
        orders : List[OrderModel] = self.__order_repo.list(db , user_id)
        
        order_list : List[OrderRead] = [OrderRead.from_orm(order) for order in orders]

        return order_list
    

    def create(self , db : Session , order_data : OrderCreate , user : dict )->OrderRead:
        from app.services.product_service import ProductService
        from app.schemas.product_schema import ProductRead
        product_service = ProductService()
        try :  
            order = OrderModel(created_by = user["id"] )
            order_created = self.__order_repo.create(order , db)
            if order_created :
                for item  in order_data.items :
                    if not item.quantity or item.quantity <= 0 :
                        raise Exception("Invalid quantity input")

                    product : ProductRead = product_service.get_by_id(item.product_id , db)
                    
                    item_price : float = product.base_price * item.quantity

                    #file will be uploaded in the background
                    order_item : OrderItemDb = OrderItemDb(
                                order_id = order_created.id,
                                product_id = item.product_id,
                                quantity = item.quantity,
                                item_price = item_price
                                 )
                    db.add(order_item)
            else : 
                raise Exception("order wasnt created")
                    #files are uploaded here in the queue pass the file + the item.id()
            db.commit()
            return OrderRead.from_orm(order_created)
        except Exception as e : 
            db.rollback()
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
