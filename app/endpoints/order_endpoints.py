from fastapi import APIRouter, UploadFile, File, HTTPException, Form, status
from app.schemas.order_schema import OrderCreate, OrderRead
from app.config.database import get_db
from fastapi import Depends
from app.services.order_service import OrderService
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.utils.private_route import PrivateRoute
from app.utils.google_drive_manager import GoogleDriveManager
from app.enums.permissions import Permissions
from app.enums.roles import Roles
import json
from app.schemas.user_schema import User
from app.auth.role_perms_map import ROLE_PERMISSION
from app.auth.permissions_api import require_permission
from app.auth.permission_context import PermissionContext

order_endpoint = APIRouter()

gdm = GoogleDriveManager()


def get_service(db: Session = Depends(get_db)):
    return OrderService(db)


@order_endpoint.get("/", response_model=list[OrderRead])
def list_orders(
    order_service: OrderService = Depends(get_service),
    ctx: PermissionContext = Depends(
        require_permission(Permissions.CAN_READ_ALL, Permissions.CAN_READ_ORDER)
    ),
):
    if ctx.can_list_all() is not None:
        orders = order_service.list(user_id=str(ctx.user.user_id))
    else:
        orders = order_service.list()
    return orders


@order_endpoint.get("/user/{user_id}", response_model=List[OrderRead])
def get_orders_by_user(
    user_id: str,
    user: User = Depends(PrivateRoute()),
    order_service: OrderService = Depends(get_service),
):
    orders = order_service.list(user)
    print(orders)
    return orders


@order_endpoint.get("/{order_id}", response_model=OrderRead)
def get_order_by_id(
    order_id: str,
    order_service: OrderService = Depends(get_service),
    ctx: PermissionContext = Depends(
        require_permission(Permissions.CAN_READ_ALL, Permissions.CAN_READ_ORDER)
    ),
):
    order = order_service.get_by_id(order_id)

    if not ctx.can_access_resource(order.created_by):
        raise HTTPException(
            detail="Can't access resource", status_code=status.HTTP_401_UNAUTHORIZED
        )

    return order


@order_endpoint.post("/", response_model=OrderRead)
def create_order(
    items_data: Annotated[str, Form(...)],
    files: List[UploadFile] = File(...),
    order_service: OrderService = Depends(get_service),
    ctx: PermissionContext = Depends(
        require_permission(Permissions.CAN_CREATE_ALL, Permissions.CAN_CREATE_ORDER)
    ),
) -> OrderRead:
    print(ctx.user.company_id)
    try:
        raw_data = json.loads(items_data)
        order_data = OrderCreate(items=raw_data)
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(422, f"invalid format for the order items")

    if len(files) != len(order_data.items):
        raise HTTPException(422, "Number of file doesnt match the items")

    order = order_service.create(order_data, ctx, files)
    return order


@order_endpoint.delete("/{order_id}")
def delete_order(
    order_id: str,
    order_service: OrderService = Depends(get_service),
    ctx: PermissionContext = Depends(require_permission(Permissions.CAN_DELETE_ALL)),
):
    order = order_service.delete(order_id)

    return order
