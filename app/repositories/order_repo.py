from sqlalchemy.orm import Session
from app.models.order import OrderModel
from typing import List
from sqlalchemy import select

class OrderRepository:

    def create(self , order:OrderModel, db : Session) -> OrderModel:
        db.add(order)

        db.commit()
        db.refresh(order)
        return order

    def get_by_id(self , order_id : str , db : Session) -> OrderModel : 
        
        stmt = select(OrderModel).where(OrderModel.id == order_id)
        result = db.execute(stmt).scalar_one_or_none()

        return result

    def list(self , db:Session) -> List[OrderModel]:
        stmt = select(OrderModel)
        result = db.execute(stmt).scalars().all()
        return result

