from .interface import ServiceInterface
from app.models.order import OrderModel
from app.schemas.order_schema import OrderCreate , OrderRead
from app.repositories.order_repo import OrderRepository
from sqlalchemy.orm import Session
from typing import List
from fastapi.exceptions import HTTPException
from fastapi import status

class OrderService(ServiceInterface) :
    
    def __init__(self):
        self.__order_repo = OrderRepository()
    
    def list(self , db : Session) -> List[OrderRead]:
        orders : List[OrderModel] = self.__order_repo.list(db)
        
        order_list : List[OrderRead] = [OrderRead.from_orm(order) for order in orders]

        return order_list


    def create(self , db : Session , order_data : OrderCreate)->OrderRead:
        
        order = OrderModel(**order_data.dict())

        order_created = self.__order_repo.create(order , db)

        return OrderRead.from_orm(order_created)


    def get_by_id(self , db : Session , order_id : str)->OrderRead:
        order = self.__order_repo.get_by_id(order_id , db)
        
        if not order : 
            raise HTTPException(detail="Order doesnt exists" , status_code = status.HTTP_400_BAD_REQUEST)

        return OrderRead.from_orm(order)


    def delete():
        return


    def update():
        return
