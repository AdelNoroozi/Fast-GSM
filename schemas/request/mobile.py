from datetime import date

from pydantic import BaseModel


class InputPropModel(BaseModel):
    prop_id: int
    value: str


class MobilePhotoModel(BaseModel):
    photo_url: str
    alt_text: str


class CreateMobileModel(BaseModel):
    name: str
    release_date: date
    brand_id: int
    price: float
    photos: list[MobilePhotoModel]
    props: list[int]
    input_props: list[InputPropModel]
