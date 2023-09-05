import sqlalchemy
from db import metadata

mobile_prop_selectable_value = sqlalchemy.Table(
    "mobile_prop_selectable_values",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("mobile_id", sqlalchemy.ForeignKey("mobiles.id"), nullable=False),
    sqlalchemy.Column("prop_value_id", sqlalchemy.ForeignKey("mobile_prop_options.id"), nullable=False),
)
