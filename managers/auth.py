from datetime import datetime, timedelta
from typing import Optional

import jwt
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from db import database
from models import user, RoleEnum


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user["id"],
                "exp": datetime.now() + timedelta(minutes=120)
            }
            return jwt.encode(payload, config("JWT_SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            raise e


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)
        try:
            payload = jwt.decode(res.credentials, config("JWT_SECRET_KEY"), algorithms=["HS256"])
            user_instance = await database.fetch_one(user.select().where(user.c.id == payload["sub"]))
            request.state.user = user_instance
            return user_instance
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "invalid token")


oauth2_scheme = CustomHTTPBearer()


async def is_admin(request: Request):
    user = request.state.user
    if not user or (not user["role"] == RoleEnum.admin):
        raise HTTPException(403, "you don't have permission")
