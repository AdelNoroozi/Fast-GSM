from db import database
from managers import UserManager
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
        articles = await database.fetch_all(query)
        article_list = []
        for article_obj in articles:
            article_data = dict(article_obj)
            author_id = article_data.pop("author_id")
            article_data["author"] = (await UserManager.get_user_by_id(author_id))["public_name"]
            article_list.append(article_data)
        return article_list

    @staticmethod
    async def retrieve_article(article_id):
        query = article.select().where(article.c.id == article_id)
        article_data = dict(await database.fetch_one(query))
        author_id = article_data.pop("author_id")
        article_data["author"] = (await UserManager.get_user_by_id(author_id))["public_name"]
        return article_data
