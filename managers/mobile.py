from asyncpg import UniqueViolationError
from fastapi import HTTPException

from db import database
from models import mobile


class MobileManager:
    @staticmethod
    async def create_mobile(mobile_data):
        try:
            query = mobile.insert().values(**mobile_data)
            id_ = await database.execute(query)
        except UniqueViolationError:
            raise HTTPException(400, "mobile already exists")
        mobile_instance = await database.fetch_one(mobile.select().where(mobile.c.id == id_))
        return mobile_instance
