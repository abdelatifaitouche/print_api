from fastapi import APIRouter , Depends
from app.config.database import get_db
from app.services.product_service import ProductService
from sqlalchemy.orm import Session
from app.schemas.product_schema import ProductRead , ProductCreate
from typing import List

product_endpoints = APIRouter()

product_service = ProductService()



@product_endpoints.post("/" , response_model = ProductRead)
def create_product(data : ProductCreate , db :Session =  Depends(get_db)):
    return product_service.create(data , db)

@product_endpoints.get("/" , response_model = List[ProductRead])
def list_products(db : Session = Depends(get_db)):
    return product_service.list(db)



