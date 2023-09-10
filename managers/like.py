from fastapi import HTTPException

from db import database
from managers import MobileManager
from models import like
from asyncpg import ForeignKeyViolationError


class LikeManager:
    @staticmethod
    async def like_mobile(like_data, requesting_user):
        like_data["user_id"] = requesting_user["id"]
        try:
            db_like = await database.fetch_one(like.select().where(like.c.user_id == like_data["user_id"],
                                                                   like.c.mobile_id == like_data["mobile_id"]))
            if db_like:
                query = like.delete().where(like.c.id == db_like["id"])
                response = "like removed"
                value = -1
            else:
                query = like.insert().values(**like_data)
                response = "liked"
                value = 1
            await database.execute(query)
            await MobileManager.update_mobile_likes_count(like_data["mobile_id"], value)
        except ForeignKeyViolationError:
            raise HTTPException(404, "mobile not found")
        return response
