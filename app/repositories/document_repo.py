from app.models.finance_document import DocumentModel
from app.repositories.base import BaseRepository


class DocumentRepository(BaseRepository["DocumentModel"]):
    MODEL = DocumentModel
