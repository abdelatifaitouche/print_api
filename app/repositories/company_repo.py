from sqlalchemy.orm import Session
from app.models.company import CompanyModel
from typing import List
from sqlalchemy import select, func
from app.repositories.base import BaseRepository


class CompanyRepository(BaseRepository["CompanyModel"]):
    MODEL = CompanyModel
