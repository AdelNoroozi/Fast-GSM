from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.requests import Request

from managers import MobileManager, oauth2_scheme, is_admin, is_authenticated
from schemas.request import CreateMobileModel
from schemas.response import RetrieveMobileModel, BaseGetMobileModel, ListMobileModel, CreateResponseMobileModel

router = APIRouter(tags=["Mobile"])


@router.get("/mobiles/", status_code=200, response_model=list[ListMobileModel],
            dependencies=[Depends(oauth2_scheme)])
async def list_mobile(request: Request, brand: Optional[int] = None, search: Optional[str] = None,
                      order_by: Optional[str] = None, props: Optional[List[int]] = Query([])):
    user = request.state.user
    if not user:
        mobiles = await MobileManager.list_mobile(brand, search, props, order_by)
    else:
        mobiles = await MobileManager.list_mobile(brand, search, props, order_by, user["id"])
    return mobiles


@router.post("/mobiles/", status_code=201, response_model=CreateResponseMobileModel, response_model_by_alias=False,
             dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def create_mobile(mobile_data: CreateMobileModel):
    mobile = await MobileManager.create_mobile(mobile_data.model_dump())
    return mobile


@router.get("/mobiles/saved/", status_code=200, response_model=list[BaseGetMobileModel],
            dependencies=[Depends(oauth2_scheme), Depends(is_authenticated)])
async def list_saved_mobiles(request: Request):
    user = request.state.user
    return await MobileManager.get_saved_mobiles(user["id"])


@router.get("/mobiles/liked/", status_code=200, response_model=list[BaseGetMobileModel],
            dependencies=[Depends(oauth2_scheme), Depends(is_authenticated)])
async def list_liked_mobiles(request: Request):
    user = request.state.user
    return await MobileManager.get_liked_mobiles(user["id"])


@router.get("/mobiles/{mobile_id}/", response_model=RetrieveMobileModel, response_model_by_alias=False, status_code=200,
            dependencies=[Depends(oauth2_scheme)])
async def retrieve_mobile(mobile_id: int, request: Request):
    user = request.state.user
    if not user:
        mobile = await MobileManager.retrieve_mobile(mobile_id)
    else:
        mobile = await MobileManager.retrieve_mobile(mobile_id, user["id"])
    if mobile is None:
        raise HTTPException(404, "mobile not found")
    return mobile
