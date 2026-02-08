from sqlalchemy.orm import Session

from app.models.company import CompanyModel
from app.repositories.company_repo import CompanyRepository
from app.schemas.company_schema import CompanyCreate, CompanyRead, CompanyUpdate
from app.services.base_service import BaseService
from app.utils.tasks import process_folder_creation


class CompanyService(
    BaseService[CompanyModel, CompanyCreate, CompanyRead, CompanyUpdate]
):
    REPO_CLASS = CompanyRepository
    READ_SCHEMA = CompanyRead

    def create(
        self, company_data: CompanyCreate, user_id: str | None = None
    ) -> CompanyRead:
        model: CompanyModel = CompanyModel(**company_data.dict())
        created_model: CompanyModel = self.repo.create(model)

        process_folder_creation.delay(
            company_id=created_model.id, folder_name=company_data.name + "Drive"
        )

        return CompanyRead.from_orm(created_model)
