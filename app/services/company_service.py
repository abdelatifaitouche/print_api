from sqlalchemy.orm import Session

from app.models.company import CompanyModel
from app.repositories.company_repo import CompanyRepository
from app.schemas.company_schema import CompanyCreate, CompanyRead, CompanyUpdate
from app.services.base_service import BaseService
from app.utils.tasks import process_folder_creation
from app.repositories.document_repo import DocumentRepository
from app.repositories.order_repo import OrderRepository


class CompanyService(
    BaseService[CompanyModel, CompanyCreate, CompanyRead, CompanyUpdate]
):
    REPO_CLASS = CompanyRepository
    READ_SCHEMA = CompanyRead
    CREATE_SCHEMA = CompanyCreate
    UPDATE_SCHEMA = CompanyUpdate
    DB_MODEL = CompanyModel

    def create(
        self, company_data: CompanyCreate, user_id: str | None = None
    ) -> CompanyRead:
        model: CompanyModel = CompanyModel(**company_data.dict())
        created_model: CompanyModel = self.repo.create(model)

        process_folder_creation.delay(
            company_id=created_model.id, folder_name=company_data.name + "Drive"
        )

        return CompanyRead.from_orm(created_model)

    def list_all_min(self):
        return

    def get_stats(self, company_id: str):
        doc_repo = DocumentRepository(self.db)
        order_repo = OrderRepository(self.db)
        client_summary: dict = doc_repo.get_client_summary(company_id)
        order_stats: dict = order_repo.getOrderStats(company_id)
        return {"finance": client_summary, "orders": order_stats}
