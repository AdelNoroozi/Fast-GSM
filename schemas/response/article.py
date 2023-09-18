from datetime import datetime

from pydantic import BaseModel


class GetArticleModel(BaseModel):
    id: int
    title: str
    author: str
    head_photo_url: str


class RetrieveArticleModel(GetArticleModel):
    created_at: datetime
    content: str
