from contextlib import contextmanager
from importlib import import_module
from inspect import getmembers

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


@contextmanager
def transaction():
    session: Session = DB.get_session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
