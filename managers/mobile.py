from typing import Optional

from asyncpg import UniqueViolationError, ForeignKeyViolationError
from fastapi import HTTPException
from sqlalchemy import desc, column, or_, and_

from db import database
from managers import BrandManager
from models import mobile, brand
from utils import SETS


class MobileManager:

    @classmethod
    async def search(cls, query, search_str):
        name_condition = mobile.c.name.ilike(f"%{search_str}%")
        brands_query = brand.select().where(brand.c.name.ilike(f"%{search_str}%"))
        brands = await database.fetch_all(brands_query)
        brand_ids = [b["id"] for b in brands]
        brand_condition = mobile.c.brand_id.in_(brand_ids)
        search_condition = or_(name_condition, brand_condition)
        mobile_by_name_res = query.where(search_condition)
        return mobile_by_name_res

    @classmethod
    def filter_by_brand(cls, query, brand_id):
        return query.where(mobile.c.brand_id == brand_id)

    @classmethod
    async def filter_by_price(cls, query, price_gt, price_lt):
        return query.where(mobile.c.price >= price_gt, mobile.c.price <= price_lt)

    @classmethod
    async def filter_by_props(cls, query, prop_ids):
        from managers import MobilePropManager
        prop_data = await MobilePropManager.get_props_by_ids(prop_ids)
        prop_values = prop_data["prop_values"]
        counts = {}
        for prop_value in prop_values:
            if prop_value["mobile_id"] in counts:
                counts[prop_value["mobile_id"]] = counts[prop_value["mobile_id"]] + 1
            else:
                counts[prop_value["mobile_id"]] = 1
        mobile_ids = []
        for id_, count in counts.items():
            if count == prop_data["prop_count"]:
                mobile_ids.append(id_)
        return query.where(mobile.c.id.in_(mobile_ids))

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
        from managers import MobilePropManager
        from managers import MobilePhotoManager
        props = mobile_data.pop("props")
        input_props = mobile_data.pop("input_props")
        photos = mobile_data.pop("photos")
        try:
            query = mobile.insert().values(**mobile_data)
            id_ = await database.execute(query)
        except UniqueViolationError:
            raise HTTPException(400, "mobile already exists")
        except ForeignKeyViolationError:
            raise HTTPException(404, "brand does not exist")
        await MobilePhotoManager.create_photos(id_, photos)
        await MobilePropManager.create_selectable_prop_values(id_, props)
        await MobilePropManager.create_input_prop_values(id_, input_props)
        return await MobileManager.retrieve_mobile(id_, None)

    @staticmethod
    async def retrieve_mobile(mobile_id, requesting_user_id: Optional[int] = None):
        from managers import LikeManager
        from managers import SaveManager
        from managers import MobilePropManager
        from managers import CommentManager
        from managers import MobilePhotoManager
        try:
            query = mobile.select().where(mobile.c.id == mobile_id)
            mobile_instance = await database.fetch_one(query)
        except Exception as e:
            raise e
        if not mobile_instance:
            raise HTTPException(404, "mobile not found")
        await MobileManager.update_mobile_views(mobile_instance["id"])
        mobile_data = dict(mobile_instance)
        mobile_data["brand"] = dict(await BrandManager.get_brand_by_id(mobile_data["brand_id"]))
        mobile_data["photos"] = await MobilePhotoManager.get_photos_by_mobile(mobile_id)
        mobile_data["is_liked_by_user"] = await LikeManager.is_liked_by_user(mobile_id, requesting_user_id)
        mobile_data["is_saved_by_user"] = await SaveManager.is_saved_by_user(mobile_id, requesting_user_id)
        mobile_data["comments"] = await CommentManager.get_comments_by_mobile(mobile_id)
        mobile_data["props"] = await MobilePropManager.get_props_by_mobile(mobile_id)
        mobile_data["input_props"] = await MobilePropManager.get_input_props_by_mobile(mobile_id)
        return mobile_data

    @staticmethod
    async def list_mobile(brand_id: Optional[id], search_str: Optional[str], prop_ids: Optional[list[int]],
                          order_column: Optional[str], price_gt: Optional[float], price_lt: Optional[float],
                          set_: Optional[SETS], requesting_user_id: Optional[int] = None):
        from managers import LikeManager
        from managers import SaveManager
        from managers import MobilePhotoManager
        query = mobile.select()
        if set_ == SETS.liked:
            query = await MobileManager.get_liked_mobiles(query, requesting_user_id)
        elif set_ == SETS.saved:
            query = await MobileManager.get_saved_mobiles(query, requesting_user_id)
        if brand_id:
            query = MobileManager.filter_by_brand(query, brand_id)
        if search_str:
            query = await MobileManager.search(query, search_str)
        if prop_ids:
            query = await MobileManager.filter_by_props(query, prop_ids)
        query = await MobileManager.filter_by_price(query, price_gt=price_gt, price_lt=price_lt)
        if order_column:
            query = MobileManager.order(query, order_column)

        mobiles = await database.fetch_all(query)
        mobile_datas = []
        for mobile_instance in mobiles:
            mobile_data = dict(mobile_instance)
            mobile_data["thumbnail"] = dict(await MobilePhotoManager.get_thumbnail_by_mobile(mobile_data["id"]))
            mobile_data["is_liked_by_user"] = await LikeManager.is_liked_by_user(mobile_data["id"], requesting_user_id)
            mobile_data["is_saved_by_user"] = await SaveManager.is_saved_by_user(mobile_data["id"], requesting_user_id)
            mobile_datas.append(mobile_data)
        return mobile_datas

    @staticmethod
    async def get_saved_mobiles(query, user_id):
        from managers import SaveManager
        saves = await SaveManager.get_saves_by_user(user_id)
        mobile_ids = [s["mobile_id"] for s in saves]
        return query.where(mobile.c.id.in_(mobile_ids))

    @staticmethod
    async def get_liked_mobiles(query, user_id):
        from managers import LikeManager
        likes = await LikeManager.get_likes_by_user(user_id)
        mobile_ids = [s["mobile_id"] for s in likes]
        return query.where(mobile.c.id.in_(mobile_ids))

    @staticmethod
    async def compare_mobiles(mobile_id1, mobile_id2):
        from managers import MobilePropManager
        from managers import MobilePhotoManager
        try:
            query1 = mobile.select().where(mobile.c.id == mobile_id1)
            query2 = mobile.select().where(mobile.c.id == mobile_id2)
            mobile_instance1 = await database.fetch_one(query1)
            mobile_instance2 = await database.fetch_one(query2)
        except Exception as e:
            raise e
        if not mobile_instance1 or not mobile_instance2:
            raise HTTPException(404, "mobile not found")
        props_mobile1 = await MobilePropManager.get_props_by_mobile(mobile_id1)
        props_mobile2 = await MobilePropManager.get_props_by_mobile(mobile_id2)
        common_props = set(props_mobile1.keys()) & set(props_mobile2.keys())
        unique_props_mobile1 = set(props_mobile1.keys()) - common_props
        unique_props_mobile2 = set(props_mobile2.keys()) - common_props
        compare_dict = {prop: (props_mobile1[prop], props_mobile2[prop]) for prop in common_props}
        compare_dict["thumbnails"] = [
            dict(await MobilePhotoManager.get_thumbnail_by_mobile(mobile_id1)),
            dict(await MobilePhotoManager.get_thumbnail_by_mobile(mobile_id2)),
                                      ]
        compare_dict["prices"] = [mobile_instance1["price"], mobile_instance2["price"]]
        comparison_result = {
            "compare_dict": compare_dict,
            "unique_props_mobile1": {prop: props_mobile1[prop] for prop in unique_props_mobile1},
            "unique_props_mobile2": {prop: props_mobile2[prop] for prop in unique_props_mobile2}
        }
        return comparison_result
