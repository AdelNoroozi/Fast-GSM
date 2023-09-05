from enum import Enum


class RoleEnum(str, Enum):
    superuser = "superuser"
    admin = "admin"
    observer = "observer"
