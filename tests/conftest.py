from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:', 
                           connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, 
                                       autoflush=False, bind=engine)
    table_registry.metadata.create_all(bind=engine)
    db = TestingSessionLocal

    try:
        yield db
    finally:
        db.close()
        table_registry.metadata.drop_all(bind=engine)

@contextmanager 
def _mock_db_time(*, model, time=datetime(2024, 1, 1)): 

    def fake_time_hook(mapper, connection, target): 
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook) 

    yield time 

    event.remove(model, 'before_insert', fake_time_hook)

@pytest.fixture
def mock_db_time():
    return _mock_db_time