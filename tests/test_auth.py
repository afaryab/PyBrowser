"""Tests for authentication module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pybrowser.auth import AuthenticationManager, OAuthConfig


@pytest.fixture
def oauth_config():
    """Create test OAuth configuration."""
    return OAuthConfig(
        client_id="test_client_id",
        client_secret="test_client_secret",
        authorization_base_url="https://auth.example.com/authorize",
        token_url="https://auth.example.com/token",
        redirect_uri="http://localhost:8080/callback",
        scope=["openid", "profile", "email"],
    )


@pytest.fixture
def auth_manager(oauth_config):
    """Create test authentication manager."""
    return AuthenticationManager(oauth_config)


def test_oauth_config_creation():
    """Test OAuth configuration creation."""
    config = OAuthConfig(
        client_id="test_id",
        client_secret="test_secret",
        authorization_base_url="https://auth.example.com/authorize",
        token_url="https://auth.example.com/token",
    )

    assert config.client_id == "test_id"
    assert config.client_secret == "test_secret"
    assert config.authorization_base_url == "https://auth.example.com/authorize"
    assert config.token_url == "https://auth.example.com/token"


def test_get_authorization_url(auth_manager):
    """Test authorization URL generation."""
    auth_url, state = auth_manager.get_authorization_url()

    assert "https://auth.example.com/authorize" in auth_url
    assert "client_id=test_client_id" in auth_url
    assert state is not None
    assert len(state) > 0


@patch("pybrowser.auth.keyring")
def test_save_token(mock_keyring, auth_manager):
    """Test token saving."""
    token = {"access_token": "test_token", "token_type": "Bearer"}

    auth_manager._save_token(token)

    mock_keyring.set_password.assert_called_once()


@patch("pybrowser.auth.keyring")
def test_load_token(mock_keyring, auth_manager):
    """Test token loading."""
    token_data = '{"access_token": "test_token", "token_type": "Bearer"}'
    mock_keyring.get_password.return_value = token_data

    token = auth_manager.load_token()

    assert token is not None
    assert token["access_token"] == "test_token"
    mock_keyring.get_password.assert_called_once()


@patch("pybrowser.auth.keyring")
def test_is_authenticated_with_token(mock_keyring, auth_manager):
    """Test authentication check with valid token."""
    token_data = '{"access_token": "test_token", "token_type": "Bearer"}'
    mock_keyring.get_password.return_value = token_data

    assert auth_manager.is_authenticated() is True


@patch("pybrowser.auth.keyring")
def test_is_authenticated_without_token(mock_keyring, auth_manager):
    """Test authentication check without token."""
    mock_keyring.get_password.return_value = None

    assert auth_manager.is_authenticated() is False


@patch("pybrowser.auth.keyring")
def test_logout(mock_keyring, auth_manager):
    """Test logout functionality."""
    auth_manager._token = {"access_token": "test_token"}

    auth_manager.logout()

    assert auth_manager._token is None
    mock_keyring.delete_password.assert_called_once()


def test_is_token_expired_no_expiration(auth_manager):
    """Test token expiration check when no expiration info is present."""
    token = {"access_token": "test_token"}
    assert auth_manager.is_token_expired(token) is False


def test_is_token_expired_valid_token(auth_manager):
    """Test token expiration check with valid token."""
    import time

    token = {"access_token": "test_token", "expires_at": time.time() + 3600}
    assert auth_manager.is_token_expired(token) is False


def test_is_token_expired_expired_token(auth_manager):
    """Test token expiration check with expired token."""
    import time

    token = {"access_token": "test_token", "expires_at": time.time() - 100}
    assert auth_manager.is_token_expired(token) is True


def test_state_validation_in_fetch_token(auth_manager):
    """Test that state validation prevents CSRF attacks."""
    auth_manager._state = "correct_state"

    # Try to fetch token with wrong state
    try:
        auth_manager.fetch_token("http://localhost:8080/callback?code=test", "wrong_state")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "CSRF" in str(e)
