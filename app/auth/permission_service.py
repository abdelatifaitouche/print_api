from .role_perms_map import ROLE_PERMISSION
from app.enums.roles import Roles
from app.enums.permissions import Permissions


class PermissionService:
    @staticmethod
    def get_role_permissions(role: Roles) -> set[Permissions]:
        return ROLE_PERMISSION[role]

    @staticmethod
    def has_permission(role: Roles, permission: Permissions):
        if permission not in PermissionService.get_role_permissions(role):
            return False
        return True
