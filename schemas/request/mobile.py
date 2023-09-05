from datetime import date

from pydantic import BaseModel, Field


class CreateMobileModel(BaseModel):
    name: str
    release_date: date
    brand_id: int
    price: float


class RetrieveMobileModel(BaseModel):
    name: str
    release_date: date
    brand: str = Field(alias="name_1")
    price: float
