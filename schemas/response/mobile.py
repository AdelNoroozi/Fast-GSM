from datetime import date

from pydantic import BaseModel, Field


class RetrieveMobileModel(BaseModel):
    name: str
    release_date: date
    brand: str = Field(alias="name_1")
    price: float
