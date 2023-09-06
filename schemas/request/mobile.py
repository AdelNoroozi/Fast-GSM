from datetime import date

from pydantic import BaseModel, Field


class CreateMobileModel(BaseModel):
    name: str
    release_date: date
    brand_id: int
    price: float

