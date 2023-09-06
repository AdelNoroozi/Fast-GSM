from datetime import datetime

from pydantic import BaseModel, EmailStr

from models import RoleEnum


class UserListModel(BaseModel):
    email: EmailStr
    password: str
    public_name: str
    role: RoleEnum
    phone_number: str
    joined_at: datetime
    modified_at: datetime
