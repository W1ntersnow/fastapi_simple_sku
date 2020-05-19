import pytest

from fastapi.testclient import TestClient

from main import app
from db import SessionLocal


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()


