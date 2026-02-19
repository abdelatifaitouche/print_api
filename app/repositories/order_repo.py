from sqlalchemy.orm import Session
from app.models.order import OrderModel
from typing import List
from sqlalchemy import select, Select
from app.repositories.base import BaseRepository
from app.schemas.pagination import Pagination
from app.filters.base_filters import BaseFilters


class OrderFilters(BaseFilters):
    def __init__(self, user_id, status, company_id: str | None = None):
        self.company_id = company_id
        super().__init__(self, user_id, status)

    def apply(self, model):
        stmt = super().apply()

        if self.company_id:
            stmt = stmt.where(model.company_id == self.company_id)

        return stmt


class OrderRepository(BaseRepository["OrderModel"]):
    MODEL = OrderModel
