from db import database
from models import mobile_photo
from schemas.response import MobilePhotoRetrieveModel


class MobilePhotoManager:
    @staticmethod
    async def get_photos_by_mobile(mobile_id):
        query = mobile_photo.select().where(mobile_photo.c.mobile_id == mobile_id)
        photo_objects = await database.fetch_all(query)
        photos = [MobilePhotoRetrieveModel(**photo) for photo in photo_objects]
        return photos

    @staticmethod
    async def create_photos(mobile_id, photos):
        is_thumbnail = True
        for photo in photos:
            query = mobile_photo.insert().values({
                "mobile_id": mobile_id,
                "photo_url": photo["photo_url"],
                "alt_text": photo["alt_text"],
                "is_thumbnail": is_thumbnail
            })
            await database.execute(query)
            if is_thumbnail:
                is_thumbnail = False
