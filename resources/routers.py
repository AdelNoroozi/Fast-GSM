from fastapi import APIRouter

from resources import auth, brand, mobile

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(brand.router)
api_router.include_router(mobile.router)
