import sqlalchemy
from db import metadata

like = sqlalchemy.Table(
    "likes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("mobile_id", sqlalchemy.ForeignKey("mobiles.id"), nullable=False),
)
