from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.mock import MockConnection
from sqlalchemy.orm import sessionmaker

from db_tables import metadata


@pytest.fixture
def in_memory_db() -> MockConnection:
    engine: MockConnection = create_engine("sqlite:///:memory")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db: MockConnection) -> Generator:
    yield sessionmaker(bind=in_memory_db)()
