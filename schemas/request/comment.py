from pydantic import BaseModel


class CreateCommentModel(BaseModel):
    mobile_id: int
    text: str
