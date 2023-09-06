import sqlalchemy

from db import metadata

mobile_photo = sqlalchemy.Table(
    "mobile_photos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("mobile_id", sqlalchemy.ForeignKey("mobiles.id"), nullable=False),
    sqlalchemy.Column("photo_url", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("is_thumbnail", sqlalchemy.Boolean, server_default="0"),
    sqlalchemy.Column("alt_text", sqlalchemy.String),
)
