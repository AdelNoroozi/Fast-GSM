from db import database
from models import comment, user, mobile


class CommentManager:
    @staticmethod
    async def create_comment(comment_data, requesting_user):
        comment_data["user_id"] = requesting_user["id"]
        query = comment.insert().values(**comment_data)
        id_ = await database.execute(query)
        response_query = (
            comment.join(user, comment.c.user_id == user.c.id)
            .join(mobile, comment.c.mobile_id == mobile.c.id)
            .select()
            .where(comment.c.id == id_)
        )
        return await database.fetch_one(response_query)
