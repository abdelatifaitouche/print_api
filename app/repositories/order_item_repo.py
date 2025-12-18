from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.order_item import OrderItem
from app.repositories.base import BaseRepository


class OrderItemRepository(BaseRepository["OrderItem"]):
    MODEL = OrderItem
