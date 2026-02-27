from app.repositories.base import BaseRepository
from app.models.payment_model import PaymentModel
from sqlalchemy import select, Select


class PaymentRepository(BaseRepository["PaymentModel"]):
    MODEL = PaymentModel

    def get_by_document_id(self, document_id: str) -> list[PaymentModel]:
        stmt: Select = select(self.MODEL)

        stmt = stmt.where(self.MODEL.document_id == document_id)

        result: list[PaymentModel] = self.db.execute(stmt).scalars().all()

        return result
