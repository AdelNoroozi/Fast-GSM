from fastapi import HTTPException

from db import database
from models import like
from asyncpg import ForeignKeyViolationError


class LikeManager:
    @staticmethod
    async def like_mobile(like_data, requesting_user):
        like_data["user_id"] = requesting_user["id"]
        try:
            db_like = await database.fetch_one(like.select().where(like.c.user_id == like_data["user_id"],
                                                                   like.c.mobile_id == like_data["mobile_data"]))
            if db_like:
                query = like.delete().where(like.c.id == db_like["id"])
            else:
                query = like.insert().values(**like_data)
        except ForeignKeyViolationError:
            raise HTTPException(404, "mobile not found")
        await database.execute(query)
