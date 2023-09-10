from datetime import date

from pydantic import BaseModel, Field


class BaseGetMobileModel(BaseModel):
    id: int
    name: str
    price: float
    views: int
    likes_count: int
    comments_count: int
    is_liked_by_user: bool


class RetrieveMobileModel(BaseGetMobileModel):
    release_date: date
    brand: str = Field(alias="name_1")
    comments: list
    props: dict
