import shutil
import uuid
from pathlib import Path
from typing import List, override, Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.auth.permission_context import PermissionContext
from app.models.order import OrderModel
from app.models.order_item import OrderItem as OrderItemDb
from app.models.uploaded_file import UploadedFile as UploadedFileDb
from app.repositories.order_repo import OrderRepository
from app.schemas.order_schema import OrderCreate, OrderRead, OrderUpdate
from app.services.base_service import BaseService
from app.services.order_item_service import OrderItemService
from app.utils.tasks import process_file_upload
from app.schemas.user_schema import User
from app.execeptions.base import NotFoundError, ValidationError
from app.enums.order_enums import OrderStatus


class OrderService(BaseService[OrderModel, OrderCreate, OrderRead, OrderUpdate]):
    READ_SCHEMA = OrderRead
    CREATE_SCHEMA = OrderCreate
    REPO_CLASS = OrderRepository
    UPDATE_SCHEMA = OrderUpdate

    def __init__(self, db: Session):
        super().__init__(db=db)
        self.__order_item_service = OrderItemService(db)
        self.UPLOAD_DIR = Path("/app/uploads")
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def accept_order(self, order_id: str) -> OrderRead:
        from app.services.order_item_service import OrderItemService
        from app.schemas.order_item_schema import OrderItemUpdate
        from app.enums.order_items_status import OrderItemStatus

        order: OrderModel = self.repo.get_by_id(order_id)

        if order.status != OrderStatus.PENDING.value.lower():
            raise ValidationError(message="Cannot Accept Order status is not Pending")

        updated_order: OrderUpdate = OrderUpdate(
            status=OrderStatus.ACCEPTED.value.lower()
        )

        item_service: OrderItemService = OrderItemService(self.db)

        for item in order.items:
            item_service.update(
                item.id, OrderItemUpdate(status=OrderItemStatus.WAIT_FOR_PROCESSING)
            )
        return super().update(order_id, updated_order)

    def reject_order(self, order_id: str) -> OrderRead:
        from app.services.order_item_service import OrderItemService
        from app.schemas.order_item_schema import OrderItemUpdate
        from app.enums.order_items_status import OrderItemStatus

        order: OrderModel = self.repo.get_by_id(order_id)

        if order.status != OrderStatus.PENDING.value.lower():
            raise ValidationError(message="Cannot reject order")

        updated_order: OrderUpdate = OrderUpdate(status=OrderStatus.REJECTED)

        item_service: OrderItemService = OrderItemService(self.db)

        for item in order.items:
            item_service.update(
                item.id, OrderItemUpdate(status=OrderItemStatus.REJECTED)
            )

        return super().update(order_id, updated_order)

    def __add_to_db(self, model, db: Session):
        db.add(model)
        db.flush()
        db.refresh(model)
        return model

    def __calculate_item_price(self, product_id: str, quantity: float, db: Session):
        from app.schemas.product_schema import ProductRead
        from app.services.product_service import ProductService

        product_service = ProductService(db)

        product: Optional[ProductRead] = product_service.get_by_id(product_id)

        return product.base_price * quantity

    def __order_item_create(self, order_id: str, order_item, file, db: Session):
        if not order_item.quantity or order_item.quantity <= 0:
            raise ValidationError(
                message="Invalid data for order item",
                details={"item": order_item.id, "error": "Invalid Quantity"},
            )

        item_price: float = self.__calculate_item_price(
            order_item.product_id, order_item.quantity, db
        )

        order_item_db: OrderItemDb = OrderItemDb(
            order_id=order_id,
            product_id=order_item.product_id,
            quantity=order_item.quantity,
            item_price=item_price,
        )

        return self.__add_to_db(order_item_db, db)

    def __process_file(self, file):
        file_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = self.UPLOAD_DIR / file_name

        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise e
        file.file.seek(0)

        size = file_path.stat().st_size
        if size == 0:
            raise ValueError(f"Empty file saved {file.filename}")
        return file_name, file_path

    @override
    def create(
        self, order_data: OrderCreate, ctx: PermissionContext, files
    ) -> OrderRead | None:
        from app.schemas.company_schema import CompanyRead
        from app.services.company_service import CompanyService

        company_service = CompanyService(self.db)
        company_data: CompanyRead = company_service.get_by_id(str(ctx.user.company_id))

        if not company_data.drive_folder_id or company_data.folder_status != "CREATED":
            raise ValidationError(message=f"Drive Error")

        drive_folder: str = company_data.drive_folder_id

        order_price: float = 0.0

        try:
            order = OrderModel(
                created_by=str(ctx.user.user_id), company_id=str(ctx.user.company_id)
            )
            order = self.__add_to_db(order, self.db)

            if order:
                for item, file in zip(order_data.items, files):
                    # Create order item
                    order_item = self.__order_item_create(order.id, item, file, self.db)

                    order_price += order_item.item_price
                    # Process and save file
                    file_name, file_path = self.__process_file(file)

                    # Create uploaded file record
                    uploaded_file = UploadedFileDb(
                        file_name=file_name,
                        status="pending",
                        order_item_id=order_item.id,
                        parent_drive_folder=str(drive_folder),
                    )
                    uploaded_file_id = self.__add_to_db(uploaded_file, self.db).id

                    # CRITICAL: Commit here so Celery can find the record
                    self.db.commit()
                    self.db.refresh(uploaded_file)

                    # Dispatch Celery task - ensure ID is string
                    task = process_file_upload.delay(
                        uploaded_file_id=str(uploaded_file_id),
                        file_name=file_name,
                        file_path=str(file_path),
                    )

                # Final commit for the order
                order.order_price = order_price

                self.db.commit()
                self.db.refresh(order)

                return OrderRead.from_orm(order)

        except Exception as e:
            self.db.rollback()

            # Clean up any uploaded files on failure
            try:
                for file in files:
                    file.file.seek(0)  # Reset file pointer
            except:
                pass

            raise e

        def get_orders_by_company(company_id: str):
            return
