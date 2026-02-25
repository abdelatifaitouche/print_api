from enum import StrEnum


class DocumentType(StrEnum):
    DEVIS = "DEVIS"
    FACTURE = "FACTURE"


class DocumentStatus(StrEnum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PARTIAL_PAID = "PARTIAL_PAID"
    PAID = "PAID"
