from typing import Generator, Any

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.mock import MockConnection
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.orm.session import Session
from orm import metadata, start_mappers
from db_tables import metadata


@pytest.fixture
def in_memory_db() -> MockConnection:
    engine: MockConnection = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db: MockConnection) -> Session:
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
