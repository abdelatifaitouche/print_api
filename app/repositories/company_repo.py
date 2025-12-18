from sqlalchemy.orm import Session
from app.models.company import CompanyModel
from typing import List
from sqlalchemy import select
from app.repositories.base import BaseRepository 

class CompanyRepository(BaseRepository["CompanyModel"]):
    
    MODEL = CompanyModel
