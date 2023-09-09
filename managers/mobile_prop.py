from db import database
from models import mobile_prop


class MobilePropManager:
    @staticmethod
    async def get_props():
        query = mobile_prop.select()
        return await database.fetch_all(query)