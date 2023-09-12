from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from models import RoleEnum


class UserListModel(BaseModel):
    email: EmailStr
    public_name: Optional[str]
    role: Optional[RoleEnum]
    phone_number: Optional[str]
    joined_at: datetime
    modified_at: datetime
