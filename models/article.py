import sqlalchemy

from db import metadata

article = sqlalchemy.Table(
    "articles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("author_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), nullable=False),
    sqlalchemy.Column("modified_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(),
                      onupdate=sqlalchemy.func.now(), nullable=False),
    sqlalchemy.Column("head_photo_url", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("content", sqlalchemy.String, nullable=False)
)
