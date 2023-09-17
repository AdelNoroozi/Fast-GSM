from datetime import date
from pydantic import BaseModel
from schemas.request import MobilePhotoModel, InputPropModel


class CreateMobileModel(BaseModel):
    name: str
    release_date: date
    brand_id: int
    price: float
    photos: list[MobilePhotoModel]
    props: list[int]
    input_props: list[InputPropModel]
