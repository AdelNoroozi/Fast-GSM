from datetime import date

from pydantic import BaseModel


class InputPropModel(BaseModel):
    prop_id: int
    value: str


class CreateMobileModel(BaseModel):
    name: str
    release_date: date
    brand_id: int
    price: float
    props: list[int]
    input_props: list[InputPropModel]
