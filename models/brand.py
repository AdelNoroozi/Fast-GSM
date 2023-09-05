import sqlalchemy
from db import metadata

brand = sqlalchemy.Table(
    "brands",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(20), nullable=False, unique=True),
    sqlalchemy.Column("logo_url", sqlalchemy.String(100)),
)
