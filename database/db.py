import os
from contextlib import contextmanager
from importlib import import_module
from inspect import getmembers
from os.path import isfile

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class DB:
    session_maker = None
    engine = None
    base = None

    @classmethod
    def get_session(cls) -> Session:
        return cls.session_maker()

    @classmethod
    def read(cls, settings):
        url = settings['alembic']['sqlalchemy.url']
        cls.engine = create_engine(url)
        cls.session_maker = sessionmaker(bind=cls.engine, autoflush=False)
        models_location = settings['alembic']['models_location']
        module = import_module(models_location)
        for name, obj in getmembers(module):
            pass

    @classmethod
    def create_tables(cls, settings):
        p = settings['alembic']['sqlalchemy.url'].split('///')[-1]
        p = os.path.join(os.getcwd(), p)
        if not isfile(p):
            m = import_module(settings['alembic']['models_location'] + '.models')
            base = getattr(m, 'Base')
            base.metadata.create_all(cls.engine)


@contextmanager
def transaction() -> Session:
    session = DB.get_session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
