from app.auth.role_perms_map import ROLE_PERMISSION
from app.enums.roles import Roles
from app.enums.permissions import Permissions


class PermissionService : 
    

    @staticmethod
    def get_permissions_for_role(role : Roles)->set[Permissions]:
        return ROLE_PERMISSION.get(role , set())
