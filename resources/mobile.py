from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, paginate
from starlette.requests import Request

from managers import MobileManager, oauth2_scheme, is_admin
from schemas.request import CreateMobileModel
from schemas.response import RetrieveMobileModel, ListMobileModel
from utils import SETS

router = APIRouter(tags=["Mobile"])

MIN_PRICE_VALUE = 0
MAX_PRICE_VALUE = 10000


@router.get("/mobiles/", status_code=200, response_model=Page[ListMobileModel],
            dependencies=[Depends(oauth2_scheme)])
async def list_mobile(request: Request, set_: Optional[SETS] = SETS.all, brand: Optional[int] = None,
                      search: Optional[str] = None, order_by: Optional[str] = None,
                      props: Optional[List[int]] = Query([]), price_gt: Optional[float] = MIN_PRICE_VALUE,
                      price_lt: Optional[float] = MAX_PRICE_VALUE):
    user = request.state.user
    if not user:
        if set_ != SETS.all:
            raise HTTPException(403, "not allowed")
        mobiles = await MobileManager.list_mobile(brand, search, props, order_by, price_gt, price_lt, set_)
    else:
        mobiles = await MobileManager.list_mobile(brand, search, props, order_by, price_gt, price_lt, set_, user["id"])
    return paginate(mobiles)


@router.post("/mobiles/", status_code=201, dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def create_mobile(mobile_data: CreateMobileModel):
    mobile = await MobileManager.create_mobile(mobile_data.model_dump())
    return mobile


@router.post("/mobiles/compare/", status_code=200, dependencies=[Depends(oauth2_scheme)])
async def compare_mobiles(mobile_id1: int, mobile_id2: int):
    mobile = await MobileManager.compare_mobiles(mobile_id1=mobile_id1, mobile_id2=mobile_id2)
    return mobile


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
