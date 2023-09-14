from pydantic import BaseModel


class BrandListModel(BaseModel):
    id: int
    name: str
    logo_url: str
