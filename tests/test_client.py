import pytest
from unittest.mock import MagicMock, patch
from src.api.client import GitLabClient

@pytest.fixture
def mock_gitlab():
    with patch('src.api.client.gitlab.Gitlab') as mock:
        yield mock

def test_client_init_success(mock_gitlab):
    # Setup mock
    mock_instance = mock_gitlab.return_value
    mock_instance.auth.return_value = None
    mock_instance.user.username = "testuser"
    
    client = GitLabClient("token123", "http://gitlab.example.com")
    success, message = client.authenticate()
    
    assert success is True
    assert client.user.username == "testuser"
    mock_gitlab.assert_called_with("http://gitlab.example.com", private_token="token123")

def test_client_init_failure(mock_gitlab):
    # Setup mock to raise exception
    mock_gitlab.return_value.auth.side_effect = Exception("Auth failed")
    
    client = GitLabClient("badtoken", "http://gitlab.example.com")
    success, message = client.authenticate()
    
    assert success is False
    assert "Auth failed" in message
