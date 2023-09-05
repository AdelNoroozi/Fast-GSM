from datetime import date

from pydantic import BaseModel


class CreateMobileModel(BaseModel):
    name: str
    release_date: date
    brand_id: int
    price: float
