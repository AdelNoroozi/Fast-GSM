from asyncpg import UniqueViolationError, ForeignKeyViolationError
from fastapi import HTTPException

from db import database
from models import mobile, brand


class MobileManager:
    @staticmethod
    async def create_mobile(mobile_data):
        try:
            query = mobile.insert().values(**mobile_data)
            id_ = await database.execute(query)
        except UniqueViolationError:
            raise HTTPException(400, "mobile already exists")
        except ForeignKeyViolationError:
            raise HTTPException(404, "brand does not exist")
        retrieve_query = mobile.join(brand, mobile.c.brand_id == brand.c.id).select().where(mobile.c.id == id_)
        mobile_instance = await database.fetch_one(retrieve_query)
        return mobile_instance

    @staticmethod
    async def retrieve_mobile(mobile_id):
        try:
            query = mobile.join(brand, mobile.c.brand_id == brand.c.id).select().where(mobile.c.id == mobile_id)
        except Exception as e:
            raise e
        mobile_instance = await database.fetch_one(query)
        return mobile_instance

    @staticmethod
    async def list_mobile():
        query = mobile.selecct()
        return await database.fetch_all(query)
