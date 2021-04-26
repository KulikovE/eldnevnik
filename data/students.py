import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Student(SqlAlchemyBase, UserMixin):
    __tablename__ = 'Students'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    klass = sqlalchemy.Column(sqlalchemy.ForeignKey("Klass.id"))
    klass_inf = orm.relation('Klass')
