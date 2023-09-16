from fastapi import APIRouter

from managers import MobilePropManager
from schemas.request import CreatePropModel

router = APIRouter(tags=["Mobile Prop"])


@router.get("/props/", status_code=200)
async def list_props():
    return await MobilePropManager.get_props()


@router.post("/props/", status_code=201)
async def list_props(prop_data: CreatePropModel):
    return await MobilePropManager.create_props(prop_data.model_dump())
