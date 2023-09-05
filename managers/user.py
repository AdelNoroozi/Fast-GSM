from fastapi import HTTPException
from passlib import context

from db import database
from managers import AuthManager
from models import user
from asyncpg import UniqueViolationError
pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            query = user.insert().values(**user_data)
            id_ = await database.execute(query)
        except UniqueViolationError:
            raise HTTPException(401, "duplicate email")
        user_instance = await database.fetch_one(user.select().where(user.c.id == id_))
        return AuthManager.encode_token(user_instance)
