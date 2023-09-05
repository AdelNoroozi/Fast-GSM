from fastapi import HTTPException

from db import database
from models import brand
from asyncpg import UniqueViolationError


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
