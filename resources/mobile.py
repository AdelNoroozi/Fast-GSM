from fastapi import APIRouter, Depends, HTTPException

from managers import MobileManager, oauth2_scheme, is_admin
from schemas.request import CreateMobileModel
from schemas.response import RetrieveMobileModel

router = APIRouter(tags=["Mobile"])


@router.post("/mobiles/", status_code=201, response_model=RetrieveMobileModel, response_model_by_alias=False,
             dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def create_mobile(mobile_data: CreateMobileModel):
    mobile = await MobileManager.create_mobile(mobile_data.model_dump())
    return mobile


@router.get("/mobiles/{mobile_id}/", response_model=RetrieveMobileModel, response_model_by_alias=False, status_code=200)
async def retrieve_mobile(mobile_id: int):
    mobile = await MobileManager.retrieve_mobile(mobile_id)
    if mobile is None:
        raise HTTPException(404, "mobile not found")
    return mobile
