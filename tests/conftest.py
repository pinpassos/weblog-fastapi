import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Returns fastapi test client instance."""
    return TestClient(app)
