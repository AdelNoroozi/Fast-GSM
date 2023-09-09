from fastapi import APIRouter

from managers import MobilePropManager
from schemas.response import MobilePropModel

router = APIRouter(tags=["Mobile Prop"])


@router.get("/props/", status_code=200)
async def list_props():
    return await MobilePropManager.get_props()
