from sqlalchemy.orm import Session
from app.models.order import OrderModel
from typing import List
from sqlalchemy import select, Select
from app.repositories.base import BaseRepository
from app.schemas.pagination import Pagination
from app.filters.order_filters import OrderFilters


class OrderRepository(BaseRepository["OrderModel"]):
    MODEL = OrderModel
