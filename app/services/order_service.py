from .interface import ServiceInterface
from app.models.order import OrderModel
from app.schemas.order_schema import OrderCreate , OrderRead
from app.repositories.order_repo import OrderRepository
from sqlalchemy.orm import Session
from typing import List
from fastapi.exceptions import HTTPException
from fastapi import status
from app.services.order_item_service import OrderItemService
from app.schemas.order_item_schema import OrderItemCreate

class OrderService(ServiceInterface) :
    
    def __init__(self):
        self.__order_repo = OrderRepository()
        self.__order_item_service = OrderItemService()

    def list(self , db : Session) -> List[OrderRead]:
        orders : List[OrderModel] = self.__order_repo.list(db)
        
        order_list : List[OrderRead] = [OrderRead.from_orm(order) for order in orders]

        return order_list


    def create(self , db : Session , order_data : OrderCreate)->OrderRead:
        try :  
            order = OrderModel(order_name = order_data.order_name ,order_price = order_data.order_price )

            order_created = self.__order_repo.create(order , db)
            print("am i even here") 
            if order_created : 
                i = 0
                print(order_created.id)
                for item in order_data.items : 
                    print(f"creating the item {i}")
                    order_item : OrderItemCreate = OrderItemCreate(
                                order_id = order_created.id,
                                item_name = item.item_name,
                                quantity = item.quantity
                                 )
                    self.__order_item_service.create(order_item , db)
                    i+=1
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
