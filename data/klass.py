import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Klass(SqlAlchemyBase):
    __tablename__ = 'Klass'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
