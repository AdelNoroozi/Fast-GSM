from pydantic import BaseModel


class SaveModel(BaseModel):
    mobile_id: int
