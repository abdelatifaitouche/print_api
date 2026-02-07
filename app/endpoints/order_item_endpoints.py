from fastapi import APIRouter, UploadFile, File
from app.services.order_item_service import OrderItemService
from app.schemas.order_item_schema import OrderItemCreate, OrderItemRead
from app.config.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


order_item_endpoints = APIRouter()
