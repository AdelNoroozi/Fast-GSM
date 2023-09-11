from typing import Optional

from asyncpg import UniqueViolationError, ForeignKeyViolationError
from fastapi import HTTPException
from sqlalchemy import desc, column

from db import database
from models import mobile, brand, comment, user, mobile_prop_selectable_value, mobile_prop_option, mobile_prop
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
    def order(cls, query, order_column):
        first_char = order_column[0]
        descending = False
        if first_char == "-":
            order_column = order_column[1:]
            descending = True
        if order_column in ["views", "likes_count", "price", "release_date"]:
            if descending:
                query = query.order_by(desc(column(order_column)))
            else:
                query = query.order_by(column(order_column))
        return query

    @classmethod
    async def update_mobile_views(cls, mobile_id):
        mobile_instance = await database.fetch_one(mobile.select().where(mobile.c.id == mobile_id))
        query = mobile.update().where(mobile.c.id == mobile_instance["id"]).values(
            views=mobile_instance["views"] + 1)
        await database.execute(query)

    @classmethod
    async def update_mobile_comments_count(cls, mobile_id):
        mobile_instance = await database.fetch_one(mobile.select().where(mobile.c.id == mobile_id))
        query = mobile.update().where(mobile.c.id == mobile_instance["id"]).values(
            comments_count=mobile_instance["comments_count"] + 1)
        await database.execute(query)

    @classmethod
    async def update_mobile_likes_count(cls, mobile_id, value):
        mobile_instance = await database.fetch_one(mobile.select().where(mobile.c.id == mobile_id))
        query = mobile.update().where(mobile.c.id == mobile_instance["id"]).values(
            likes_count=mobile_instance["likes_count"] + value)
        await database.execute(query)

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
    async def retrieve_mobile(mobile_id, requesting_user_id: Optional[int] = None):
        from managers import LikeManager
        from managers import SaveManager
        from managers import MobilePropManager
        from managers import CommentManager
        try:
            query = mobile.join(brand, mobile.c.brand_id == brand.c.id).select().where(mobile.c.id == mobile_id)
            mobile_instance = await database.fetch_one(query)
        except Exception as e:
            raise e
        if not mobile_instance:
            raise HTTPException(404, "mobile not found")
        await MobileManager.update_mobile_views(mobile_instance["id"])
        mobile_data = dict(mobile_instance)
        mobile_data["is_liked_by_user"] = await LikeManager.is_liked_by_user(mobile_id, requesting_user_id)
        mobile_data["is_saved_by_user"] = await SaveManager.is_saved_by_user(mobile_id, requesting_user_id)
        mobile_data["comments"] = await CommentManager.get_comments_by_mobile(mobile_id)
        mobile_data["props"] = await MobilePropManager.get_props_by_mobile(mobile_id)
        return mobile_data

    @staticmethod
    async def list_mobile(brand_id: Optional[id], search_str: Optional[str], order_column: Optional[str],
                          requesting_user_id: Optional[int] = None):
        from managers import LikeManager
        from managers import SaveManager
        query = mobile.select()
        if brand_id:
            query = MobileManager.filter_by_brand(query, brand_id)
        if search_str:
            query = await MobileManager.search(query, search_str)
        if order_column:
            query = MobileManager.order(query, order_column)
        mobiles = await database.fetch_all(query)
        mobile_datas = []
        for mobile_instance in mobiles:
            mobile_data = dict(mobile_instance)
            mobile_data["is_liked_by_user"] = await LikeManager.is_liked_by_user(mobile_data["id"], requesting_user_id)
            mobile_data["is_saved_by_user"] = await SaveManager.is_saved_by_user(mobile_data["id"], requesting_user_id)
            mobile_datas.append(mobile_data)
        return mobile_datas
