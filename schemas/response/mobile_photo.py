from pydantic import BaseModel


class MobilePhotoRetrieveModel(BaseModel):
    photo_url: str
    alt_text: str
