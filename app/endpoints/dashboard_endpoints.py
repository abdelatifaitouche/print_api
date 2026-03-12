from fastapi import APIRouter, Depends
from app.services.dashboard_service import AnalyticsService
from app.config.database import get_db
from sqlalchemy.orm import Session

dashboard = APIRouter()


def get_service(db: Session = Depends(get_db)):
    return AnalyticsService(db)


@dashboard.get("")
def order_stats(service: AnalyticsService = Depends(get_service)):
    return service.get_orders_analytics()
