from fastapi import APIRouter, Depends
from starlette.requests import Request
from fastapi_pagination import Page, paginate
from managers import ArticleManager, oauth2_scheme, is_blog_author
from schemas.request import CreateArticleModel
from schemas.response import RetrieveArticleModel, GetArticleModel

router = APIRouter(tags=["Article"])


@router.post("/articles/", status_code=201, response_model=RetrieveArticleModel,
             dependencies=[Depends(oauth2_scheme), Depends(is_blog_author)])
async def create_article(article: CreateArticleModel, request: Request):
    user = request.state.user
    return await ArticleManager.create_article(article.model_dump(), user)


@router.get("/articles/", status_code=200, response_model=Page[GetArticleModel])
async def list_articles():
    articles = await ArticleManager.list_articles()
    return paginate(articles)
