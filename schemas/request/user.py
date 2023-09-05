from pydantic import BaseModel, field_validator, EmailStr

from schemas import password_schema


class RegisterModel(BaseModel):
    email: EmailStr
    password: str
    public_name: str

    @field_validator("password")
    def validate_password(cls, value):
        if password_schema.validate(value):
            return value
        else:
            raise ValueError(
                "password length must be at least 8 and it must contain at least 1 lowercase letter and 1 number with \
                 no spaces"
            )


class LoginModel(BaseModel):
    email: EmailStr
    password: str
