from datetime import datetime

from pydantic import BaseModel, Field


class RetrieveCommentModel(BaseModel):
    submitted_by: str = Field(alias="public_name")
    submitted_for: str = Field(alias="name")
    submitted_at: datetime
    text: str
