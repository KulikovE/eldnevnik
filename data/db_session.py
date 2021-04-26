# отвечает за подключение к базе данных и создание сессии для работы с ней

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

# Сначала импортируем необходимое —
# саму библиотеку sqlalchemy (в принципе,
# этого достаточно, остальные импорты нужны только
# для избавления от длинных путей), затем часть библиотеки,
# которая отвечает за функциональность ORM, потом объект Session,
# отвечающий за соединение с базой данных, и модуль declarative
# — он поможет нам объявить нашу базу данных.

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    # Если в функцию create_engine() передать параметр echo
    # со значением True, в консоль будут выводиться все SQL-запросы,
    # которые сделает SQLAlchemy, что очень удобно для отладки.
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
