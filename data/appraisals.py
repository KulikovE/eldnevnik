import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Appraisals(SqlAlchemyBase):
    __tablename__ = 'Appraisals'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    appraisals = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    lesson = sqlalchemy.Column(sqlalchemy.ForeignKey("Lessons.id"))
    lesson_inf = orm.relation('Lesson')
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    student = sqlalchemy.Column(sqlalchemy.ForeignKey("Students.id"))
    student_inf = orm.relation('Student')
