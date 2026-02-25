from app.models.company import CompanyModel
from app.repositories.base import BaseRepository


class CompanyRepository(BaseRepository["CompanyModel"]):
    MODEL = CompanyModel
