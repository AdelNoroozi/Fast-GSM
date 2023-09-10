from typing import Optional


from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from managers import MobileManager, oauth2_scheme, is_admin, oauth2_scheme_unprotected
from schemas.request import CreateMobileModel
from schemas.response import RetrieveMobileModel, BaseGetMobileModel

router = APIRouter(tags=["Mobile"])


@router.post("/mobiles/", status_code=201, response_model=RetrieveMobileModel, response_model_by_alias=False,
             dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def create_mobile(mobile_data: CreateMobileModel):
    mobile = await MobileManager.create_mobile(mobile_data.model_dump())
    return mobile


@router.get("/mobiles/{mobile_id}/", response_model=RetrieveMobileModel, response_model_by_alias=False, status_code=200,
            dependencies=[Depends(oauth2_scheme_unprotected)])
async def retrieve_mobile(mobile_id: int, request: Request):
    try:
        user = request.state.user
    except AttributeError:
        mobile = await MobileManager.retrieve_mobile(mobile_id, None)
    else:
        mobile = await MobileManager.retrieve_mobile(mobile_id, user["id"])
    if mobile is None:
        raise HTTPException(404, "mobile not found")
    return mobile


@router.get("/mobiles/", response_model=list[BaseGetMobileModel], status_code=200)
async def list_mobile(brand: Optional[int] = None, search: Optional[str] = None, ):
    mobiles = await MobileManager.list_mobile(brand, search)
    return mobiles
