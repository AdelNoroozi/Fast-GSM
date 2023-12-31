import sqlalchemy
from db import metadata

mobile = sqlalchemy.Table(
    "mobiles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50), nullable=False, unique=True),
    sqlalchemy.Column("release_date", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("brand_id", sqlalchemy.ForeignKey("brands.id"), nullable=False),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("views", sqlalchemy.Integer, nullable=False, server_default='0'),
    sqlalchemy.Column("likes_count", sqlalchemy.Integer, nullable=False, server_default='0'),
    sqlalchemy.Column("comments_count", sqlalchemy.Integer, nullable=False, server_default='0'),
)
