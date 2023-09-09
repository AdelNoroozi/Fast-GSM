from datetime import date

from pydantic import BaseModel, Field


class BaseGetMobileModel(BaseModel):
    name: str
    price: float


class RetrieveMobileModel(BaseModel):
    name: str
    release_date: date
    brand: str = Field(alias="name_1")
    price: float
    comments: list
