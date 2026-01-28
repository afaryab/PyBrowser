"""Tests for data models."""

import pytest
from pydantic import ValidationError

from pybrowser.models import QuickLink, Application, Team, UserProfile


def test_quick_link_creation():
    """Test QuickLink model creation."""
    link = QuickLink(id="link1", name="Dashboard", url="https://example.com/dashboard", order=0)

    assert link.id == "link1"
    assert link.name == "Dashboard"
    assert str(link.url) == "https://example.com/dashboard"
    assert link.order == 0


def test_quick_link_validation():
    """Test QuickLink URL validation."""
    with pytest.raises(ValidationError):
        QuickLink(id="link1", name="Invalid", url="not-a-url", order=0)


def test_application_creation():
    """Test Application model creation."""
    app = Application(id="app1", name="App 1", url="https://app.example.com", description="Test application")

    assert app.id == "app1"
    assert app.name == "App 1"
    assert str(app.url) == "https://app.example.com/"
    assert app.description == "Test application"
    assert app.quick_links == []


def test_application_with_quick_links():
    """Test Application with quick links."""
    links = [
        QuickLink(id="l1", name="Link 1", url="https://example.com/1", order=0),
        QuickLink(id="l2", name="Link 2", url="https://example.com/2", order=1),
    ]

    app = Application(id="app1", name="App 1", url="https://app.example.com", quick_links=links)

    assert len(app.quick_links) == 2
    assert app.quick_links[0].name == "Link 1"


def test_team_creation():
    """Test Team model creation."""
    team = Team(id="team1", name="Team 1", description="Test team")

    assert team.id == "team1"
    assert team.name == "Team 1"
    assert team.description == "Test team"
    assert team.applications == []


def test_team_with_applications():
    """Test Team with applications."""
    apps = [
        Application(id="a1", name="App 1", url="https://app1.example.com"),
        Application(id="a2", name="App 2", url="https://app2.example.com"),
    ]

    team = Team(id="team1", name="Team 1", applications=apps)

    assert len(team.applications) == 2
    assert team.applications[0].name == "App 1"


def test_user_profile_creation():
    """Test UserProfile model creation."""
    profile = UserProfile(id="user123", email="test@example.com", name="Test User")

    assert profile.id == "user123"
    assert profile.email == "test@example.com"
    assert profile.name == "Test User"
    assert profile.avatar is None
