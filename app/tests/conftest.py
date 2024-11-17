import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db_setup import Base, get_session
from backend.kv_store import KVStore
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="module")
def db_engine():
    """Creates an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="module")
def db_session(db_engine):
    """Provides a SQLAlchemy session for testing."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture(scope="module")
def kv_store(db_session):
    """Provides a KVStore instance for testing."""
    return KVStore(db_session)
