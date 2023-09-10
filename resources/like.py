from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers import oauth2_scheme, is_observer, LikeManager
from schemas.request import LikeModel

router = APIRouter(tags=["Like"])


@router.post("/likes/", status_code=200, dependencies=[Depends(oauth2_scheme), Depends(is_observer)])
async def like_mobile(like: LikeModel, request: Request):
    user = request.state.user
    response = await LikeManager.like_mobile(like.model_dump(), user)
    return {response}
