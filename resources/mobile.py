from fastapi import APIRouter, Depends

from managers import MobileManager, oauth2_scheme, is_admin
from schemas.request import CreateMobileModel, RetrieveMobileModel

router = APIRouter(tags=["Mobile"])


@router.post("/mobiles/", status_code=201, response_model=RetrieveMobileModel, response_model_by_alias=False,
             dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def create_mobile(mobile_data: CreateMobileModel):
    mobile = await MobileManager.create_mobile(mobile_data.model_dump())
    return mobile
