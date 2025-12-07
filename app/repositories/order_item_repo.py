from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.order_item import OrderItem



class OrderItemRepository:



    def create(self , order_item : OrderItem , db : Session)->OrderItem:
        db.add(order_item)
        db.flush()
        return order_item


    
    def get_by_id():
        return


    def list():
        return
