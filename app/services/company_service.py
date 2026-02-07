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
        """
        FIRST CREATE THE FOLDER DRIVER
        """

        if not company_data.name:
            raise Exception("Company name must be valid")

        if not company_data.email:
            # include some way to verify the email validity
            raise Exception("please enter a valid email")

        model: CompanyModel = CompanyModel(**company_data.dict())
        created_model: CompanyModel = self.__repo.create(model)

        if not created_model:
            raise Exception("Company was not created")

        process_folder_creation.delay(
            company_id=created_model.id, folder_name=company_data.name + "Drive"
        )

        return CompanyRead.from_orm(created_model)
