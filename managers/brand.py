from sqlalchemy import select
from asyncpg import UniqueViolationError
from fastapi import HTTPException

from db import database
from models import brand


class BrandManager:
    @staticmethod
    async def create_brand(brand_data):
        try:
            query = brand.insert().values(**brand_data)
            id_ = await database.execute(query)
        except UniqueViolationError:
            raise HTTPException(401, "brand already exists")
        brand_instance = await database.fetch_one(brand.select().where(brand.c.id == id_))
        return brand_instance

    @staticmethod
    async def list_brand():
        query = brand.select()
        return await database.fetch_all(query)

    @staticmethod
    async def list_brand_for_filter():
        query = select([brand.c.id, brand.c.name.label("option"), brand.c.logo_url])
        return await database.fetch_all(query)
