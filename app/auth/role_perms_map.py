"""
    MAP EACH ROLE WITH ITS OWN PERMISSIONS
    I KNOW ITS GOING TO BE HARDCODED
    BUT F THAT 
"""


from typing import Dict , Set
from app.enums.roles import Roles
from app.enums.permissions import Permissions


ROLE_PERMISSION : Dict[Roles , Set[Permissions]] = {
   
    Roles.ADMIN : {
        Permissions.CAN_SEE_ALL ,
        Permissions.CAN_READ ,
        Permissions.CAN_UPDATE ,
        Permissions.CAN_DELETE ,
        Permissions.CAN_CREATE
        },
    Roles.USER : {
        Permissions.CAN_SEE_ALL , 
        Permissions.CAN_READ , 
        Permissions.CAN_UPDATE, 
        Permissions.CAN_CREATE
    } , 
    Roles.CLIENT : {
        Permissions.CAN_CREATE ,
        Permissions.CAN_READ , 
        Permissions.CAN_UPDATE,
        Permissions.CAN_DELETE , 
    }

}



