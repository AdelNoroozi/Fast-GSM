from fastapi import APIRouter, Depends

from managers import MobilePropManager, is_admin, oauth2_scheme
from schemas.request import CreatePropModel

router = APIRouter(tags=["Mobile Prop"])


@router.get("/props/", status_code=200)
async def list_props():
    return await MobilePropManager.get_props()


@router.post("/props/", status_code=201, dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def list_props(prop_data: CreatePropModel):
    return await MobilePropManager.create_props(prop_data.model_dump())
