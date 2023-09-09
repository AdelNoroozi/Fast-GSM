from pydantic import BaseModel


class MobilePropModel(BaseModel):
    prop: str
