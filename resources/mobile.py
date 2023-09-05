from fastapi import APIRouter

from managers import MobileManager
from schemas.request import CreateMobileModel, RetrieveMobileModel

router = APIRouter(tags=["Mobile"])


@router.post("/mobiles/", status_code=201, response_model=RetrieveMobileModel, response_model_by_alias=False)
async def create_mobile(mobile_data: CreateMobileModel):
    mobile = await MobileManager.create_mobile(mobile_data.model_dump())
    return mobile
