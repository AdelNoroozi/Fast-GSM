from datetime import date

from pydantic import BaseModel, Field


class BaseGetMobileModel(BaseModel):
    id: int
    name: str
    price: float
    views: int


class RetrieveMobileModel(BaseModel):
    name: str
    release_date: date
    brand: str = Field(alias="name_1")
    price: float
    comments: list
    props: dict
    views: int
