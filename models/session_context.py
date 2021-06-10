import os

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

postgres_uri = os.getenv("postgres.url")


@contextmanager
def db_session():
    """ Creates a context with an open SQLAlchemy session.
    """
    engine = create_engine(postgres_uri, convert_unicode=True)
    connection = engine.connect()
    db_sesh = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    yield db_sesh
    db_sesh.close()
    connection.close()
