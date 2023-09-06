from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers import oauth2_scheme, CommentManager
from schemas.request import CreateCommentModel
from schemas.response import RetrieveCommentModel

router = APIRouter(tags=["Comment"])


@router.post("/comments/", status_code=201, response_model=RetrieveCommentModel, response_model_by_alias=False,
             dependencies=[Depends(oauth2_scheme)])
async def create_comment(comment: CreateCommentModel, request: Request):
    user = request.state.user
    return await CommentManager.create_comment(comment.model_dump(), user)
