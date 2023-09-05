from datetime import datetime

from pydantic import BaseModel


class CreateMobileModel(BaseModel):
    name: str
    release_date: datetime
    brand_id: int
    price: float
