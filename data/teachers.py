import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Teacher(SqlAlchemyBase, UserMixin):
    __tablename__ = 'Teachers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
