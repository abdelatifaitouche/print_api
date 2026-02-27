from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.finance_schemas import DocumentCreate, DocumentSummary
from app.auth.permission_context import PermissionContext
from app.enums.permissions import Permissions
from app.services.document_service import DocumentService
from app.auth.permissions_api import require_permission
from app.filters.document_filters import DocumentFilters
from app.schemas.pagination import Pagination


def get_service(db: Session = Depends(get_db)):
    return DocumentService(db)


finance_endpoints = APIRouter()


@finance_endpoints.get("")
def list_documents(
    filters: DocumentFilters | None = Depends(DocumentFilters),
    pagination: Pagination | None = Depends(Pagination),
    service: DocumentService = Depends(get_service),
    ctx: PermissionContext = Depends(require_permission(Permissions.CAN_READ_ALL)),
):
    return service.list(filters, pagination)


@finance_endpoints.get("/{document_id}")
def get_document_by_id(
    document_id: str,
    service: DocumentService = Depends(get_service),
):
    return service.get_by_id(document_id)


@finance_endpoints.get("/{order_id}/documents")
def list_order_documents(
    order_id: str,
    filters: DocumentFilters | None = Depends(DocumentFilters),
    service: DocumentService = Depends(get_service),
    pagination: Pagination | None = Depends(Pagination),
):
    return service.get_order_documents(order_id, filters, pagination)


@finance_endpoints.post("/create/", response_model=DocumentSummary)
def create_document(
    data: DocumentCreate,
    service: DocumentService = Depends(get_service),
    ctx: PermissionContext = Depends(require_permission(Permissions.CAN_CREATE_ALL)),
):
    return service.create(data, ctx)


@finance_endpoints.post("/{document_id}/approve/", response_model=DocumentSummary)
def approve_document(
    document_id: str,
    service: DocumentService = Depends(get_service),
    ctx: PermissionContext = Depends(
        require_permission(Permissions.CAN_CREATE_ALL),
    ),
):
    return service.approve_devis(document_id, ctx)
