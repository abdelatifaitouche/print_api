from app.repositories.analytics_repo import AnalyticsRepository
from sqlalchemy.orm import Session


class AnalyticsService:
    def __init__(self, db: Session):
        self.db: Session = db
        self.repo: AnalyticsRepository = AnalyticsRepository(db)

    def get_orders_analytics(self):
        order_results = self.repo.order_stats()

        doc_results = self.repo.facture_stats()

        return {"order_stats": order_results, "facture_stats": doc_results}

    def financial_analytics():
        return
