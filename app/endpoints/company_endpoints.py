from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from app.schemas.company_schema import CompanyCreate, CompanyRead, CompanyUpdate
from app.config.database import get_db
from app.services.company_service import CompanyService
from sqlalchemy.orm import Session
from typing import List
from app.utils.private_route import PrivateRoute
from app.enums.roles import Roles
from app.enums.permissions import Permissions
from app.auth.permission_context import PermissionContext
from app.auth.permissions_api import require_permission
from app.filters.base_filters import BaseFilters
from app.schemas.pagination import Pagination

company_endpoints = APIRouter()


def get_service(db: Session = Depends(get_db)):
    return CompanyService(db)


@company_endpoints.get("/{company_id}", response_model=CompanyRead)
def get_company(
    company_id: str,
    company_service: CompanyService = Depends(get_service),
    ctx: PermissionContext = Depends(
        require_permission(Permissions.CAN_READ_ALL, Permissions.CAN_READ_COMPANY)
    ),
):
    if not ctx.is_memeber(str(company_id)):
        raise HTTPException(
            detail="Not Authorized", status_code=status.HTTP_401_UNAUTHORIZED
        )
    company: CompanyRead = company_service.get_by_id(company_id)
    return company


@company_endpoints.post("/", response_model=CompanyRead)
def create_company(
    company_data: CompanyCreate,
    company_service: CompanyService = Depends(get_service),
    ctx: PermissionContext = Depends(require_permission(Permissions.CAN_CREATE_ALL)),
):
    company: CompanyRead = company_service.create(company_data, str(ctx.user.user_id))

    return company


@company_endpoints.get("/", response_model=List[CompanyRead])
def list_companies(
    filters: BaseFilters | None = Depends(BaseFilters),
    pagination: Pagination | None = Depends(Pagination),
    company_service: CompanyService = Depends(get_service),
    ctx: PermissionContext = Depends(require_permission(Permissions.CAN_READ_ALL)),
) -> List[CompanyRead]:
    companies: List[CompanyRead] = company_service.list(filters, pagination)

    return companies


@company_endpoints.patch("/{company_id}/", response_model=CompanyRead)
def update_company(
    company_id: str,
    company_data: CompanyUpdate,
    company_service: CompanyService = Depends(get_service),
):
    company: CompanyRead = company_service.update(company_id, company_data)

    return company


@company_endpoints.delete("/{company_id}/")
def delete_company(
    company_id: str,
    company_service: CompanyService = Depends(get_service),
    user: dict = Depends(PrivateRoute()),
):
    if not company_service.delete(company_id):
        return "not delete"

    return "deleted"
