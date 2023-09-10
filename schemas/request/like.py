from pydantic import BaseModel


class LikeModel(BaseModel):
    mobile_id: int
