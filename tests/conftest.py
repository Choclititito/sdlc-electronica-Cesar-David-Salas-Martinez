import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db import Base, get_db
from app.main import app

TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(bind=TEST_ENGINE, expire_on_commit=False)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=TEST_ENGINE)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=TEST_ENGINE)