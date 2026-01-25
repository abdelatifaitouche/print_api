from app.auth.permission_service import PermissionService
from app.enums.permissions import Permissions
from app.schemas.user_schema import User
from app.schemas.jwt_payload import JwtPayload


class PermissionContext:
    def __init__(self, user: JwtPayload):
        self.user = user
        self.permissions: set[Permissions] = PermissionService.get_role_permissions(
            self.user.role
        )

    def has_permission(self, permission):
        if permission not in self.permissions:
            return False
        return True

    def has_any_permission(self, *permissions: Permissions):
        return any(perm in self.permissions for perm in permissions)

    def can_list_all(self):
        if Permissions.CAN_READ_ALL in self.permissions:
            return None
        return self.user.user_id

    def __is_resource_owner(self, resource_owner_id: str) -> bool:
        if self.user.user_id == resource_owner_id:
            return True
        return False

    def can_access_resource(self, resource_owner_id):
        if self.can_list_all() is not None:
            return self.__is_resource_owner(resource_owner_id)
        else:
            return True

    def is_memeber(self, org_id: str):
        if self.can_list_all() is not None:
            return self.user.company_id == org_id
        return True
