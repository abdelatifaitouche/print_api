from app.services.base_service import BaseService
from app.models.product import ProductModel
from app.schemas.product_schema import ProductRead, ProductCreate, ProductUpdate
from app.repositories.product_repo import ProductRepository
from sqlalchemy.orm import Session
from app.models.product_raw_material import ProductRawMaterial
from typing import override


class ProductService(
    BaseService[ProductModel, ProductCreate, ProductRead, ProductUpdate]
):
    REPO_CLASS = ProductRepository
    READ_SCHEMA = ProductRead
    CREATE_SCHEMA = ProductCreate
    UPDATE_SCHEMA = ProductUpdate

    @override
    def create(self, data: ProductCreate) -> ProductRead:
        product: ProductModel = self.repo.create(
            ProductModel(**(data.model_dump(exclude={"raw_materials"})))
        )

        if not product:
            raise Exception("error while creating the product")

        for raw_material in data.raw_materials:
            association = ProductRawMaterial(
                product_id=product.id,
                raw_material_id=raw_material.raw_material_id,
                quantity=raw_material.quantity,
            )
            self.db.add(association)

        self.db.commit()
        self.db.refresh(product)

        return ProductRead.from_orm(product)
