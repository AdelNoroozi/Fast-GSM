from fastapi import HTTPException

from db import database
from models import like
from asyncpg import ForeignKeyViolationError


class LikeManager:
    @staticmethod
    async def like_mobile(like_data, requesting_user):
        like_data["user_id"] = requesting_user["id"]
        try:
            query = like.insert().values(**like_data)
            await database.execute(query)
        except ForeignKeyViolationError:
            raise HTTPException(404, "mobile not found")
