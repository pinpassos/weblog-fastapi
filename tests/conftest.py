import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.main import app
from app.settings.database import Base
from app.users.models import User


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    """Returns fastapi test client instance."""
    return TestClient(app)


@pytest.fixture
def user():
    return User(
        username="user_test@gmail.com",
        email="user_test@gmail.com",
        hashed_password="hashed_password",
        is_active=True
    )


@pytest.fixture
def duplicated_user():
    return User(
        username="user_test@gmail.com",
        email="user_test@gmail.com",
        hashed_password="hashed_password",
        is_active=True
    )
