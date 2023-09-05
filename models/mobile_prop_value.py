import sqlalchemy
from db import metadata

mobile_prop_value = sqlalchemy.Table(
    "mobile_prop_values",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=False),
    sqlalchemy.Column("prop_id", sqlalchemy.ForeignKey("mobile_props.id"), nullable=False),
    sqlalchemy.Column("value", sqlalchemy.String(50), nullable=False),
)
