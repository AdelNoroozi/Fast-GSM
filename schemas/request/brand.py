from pydantic import BaseModel


class BrandModel(BaseModel):
    name: str
    logo_url: str
