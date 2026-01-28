"""Configuration utilities for PyBrowser."""

import os
import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration is invalid."""

    pass


class Config:
    """Application configuration."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to configuration file
        """
        if config_path is None:
            config_path = os.environ.get("PYBROWSER_CONFIG", str(Path.home() / ".pybrowser" / "config.json"))

        self.config_path = Path(config_path)
        self._config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from file."""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            return self._get_default_config()

        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                self._validate_config(config)
                return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> dict:
        """Get default configuration."""
        return {
            "api_base_url": os.environ.get("PYBROWSER_API_URL", "https://api.example.com"),
            "oauth": {
                "client_id": os.environ.get("PYBROWSER_CLIENT_ID", ""),
                "client_secret": os.environ.get("PYBROWSER_CLIENT_SECRET", ""),
                "authorization_url": os.environ.get("PYBROWSER_AUTH_URL", "https://auth.example.com/oauth/authorize"),
                "token_url": os.environ.get("PYBROWSER_TOKEN_URL", "https://auth.example.com/oauth/token"),
                "redirect_uri": os.environ.get("PYBROWSER_REDIRECT_URI", "http://localhost:8080/callback"),
                "scope": ["openid", "profile", "email"],
            },
            "log_level": os.environ.get("PYBROWSER_LOG_LEVEL", "INFO"),
        }

    def _validate_config(self, config: dict):
        """
        Validate configuration structure.

        Args:
            config: Configuration dictionary to validate

        Raises:
            ConfigurationError: If configuration is invalid
        """
        # Check required top-level keys
        required_keys = ["api_base_url", "oauth"]
        for key in required_keys:
            if key not in config:
                raise ConfigurationError(f"Missing required configuration key: {key}")

        # Check required OAuth keys
        oauth_config = config.get("oauth", {})
        required_oauth_keys = ["client_id", "client_secret", "authorization_url", "token_url"]
        for key in required_oauth_keys:
            if key not in oauth_config or not oauth_config[key]:
                raise ConfigurationError(f"Missing or empty required OAuth configuration: {key}")

    def save(self):
        """Save configuration to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(self._config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def get(self, key: str, default=None):
        """Get configuration value."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value):
        """Set configuration value."""
        keys = key.split(".")
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
