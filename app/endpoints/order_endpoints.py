from fastapi import APIRouter ,  UploadFile
from app.schemas.order_schema import OrderCreate , OrderRead
from app.config.database import get_db
from fastapi import Depends
from app.services.order_service import OrderService
from sqlalchemy.orm import Session
from typing import List
from app.utils.private_route import PrivateRoute
from app.utils.google_drive_manager import GoogleDriveManager
order_endpoint = APIRouter(
)
order_service = OrderService()

gdm = GoogleDriveManager()


@order_endpoint.get("/" , response_model=List[OrderRead])
def list_orders(db : Session= Depends(get_db)):
    orders = order_service.list(db)
    return orders


@order_endpoint.get("/{order_id}" , response_model=OrderRead)
def get_order_by_id(order_id : str , db : Session = Depends(get_db)):
    order = order_service.get_by_id(db , order_id)
    return order




@order_endpoint.post("/" , response_model=OrderRead)
def create_order(order_data : OrderCreate , files : List[UploadFile], db:Session = Depends(get_db)) -> OrderRead:
    order = order_service.create(db , order_data , files)
    return order



@order_endpoint.get("/test_drive/")
def test_drive():
    folder_id = gdm.create_folder("testfolder")
    return f"folder id {folder_id}"





