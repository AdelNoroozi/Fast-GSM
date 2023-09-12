from datetime import date

from pydantic import BaseModel, Field


class BaseGetMobileModel(BaseModel):
    id: int
    name: str
    price: float
    views: int
    likes_count: int
    comments_count: int


class ListMobileModel(BaseGetMobileModel):
    is_liked_by_user: bool
    is_saved_by_user: bool


class CreateResponseMobileModel(BaseGetMobileModel):
    id: int
    name: str
    price: float
    release_date: date
    brand: str = Field(alias="name_1")


class RetrieveMobileModel(ListMobileModel):
    release_date: date
    brand: str = Field(alias="name_1")
    comments: list
    props: dict
