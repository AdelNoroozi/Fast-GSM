from fastapi import HTTPException

from db import database
from models import save
from asyncpg import ForeignKeyViolationError


class SaveManager:
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
        except ForeignKeyViolationError:
            raise HTTPException(404, "mobile not found")
        await database.execute(query)
        return response
