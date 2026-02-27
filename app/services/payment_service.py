from app.services.base_service import BaseService
from app.models.payment_model import PaymentModel
from app.schemas.payment_schemas import (
    PaymentCreate,
    PaymentRead,
    PaymentSummary,
    PaymentUpdate,
)
from app.repositories.payment_repo import PaymentRepository
from app.repositories.document_repo import DocumentRepository
from app.schemas.finance_schemas import DocumentRead, DocumentUpdate
from app.enums.document_type import DocumentType, DocumentStatus
from app.auth.permission_context import PermissionContext
from app.execeptions.exceptions_handlers import ValidationError, NotFoundError


class PaymentService(
    BaseService[PaymentModel, PaymentCreate, PaymentRead, PaymentUpdate]
):
    DB_MODEL = PaymentModel
    READ_SCHEMA = PaymentRead
    UPDATE_SCHEMA = PaymentUpdate
    CREATE_SCHEMA = PaymentCreate
    REPO_CLASS = PaymentRepository

    def create(self, facture_id: str, data: PaymentCreate, ctx: PermissionContext):
        if not facture_id:
            raise ValidationError(message="Facture ID is required")

        document_repo = DocumentRepository(self.db)
        facture = document_repo.get_by_id(facture_id)

        if not facture:
            raise NotFoundError(message="Facture not found")

        if facture.document_type != DocumentType.FACTURE:
            raise ValidationError(message="Document must be a FACTURE")

        if facture.status == DocumentStatus.PAID:
            raise ValidationError(message="Facture is already fully paid")

        if data.amount > facture.total_remaining:
            raise ValidationError(message="Payment amount exceeds remaining balance")

        try:
            # 1. create the payment record
            payment = PaymentModel(
                amount=data.amount,
                payment_method=data.payment_method,
                document_id=facture_id,
                created_by=str(ctx.user.user_id),
            )
            self.db.add(payment)
            self.db.flush()  # payment exists in session, not committed yet

            # 2. recompute totals from all payments including the new one
            all_payments = self.repo.get_by_document_id(facture_id)
            total_paid = sum(p.amount for p in all_payments)

            # 3. update document in the same transaction
            facture.total_paid = total_paid
            facture.total_remaining = facture.total - total_paid

            if facture.total_remaining <= 0:
                facture.status = DocumentStatus.PAID
            elif total_paid > 0:
                facture.status = DocumentStatus.PARTIAL_PAID

            # 4. single commit — everything atomic
            self.db.commit()
            self.db.refresh(payment)

            return PaymentRead.from_orm(payment)

        except Exception:
            self.db.rollback()
            raise
