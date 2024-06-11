import pytest
from unittest.mock import AsyncMock, patch

from src.utils.auth_utils import (
    verify_password,
    get_password_hash,
    authenticate_user,
)
from src.database.model import User
from src.config import get_config

app_config = get_config()

@pytest.mark.asyncio
async def test_verify_password():
    hashed_password = get_password_hash("truepassword")
    assert verify_password("truepassword", hashed_password)
    assert not verify_password("wrongpassword", hashed_password)

@pytest.mark.asyncio
async def test_authenticate_user():
    mock_user_repo = AsyncMock()
    mock_user = User(username="testuser", hashed_password=get_password_hash("testpassword"))

    mock_user_repo.get_by_condition.return_value = mock_user
    session = AsyncMock()

    with patch('src.utils.auth_utils.user_repo', mock_user_repo):
        user = await authenticate_user("testuser", "testpassword", session)
        assert user == mock_user

        user = await authenticate_user("testuser", "wrongpassword", session)
        assert not user

        mock_user_repo.get_by_condition.return_value = None
        user = await authenticate_user("nonexistent", "testpassword", session)
        assert not user
