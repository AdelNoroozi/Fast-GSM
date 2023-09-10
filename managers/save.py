from typing import Optional

from fastapi import HTTPException

from db import database
from models import save
from asyncpg import ForeignKeyViolationError


class SaveManager:
    @classmethod
    async def is_saved_by_user(cls, mobile_id, user_id: Optional[int]):
        if not user_id:
            return False
        db_save = await database.fetch_one(save.select().where(save.c.user_id == user_id,
                                                               save.c.mobile_id == mobile_id))
        if db_save:
            return True
        else:
            return False

    @staticmethod
    async def save_mobile(save_data, requesting_user):
        save_data["user_id"] = requesting_user["id"]
        try:
            db_save = await database.fetch_one(save.select().where(save.c.user_id == save_data["user_id"],
                                                                   save.c.mobile_id == save_data["mobile_id"]))
            if db_save:
                query = save.delete().where(save.c.id == db_save["id"])
                response = "save removed"
            else:
                query = save.insert().values(**save_data)
                response = "saved"
            await database.execute(query)
        except ForeignKeyViolationError:
            raise HTTPException(404, "mobile not found")
        return response
