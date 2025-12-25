from fastapi import APIRouter , Depends
from app.schemas.company_schema import CompanyCreate, CompanyRead , CompanyUpdate
from app.config.database import get_db
from app.services.company_service import CompanyService
from sqlalchemy.orm import Session
from typing import List
from app.utils.private_route import PrivateRoute
from app.enums.roles import Roles
from app.enums.permissions import Permissions

company_endpoints = APIRouter()


company_service = CompanyService()

@company_endpoints.get("/{company_id}" , response_model=CompanyRead)
def get_company(company_id : str , db : Session = Depends(get_db) , user : dict = Depends(PrivateRoute(roles=[Roles.ADMIN]))):
    company : CompanyRead = company_service.get_by_id(company_id , db)
    return company


@company_endpoints.post('/' , response_model=CompanyRead)
def create_company(company_data : CompanyCreate , db:Session=Depends(get_db), user : dict=Depends(PrivateRoute(roles=[Roles.ADMIN]))): 
    print("user" , user)
    company : CompanyRead = company_service.create(company_data , db , user["id"])

    return company

@company_endpoints.get('/' , response_model=List[CompanyRead])
def list_companies(db : Session = Depends(get_db) , user : dict = Depends(PrivateRoute(roles=[Roles.ADMIN])))->List[CompanyRead]:
    print(user) 
    companies : List[CompanyRead] = company_service.list(db)

    return companies




@company_endpoints.patch('/{company_id}/' , response_model=CompanyRead)
def update_company(company_id : str , company_data : CompanyUpdate , db:Session=Depends(get_db)):
    
    company : CompanyRead = company_service.update(company_id , company_data , db)

    return company

@company_endpoints.delete("/{company_id}/")
def delete_company(company_id : str , db:Session=Depends(get_db) , user : dict = Depends(PrivateRoute(roles=[Roles.ADMIN]))):

    if not company_service.delete(company_id , db) : 
        return "not delete"

    return "deleted"




