from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers import oauth2_scheme, is_observer, SaveManager
from schemas.request import SaveModel

router = APIRouter(tags=["Save"])


@router.post("/saves/", status_code=200, dependencies=[Depends(oauth2_scheme), Depends(is_observer)])
async def like_mobile(save: SaveModel, request: Request):
    user = request.state.user
    response = await SaveManager.save_mobile(save.model_dump(), user)
    return {response}
