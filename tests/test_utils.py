"""Tests for utility functions."""

import pytest
import json
import tempfile
from pathlib import Path

from pybrowser.utils import Config, ConfigurationError


def test_config_default_values():
    """Test that default configuration is returned when no file exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config = Config(str(config_path))

        assert config.get("api_base_url") is not None
        assert config.get("oauth.client_id") is not None


def test_config_load_from_file():
    """Test loading configuration from file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"

        # Create a valid config file
        config_data = {
            "api_base_url": "https://test.example.com",
            "oauth": {
                "client_id": "test_client",
                "client_secret": "test_secret",
                "authorization_url": "https://auth.test.com/auth",
                "token_url": "https://auth.test.com/token",
            },
        }

        with open(config_path, "w") as f:
            json.dump(config_data, f)

        config = Config(str(config_path))

        assert config.get("api_base_url") == "https://test.example.com"
        assert config.get("oauth.client_id") == "test_client"


def test_config_validation_missing_required_key():
    """Test that configuration validation catches missing required keys."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"

        # Create invalid config file (missing oauth)
        config_data = {"api_base_url": "https://test.example.com"}

        with open(config_path, "w") as f:
            json.dump(config_data, f)

        # Should fall back to defaults due to validation error
        config = Config(str(config_path))
        # Should still work, using defaults
        assert config.get("api_base_url") is not None


def test_config_save():
    """Test saving configuration to file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config = Config(str(config_path))

        config.set("custom_key", "custom_value")
        config.save()

        assert config_path.exists()

        # Load and verify
        with open(config_path, "r") as f:
            saved_data = json.load(f)
            assert saved_data["custom_key"] == "custom_value"


def test_config_get_with_default():
    """Test getting configuration value with default."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config = Config(str(config_path))

        value = config.get("nonexistent.key", "default_value")
        assert value == "default_value"


def test_config_nested_set():
    """Test setting nested configuration values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config = Config(str(config_path))

        config.set("level1.level2.key", "value")
        assert config.get("level1.level2.key") == "value"
