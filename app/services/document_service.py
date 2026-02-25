from app.services.base_service import BaseService
from app.schemas.finance_schemas import (
    DocumentSummary,
    DocumentCreate,
    DocumentRead,
    DocumentUpdate,
)
from app.models.finance_document import DocumentModel
from app.repositories.document_repo import DocumentRepository
from app.models.order import OrderModel
from app.repositories.order_repo import OrderRepository
from app.auth.permission_context import PermissionContext
from app.enums.document_type import DocumentType, DocumentStatus
from datetime import datetime


class DocumentService(
    BaseService[DocumentModel, DocumentCreate, DocumentRead, DocumentUpdate]
):
    REPO_CLASS = DocumentRepository
    READ_SCHEMA = DocumentRead
    CREATE_SCHEMA = DocumentCreate
    UPDATE_SCHEMA = DocumentUpdate
    DB_MODEL = DocumentModel

    def create(self, data: DocumentCreate, ctx: PermissionContext) -> DocumentSummary:
        order_repo: OrderRepository = OrderRepository(self.db)
        order: OrderModel = order_repo.get_by_id(data.order_id)
        from app.repositories.company_repo import CompanyRepository
        from app.models.company import CompanyModel

        company_repo: CompanyRepository = CompanyRepository(self.db)
        company: CompanyModel = company_repo.get_by_id(data.company_id)

        if not order.order_price or order.order_price <= 0:
            raise ValueError("Invalid Order Price")

        tva: float = 0.19

        document: DocumentModel = DocumentModel(
            order_id=data.order_id,
            company_id=data.company_id,
            total=order.order_price * tva + order.order_price,
            total_ht=order.order_price,
            total_paid=0.0,
            total_remaining=order.order_price,
            created_by=str(ctx.user.user_id),
        )

        return DocumentSummary.from_orm(self.repo.create(document))

    def approve_devis(self, entity_id: str, ctx: PermissionContext):
        document: DocumentRead = super().get_by_id(entity_id)

        if document.document_type != DocumentType.DEVIS:
            raise ValueError("Cant approve facture")

        if document.status != DocumentStatus.DRAFT:
            raise ValueError("Cant approve non drafts")

        facture: DocumentModel = DocumentModel(
            document_type=DocumentType.FACTURE,
            status=DocumentStatus.PENDING_PAYMENT,
            order_id=document.order.id,
            company_id=document.company.id,
            created_by=document.creator.id,
            approved_by=str(ctx.user.user_id),
            total_ht=document.total_ht,
            total=document.total,
            total_paid=document.total_paid,
            total_remaining=document.total_remaining,
            approved_at=datetime.utcnow(),
            devis_id=document.id,
        )

        return DocumentSummary.from_orm(self.repo.create(facture))
