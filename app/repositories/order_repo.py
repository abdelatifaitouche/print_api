from sqlalchemy.orm import Session
from app.models.order import OrderModel
from typing import List
from sqlalchemy import select, Select, func, text
from app.repositories.base import BaseRepository
from app.schemas.pagination import Pagination
from app.filters.order_filters import OrderFilters


class OrderRepository(BaseRepository["OrderModel"]):
    MODEL = OrderModel

    def getOrderStats(self, client_id: str | None = None):
        query = text("""
            SELECT
                COUNT(*) AS total_orders , 
                COUNT(*) FILTER (WHERE status = 'PENDING') AS pending,
                COUNT(*) FILTER (WHERE status = 'ACCEPTED') AS accepted , 
                COUNT(*) FILTER (WHERE status = 'PAIED') AS paid
            FROM orders
            WHERE (:client_id IS NULL OR company_id = :client_id)
                     """)

        result = self.db.execute(query, {"client_id": client_id})

        return result.fetchone()._mapping
