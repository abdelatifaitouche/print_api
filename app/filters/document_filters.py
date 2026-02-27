from .base_filters import BaseFilters
from sqlalchemy import Select


class DocumentFilters(BaseFilters):
    def __init__(
        self,
        all: bool = False,
        user_id: str | None = None,
        status: str | None = None,
        company_id: str | None = None,
        document_type: str | None = None,
        order_id: str | None = None,
    ):
        self.order_id = order_id
        self.company_id = company_id
        self.document_type = document_type

        super().__init__(all, user_id, status)

    def apply(self, stmt: Select, model):
        stmt = super().apply(stmt, model)

        if self.company_id:
            stmt = stmt.where(model.company_id == self.company_id)

        if self.document_type:
            stmt = stmt.where(model.document_type == self.document_type)

        if self.order_id:
            stmt = stmt.where(model.order_id == self.order_id)

        return stmt
