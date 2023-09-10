from typing import Optional

from asyncpg import UniqueViolationError, ForeignKeyViolationError
from fastapi import HTTPException

from db import database
from models import mobile, brand, comment, user, mobile_prop_selectable_value, mobile_prop_option, mobile_prop
from schemas.response import BaseCommentModel, BaseGetMobileModel


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
        query = comment.join(user, user.c.id == comment.c.user_id).select().where(comment.c.mobile_id == mobile_id)
        comments = await database.fetch_all(query)
        return [BaseCommentModel(**c) for c in comments]

    @classmethod
    async def get_props(cls, mobile_id):
        query = mobile_prop_selectable_value.select().where(
            mobile_prop_selectable_value.c.mobile_id == mobile_id)
        mobile_prop_selectable_values = await database.fetch_all(query)
        props = {}
        for mpsv in mobile_prop_selectable_values:
            prop_value_query = mobile_prop_option.select().where(mobile_prop_option.c.id == mpsv["prop_value_id"])
            prop_value = await database.fetch_one(prop_value_query)
            prop_query = mobile_prop.select().where(mobile_prop.c.id == prop_value["prop_id"])
            prop_key = await database.fetch_one(prop_query)
            props[prop_key["prop"]] = prop_value["value"]
        return props

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
        mobile_data["comments"] = await MobileManager.get_comments(mobile_id)
        mobile_data["props"] = await MobileManager.get_props(mobile_id)
        return mobile_data

    @staticmethod
    async def list_mobile(brand_id: Optional[id], search_str: Optional[str], requesting_user_id: Optional[int] = None):
        from managers import LikeManager
        query = mobile.select()
        if brand_id:
            query = MobileManager.filter_by_brand(query, brand_id)
        if search_str:
            query = await MobileManager.search(query, search_str)
        mobiles = await database.fetch_all(query)
        mobile_datas = []
        for mobile_instance in mobiles:
            mobile_data = dict(mobile_instance)
            mobile_data["is_liked_by_user"] = await LikeManager.is_liked_by_user(mobile_data["id"], requesting_user_id)
            mobile_datas.append(mobile_data)
        return mobile_datas
