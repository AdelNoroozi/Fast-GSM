import sqlalchemy

mobile_prop = sqlalchemy.Table(
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("prop", sqlalchemy.String(30), nullable=False),
    sqlalchemy.Column("is_selectable", sqlalchemy.Boolean, server_default=False),
)
