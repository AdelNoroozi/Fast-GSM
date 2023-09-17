from datetime import datetime

from pydantic import BaseModel


class RetrieveArticleModel(BaseModel):
    id: int
    title: str
    author: str
    created_at: datetime
    head_photo_url: str
    content: str
