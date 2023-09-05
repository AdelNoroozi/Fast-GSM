from fastapi import APIRouter, Depends

from managers import BrandManager, oauth2_scheme, is_admin
from schemas.request import BrandModel

router = APIRouter(tags=["Brand"])


@router.post("/brands/", status_code=201,
             dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def create_brand(brand_data: BrandModel):
    brand = await BrandManager.create_brand(brand_data.model_dump())
    return brand
