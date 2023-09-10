from fastapi import APIRouter

from resources import auth, brand, mobile, comment, mobile_prop, like

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(brand.router)
api_router.include_router(mobile.router)
api_router.include_router(comment.router)
api_router.include_router(mobile_prop.router)
api_router.include_router(like.router)
