from pydantic import BaseModel


class MobilePhotoModel(BaseModel):
    photo_url: str
    alt_text: str
