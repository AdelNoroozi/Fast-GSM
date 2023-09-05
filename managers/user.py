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

    @staticmethod
    async def login(user_data):
        user_instance = await database.fetch_one(user.select().where(user.c.email == user_data["email"]))
        if not user_instance or not pwd_context.verify(user_data["password"], user_instance["password"]):
            raise HTTPException(401, "wrong pass or email")
        return AuthManager.encode_token(user_instance)
