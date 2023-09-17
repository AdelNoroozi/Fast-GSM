from pydantic import BaseModel


class CreateArticleModel(BaseModel):
    title: str
    head_photo_url: str
    content: str
