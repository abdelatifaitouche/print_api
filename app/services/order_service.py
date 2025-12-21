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

class OrderService(ServiceInterface) :
    
    def __init__(self):
        self.__order_repo = OrderRepository()
        self.__order_item_service = OrderItemService()

    def list(self , db : Session , user_id : str | None = None ) -> List[OrderRead]:
        orders : List[OrderModel] = self.__order_repo.list(db , user_id)
        
        order_list : List[OrderRead] = [OrderRead.from_orm(order) for order in orders]

        return order_list
    

    def create(self , db : Session , order_data : OrderCreate , user : dict )->OrderRead:
        """
            Creates an order and its item in cascade, 
            the whole creation is done in one single transaction to avoid
            any data integrity issues

        """    


        try :  
            order = OrderModel(order_name = order_data.order_name ,order_price = order_data.order_price , created_by = user["id"] )
            order_created = self.__order_repo.create(order , db)
            if order_created :

                for item  in order_data.items :
                    if not item.item_name : 
                        raise Exception("item name must be added")

                    if not item.quantity or item.quantity <= 0 :
                        raise Exception("Invalid quantity input")

                    #file will be uploaded in the background
                    order_item : OrderItemCreate = OrderItemCreate(
                                order_id = order_created.id,
                                item_name = item.item_name,
                                quantity = item.quantity
                                 )
                    item_model  = self.__order_item_service.create(order_item , db)

                    #files are uploaded here in the queue pass the file + the item.id()
            else : 
                raise Exception("an error has occured while creating the order")

            db.commit()
            return OrderRead.from_orm(order_created)
        except : 
            db.rollback()
            raise Exception("an error has occured while creating th items or order")

    def get_by_id(self , db : Session , order_id : str)->OrderRead:
        order = self.__order_repo.get_by_id(order_id , db)
        
        if not order : 
            raise HTTPException(detail="Order doesnt exists" , status_code = status.HTTP_400_BAD_REQUEST)

        return OrderRead.from_orm(order)


    def delete():
        return


    def update():
        return
