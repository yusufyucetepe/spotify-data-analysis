from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_current_user, get_spotify_client
from app.main import app
from app.models.user import User


@pytest.fixture
def mock_user():
    user = MagicMock(spec=User)
    user.spotify_id = "test_spotify_id"
    user.display_name = "Test User"
    user.access_token = "mock_access_token"
    user.refresh_token = "mock_refresh_token"
    user.token_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    return user


@pytest.fixture
def mock_sp():
    return MagicMock()


@pytest.fixture
def client(mock_user, mock_sp):
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_spotify_client] = lambda: mock_sp
    yield TestClient(app)
    app.dependency_overrides.clear()
