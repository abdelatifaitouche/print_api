from sqlalchemy.orm import Session
from sqlalchemy import text


class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def order_stats(self):
        query = text("""
            SELECT 
                COUNT(*) AS total_orders , 
                COUNT(*) FILTER (WHERE status='FINISHED') AS total_finished,
                COUNT(*) FILTER (WHERE created_at::date = CURRENT_DATE) AS recent_created,
                COUNT(*) FILTER (WHERE status='ACCEPTED') AS total_accepted
            FROM orders 
        """)

        results = self.db.execute(query).fetchone()._mapping

        return results

    def facture_stats(self):
        query = text("""
                   SELECT status ,  COUNT(*) AS total FROM documents WHERE document_type='FACTURE' GROUP BY status
                     """)

        results = self.db.execute(query).fetchall()

        return {row.status: row.total for row in results}
