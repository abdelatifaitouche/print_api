from enum import StrEnum



class Permissions(StrEnum):
    CAN_SEE_ALL = "CAN_SEE_ALL"
    CAN_CREATE = "CAN_CREATE"
    CAN_DELETE = "CAN_DELETE"
    CAN_UPDATE = "CAN_UDPATE"
    CAN_READ = "CAN_READ"
