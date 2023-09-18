from db import database
from models import article


class ArticleManager:
    @staticmethod
    async def create_article(article_data, requesting_user):
        article_data["author_id"] = requesting_user["id"]
        query = article.insert().values(**article_data)
        id_ = await database.execute(query)
        article_data = dict(await database.fetch_one(article.select().where(article.c.id == id_)))
        article_data["author"] = requesting_user["public_name"]
        return article_data

    @staticmethod
    async def list_articles():
        query = article.select()
        return await database.fetch_all(query)
