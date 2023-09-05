from fastapi import APIRouter

from managers import MobileManager
from schemas.request import CreateMobileModel

router = APIRouter(tags=["Mobile"])


@router.post("/mobiles/")
async def create_mobile(mobile_data: CreateMobileModel):
    mobile = await MobileManager.create_mobile(mobile_data.model_dump())
    return mobile
