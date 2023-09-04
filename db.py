from decouple import config
from databases import Database
from sqlalchemy import MetaData

DATABASE_URL = config("DATABASE_URL")
database = Database(DATABASE_URL)
metadata = MetaData()
