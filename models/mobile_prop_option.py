import sqlalchemy
from db import metadata

mobile_prop_option = sqlalchemy.Table(
    "mobile_prop_options",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("prop_id", sqlalchemy.ForeignKey("mobile_props.id"), nullable=False),
    sqlalchemy.Column("value", sqlalchemy.String(50), nullable=False),
)
