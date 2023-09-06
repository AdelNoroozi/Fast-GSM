from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib import context

from db import database
from managers import AuthManager
from models import user, RoleEnum

pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data, on_event_token):
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            query = user.insert().values(**user_data)
            id_ = await database.execute(query)
        except UniqueViolationError:
            raise HTTPException(401, "duplicate email")
        user_instance = await database.fetch_one(user.select().where(user.c.id == id_))
        if on_event_token:
            return AuthManager.encode_token(user_instance)
        else:
            return user_instance["email"]

    @staticmethod
    async def login(user_data):
        user_instance = await database.fetch_one(user.select().where(user.c.email == user_data["email"]))
        if not user_instance or not pwd_context.verify(user_data["password"], user_instance["password"]):
            raise HTTPException(401, "wrong pass or email")
        return AuthManager.encode_token(user_instance)

    @staticmethod
    async def add_admin(admin_data):
        admin_data["role"] = RoleEnum.admin.name
        return await UserManager.register(admin_data, False)

    @staticmethod
    async def get_user_list(requesting_user):
        query = user.select()
        if requesting_user["role"] == RoleEnum.admin:
            query = query.where(user.c.role == RoleEnum.observer)
        elif requesting_user["role"] == RoleEnum.observer:
            query = query.where(user.c.id == requesting_user["id"])
        return await database.fetch_all(query)
