"""Tests for API client."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

from pybrowser.api import APIClient
from pybrowser.auth import AuthenticationManager, OAuthConfig
from pybrowser.models import Team, Application, QuickLink, UserProfile


@pytest.fixture
def auth_manager():
    """Create mock authentication manager."""
    config = OAuthConfig(
        client_id="test_id",
        client_secret="test_secret",
        authorization_base_url="https://auth.example.com/authorize",
        token_url="https://auth.example.com/token",
    )
    manager = AuthenticationManager(config)
    manager._token = {"access_token": "test_token", "token_type": "Bearer"}
    return manager


@pytest.fixture
def api_client(auth_manager):
    """Create test API client."""
    return APIClient("https://api.example.com", auth_manager)


def test_api_client_initialization(api_client):
    """Test API client initialization."""
    assert api_client.base_url == "https://api.example.com"
    assert api_client.auth_manager is not None


def test_get_headers(api_client):
    """Test request headers generation."""
    headers = api_client._get_headers()

    assert "Authorization" in headers
    assert headers["Authorization"] == "Bearer test_token"
    assert headers["Content-Type"] == "application/json"


@patch("pybrowser.api.requests.get")
def test_get_user_profile_success(mock_get, api_client):
    """Test successful user profile fetch."""
    mock_response = Mock()
    mock_response.json.return_value = {"id": "user123", "email": "test@example.com", "name": "Test User"}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    profile = api_client.get_user_profile()

    assert profile is not None
    assert profile.id == "user123"
    assert profile.email == "test@example.com"
    assert profile.name == "Test User"


@patch("pybrowser.api.requests.get")
def test_get_teams_success(mock_get, api_client):
    """Test successful teams fetch."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "teams": [{"id": "team1", "name": "Team 1", "description": "First team", "applications": []}]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    teams = api_client.get_teams()

    assert len(teams) == 1
    assert teams[0].id == "team1"
    assert teams[0].name == "Team 1"


@patch("pybrowser.api.requests.get")
def test_get_applications_success(mock_get, api_client):
    """Test successful applications fetch."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "applications": [
            {"id": "app1", "name": "App 1", "url": "https://app1.example.com", "description": "First app", "quick_links": []}
        ]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    apps = api_client.get_applications("team1")

    assert len(apps) == 1
    assert apps[0].id == "app1"
    assert apps[0].name == "App 1"


@patch("pybrowser.api.requests.get")
def test_get_quick_links_success(mock_get, api_client):
    """Test successful quick links fetch."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "quick_links": [{"id": "link1", "name": "Dashboard", "url": "https://app.example.com/dashboard", "order": 0}]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    links = api_client.get_quick_links("app1")

    assert len(links) == 1
    assert links[0].id == "link1"
    assert links[0].name == "Dashboard"


@patch("pybrowser.api.requests.get")
def test_api_error_handling(mock_get, api_client):
    """Test API error handling."""
    mock_get.side_effect = requests.exceptions.RequestException("Network error")

    profile = api_client.get_user_profile()
    assert profile is None

    teams = api_client.get_teams()
    assert teams == []
