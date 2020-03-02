from sqlalchemy import Column, MetaData, Table, create_engine

from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import scoped_session, sessionmaker

from contextlib import contextmanager


@contextmanager
def Session(*args, **kwargs):
    Session = scoped_session(sessionmaker(
        bind=create_engine(*args, **kwargs)))

    try:
        session = Session()
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class DataBase(object):

    def __init__(self, dbname):
        self.dbname = dbname

    def create_table(self, table_name, table_spec):
        table = self.__get_table(table_name, table_spec)

        with Session(self.dbname, echo=True) as s:
            # for the sake of simplicity for this script
            s.execute('drop table if exists {}'.format(table_name))
            table_creation_sql = CreateTable(table)
            s.execute(table_creation_sql)
            s.commit()

    def insert_data(self, table_name, data, table_spec):
        table = self.__get_table(table_name, table_spec)
        with Session(self.dbname, echo=True) as s:
            s.execute(table.insert(), data)
            s.commit()

    def __get_table(self, table_name, table_spec):
        columns = [Column(n, t) for n, t in table_spec]
        table = Table(table_name, MetaData(), *columns)
        return table

