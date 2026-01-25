from sqlalchemy.orm import Session

from app.models.company import CompanyModel
from app.repositories.company_repo import CompanyRepository
from app.schemas.company_schema import CompanyCreate, CompanyRead, CompanyUpdate
from app.services.base_service import BaseService
from app.utils.tasks import process_folder_creation


class CompanyService(
    BaseService[CompanyModel, CompanyCreate, CompanyRead, CompanyUpdate]
):
    repo = CompanyRepository()
    READ_SCHEMA = CompanyRead

    def __init__(self):
        """
        should add the company repo
        """
        self.__repo = CompanyRepository()

    def create(
        self, company_data: CompanyCreate, db: Session, user_id: str | None = None
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
        created_model: CompanyModel = self.__repo.create(model, db)

        if not created_model:
            raise Exception("Company was not created")

        process_folder_creation.delay(
            company_id=created_model.id, folder_name=company_data.name + "Drive"
        )

        return CompanyRead.from_orm(created_model)

    """
    def get_by_id(self, company_id: str, db: Session) -> CompanyRead:
        company: CompanyModel = self.__repo.get_by_id(company_id, db)

        if not company:
            raise Exception("no company found")

        return CompanyRead.from_orm(company)
    """

    def delete(self, company_id: str, db: Session) -> bool:
        company: CompanyModel = self.__repo.get_by_id(company_id, db)

        if not company:
            raise Exception("No Company Found")

        return self.__repo.delete(company.id, db)

    def update(self, company_id: str, data: CompanyUpdate, db: Session) -> CompanyRead:
        company_model: CompanyModel = self.__repo.get_by_id(company_id, db)

        """
            validate the data first ??
        """

        updated_data: dict = data.dict(exclude_unset=True)

        updated_model: CompanyModel = self.__repo.update(
            company_model, updated_data, db
        )

        if not updated_model:
            raise Exception("an error has occured while updating")

        return CompanyRead.from_orm(updated_model)
