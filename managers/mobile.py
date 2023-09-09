from typing import Optional

from asyncpg import UniqueViolationError, ForeignKeyViolationError
from fastapi import HTTPException

from db import database
from models import mobile, brand, comment, user
from schemas.response import BaseCommentModel


class MobileManager:

    @classmethod
    async def search(cls, query, search_str):
        mobile_by_name_res = query.where(mobile.c.name.ilike(f"%{search_str}%"))
        brands_query = brand.select().where(brand.c.name.ilike(f"%{search_str}%"))
        brands = await database.fetch_all(brands_query)
        brand_ids = [b["id"] for b in brands]
        mobile_by_brand_res = query.where(mobile.c.brand_id.in_(brand_ids))
        return mobile_by_name_res.union(mobile_by_brand_res)

    @classmethod
    def filter_by_brand(cls, query, brand_id):
        return query.where(mobile.c.brand_id == brand_id)

    @classmethod
    async def get_comments(cls, mobile_id):
        query = comment.join(user, user.c.id == comment.c.user_id).select().where(mobile.c.id == mobile_id)
        comments = await database.fetch_all(query)
        return [BaseCommentModel(**c) for c in comments]

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
        mobile_data = dict(await database.fetch_one(query))
        comments = await MobileManager.get_comments(mobile_id)
        mobile_data["comments"] = comments
        return mobile_data

    @staticmethod
    async def list_mobile(brand_id: Optional[id], search_str: Optional[str]):
        query = mobile.select()
        if brand_id:
            query = MobileManager.filter_by_brand(query, brand_id)
        if search_str:
            query = await MobileManager.search(query, search_str)
        return await database.fetch_all(query)
