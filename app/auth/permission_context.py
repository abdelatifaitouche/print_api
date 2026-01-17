from app.enums.permissions import Permissions
from app.enums.roles import Roles
from app.auth.permission_service import PermissionService
class PermissionContext : 
    def __init__(self , user_id : str , role : Roles):
        self.user_id : str = user_id
        self.role : Roles = role
        self.permissions : set[Roles] = PermissionService.get_permissions_for_role(role)
    
    def has_permission(self , permission : Permissions)->bool:
        return True if permission in self.permissions else False
    
    def has_all_permissions(self , *permissions : Permissions)->bool:
        """
            this one might cause me some confusion later,
            what's happening is am just checking if the user
            has all the permissions in the permissions parameter that we passed

            dont get angry at this, take a lil bit of time to read it (dont smoke)
        """    
        return all(permission in self.permissions for permission in permissions )
            
    def can_see_all(self):
        """
            Just checking if the user can list everything, or if he is an admin
        """    
        return True if Permissions.CAN_SEE_ALL in self.permissions or self.role == Roles.ADMIN else False

    def get_ownership(self)->str:
        """
            checks if he can see all (which is for sure for an admin),
            otherwise just return the user id to filter later 
        """
        return None if self.can_see_all() else self.user_id

    def has_role(self , role : Roles):
        return True if self.role == role else False


