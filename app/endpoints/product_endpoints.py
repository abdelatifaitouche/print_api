from fastapi import APIRouter, Depends
from app.config.database import get_db
from app.services.product_service import ProductService
from sqlalchemy.orm import Session
from app.schemas.product_schema import (
    ProductRead,
    ProductUpdate,
    ProductCreate,
    ProductLightRead,
)
from typing import List
from app.auth.permission_context import PermissionContext
from app.auth.permissions_api import require_permission

product_endpoints = APIRouter()


def get_service(db: Session = Depends(get_db)):
    return ProductService(db)


@product_endpoints.post("/", response_model=ProductRead)
def create_product(
    data: ProductCreate, product_service: ProductService = Depends(get_service)
):
    return product_service.create(data)


@product_endpoints.get("/", response_model=List[ProductRead])
def list_products(product_service: ProductService = Depends(get_service)):
    return product_service.list()


@product_endpoints.get("/product/{product_id}/", response_model=ProductLightRead)
def get_product_by_id(
    product_id: str,
    product_service: ProductService = Depends(get_service),
) -> ProductLightRead:
    product: ProductRead = product_service.get_by_id(product_id)

    return ProductLightRead.model_validate(
        product.model_dump(exclude={"raw_materials"})
    )


@product_endpoints.patch("/product/{product_id}/", response_model=ProductRead)
def update_product(
    product_id: str,
    product_data: ProductUpdate,
    product_service: ProductService = Depends(get_service),
):
    return product_service.update(product_id, product_data)


@product_endpoints.delete("/{product_id}/")
def delete_product(
    product_id: str, product_service: ProductService = Depends(get_service)
):
    return product_service.delete(product_id)
