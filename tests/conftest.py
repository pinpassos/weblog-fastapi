import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.main import app
from app.posts.models import Category, Post
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
        is_active=True,
        posts=[]
    )


@pytest.fixture
def duplicated_user():
    return User(
        username="user_test@gmail.com",
        email="user_test@gmail.com",
        hashed_password="hashed_password",
        is_active=True,
        posts=[]
    )


@pytest.fixture
def post():
    return Post(
        title="Software development and unit tests",
        summary="Unit tests are a wonderful way...",
        content="I enjoy writing unit tests because they are key to maintaining code quality",
        slug="tech-unit-test",
        author=None,
        categories=[]
    )


@pytest.fixture
def category():
    return Category(
        name="Technologie",
        description="Everything about tech world",
        is_active=False,
        posts=[]
    )


@pytest.fixture
def duplicated_category():
    return Category(
        name="Technologie",
        description="Category with duplicated name",
        is_active=False,
        posts=[]
    )
