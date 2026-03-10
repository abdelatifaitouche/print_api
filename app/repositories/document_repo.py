from app.models.finance_document import DocumentModel
from app.repositories.base import BaseRepository
from sqlalchemy import text


class DocumentRepository(BaseRepository["DocumentModel"]):
    MODEL = DocumentModel

    def get_client_summary(self, client_id: str):
        query = text("""
            SELECT 
                SUM(total_remaining) AS total_remaining , 
                SUM(total_paid) AS total_paid ,
                SUM(total) AS total ,
                COUNT(*) AS total_factures 
            FROM documents
            WHERE document_type = 'FACTURE'
            AND company_id = :client_id

                     """)

        result = self.db.execute(query, {"client_id": client_id})
        row = result.fetchone()
        return row._mapping
