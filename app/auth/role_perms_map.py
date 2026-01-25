"""
MAP EACH ROLE WITH ITS OWN PERMISSIONS
I KNOW ITS GOING TO BE HARDCODED
BUT F THAT
"""

from typing import Dict, Set
from app.enums.roles import Roles
from app.enums.permissions import Permissions


ROLE_PERMISSION: Dict[Roles, Set[Permissions]] = {
    Roles.ADMIN: {
        Permissions.CAN_SEE_ALL,
        Permissions.CAN_UPDATE_ALL,
        Permissions.CAN_DELETE_ALL,
        Permissions.CAN_CREATE_ALL,
        Permissions.CAN_READ_ALL,
    },
    Roles.USER: {
        Permissions.CAN_SEE_ALL,
        Permissions.CAN_READ_ALL,
        Permissions.CAN_UPDATE_ALL,
        Permissions.CAN_CREATE_ALL,
        Permissions.CAN_READ_ALL,
    },
    Roles.CLIENT: {
        Permissions.CAN_CREATE_ORDER,
        Permissions.CAN_CREATE_ITEM,
        Permissions.CAN_READ_ORDER,
        Permissions.CAN_READ_ITEM,
        Permissions.CAN_LIST_ORDERS,
        Permissions.CAN_LIST_ITEMS,
    },
}
