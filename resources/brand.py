from fastapi import APIRouter

from managers import BrandManager
from schemas.request import BrandModel

router = APIRouter(tags=["Brand"])


@router.post("/brands/", status_code=201)
async def create_brand(brand_data: BrandModel):
    brand = await BrandManager.create_brand(brand_data.model_dump())
    return brand
