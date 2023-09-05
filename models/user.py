import sqlalchemy

from db import metadata
from models.enums import RoleEnum

user = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("public_name", sqlalchemy.String(20)),
    sqlalchemy.Column("role", sqlalchemy.Enum(RoleEnum), server_default=RoleEnum.observer.name, nullable=False),
    sqlalchemy.Column("phone_number", sqlalchemy.String(20)),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("joined_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), nullable=False),
    sqlalchemy.Column(
        "modified_at", sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
        nullable=False
    )
)
