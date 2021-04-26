import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Lesson(SqlAlchemyBase):
    __tablename__ = 'Lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    klass = sqlalchemy.Column(sqlalchemy.ForeignKey("Klass.id"))
    klass_inf = orm.relation('Klass')
    teacher = sqlalchemy.Column(sqlalchemy.ForeignKey("Teachers.id"))
    teacher_inf = orm.relation('Teacher')
