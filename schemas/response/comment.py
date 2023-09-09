from datetime import datetime

from pydantic import BaseModel, Field


class BaseCommentModel(BaseModel):
    submitted_by: str = Field(alias="public_name")
    submitted_at: datetime
    text: str


class RetrieveCommentModel(BaseCommentModel):
    submitted_for: str = Field(alias="name")
