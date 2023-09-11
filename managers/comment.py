from asyncpg import ForeignKeyViolationError
from fastapi import HTTPException

from db import database
from managers import MobileManager
from models import comment, user, mobile
from schemas.response import BaseCommentModel


class CommentManager:
    @staticmethod
    async def get_comments_by_mobile(mobile_id):
        query = comment.join(user, user.c.id == comment.c.user_id).select().where(comment.c.mobile_id == mobile_id)
        comments = await database.fetch_all(query)
        return [BaseCommentModel(**c) for c in comments]

    @staticmethod
    async def create_comment(comment_data, requesting_user):
        comment_data["user_id"] = requesting_user["id"]
        try:
            query = comment.insert().values(**comment_data)
            id_ = await database.execute(query)
        except ForeignKeyViolationError:
            raise HTTPException(404, "mobile not found")
        await MobileManager.update_mobile_comments_count(comment_data["mobile_id"])
        response_query = (
            comment.join(user, comment.c.user_id == user.c.id)
            .join(mobile, comment.c.mobile_id == mobile.c.id)
            .select()
            .where(comment.c.id == id_)
        )
        return await database.fetch_one(response_query)
