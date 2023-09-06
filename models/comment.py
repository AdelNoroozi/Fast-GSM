import sqlalchemy

from db import metadata

comment = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("mobile_id", sqlalchemy.ForeignKey("mobiles.id"), nullable=False),
    sqlalchemy.Column("text", sqlalchemy.String(256), nullable=False),
    sqlalchemy.Column("submitted_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)
