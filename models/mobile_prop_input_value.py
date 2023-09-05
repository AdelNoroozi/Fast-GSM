import sqlalchemy
from db import metadata

mobile_prop_input_value = sqlalchemy.Table(
    "mobile_prop_input_values",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("mobile_id", sqlalchemy.ForeignKey("mobiles.id"), nullable=False),
    sqlalchemy.Column("prop_id", sqlalchemy.ForeignKey("mobile_prop.ids"), nullable=False),
    sqlalchemy.Column("value", sqlalchemy.String(50), nullable=False),
)
