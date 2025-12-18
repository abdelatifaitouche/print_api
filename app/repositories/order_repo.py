from sqlalchemy.orm import Session
from app.models.order import OrderModel
from typing import List
from sqlalchemy import select
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository['OrderModel']):
    MODEL = OrderModel
