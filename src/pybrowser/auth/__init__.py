"""OAuth authentication module for PyBrowser."""

import json
import logging
import time
from typing import Optional, Dict
from requests_oauthlib import OAuth2Session
import keyring

logger = logging.getLogger(__name__)


class OAuthConfig:
    """OAuth configuration."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        authorization_base_url: str,
        token_url: str,
        redirect_uri: str = "http://localhost:8080/callback",
        scope: Optional[list] = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_base_url = authorization_base_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.scope = scope or ["openid", "profile", "email"]


class AuthenticationManager:
    """Manages OAuth authentication flow and token storage."""

    SERVICE_NAME = "PyBrowser"
    TOKEN_KEY = "oauth_token"

    def __init__(self, config: OAuthConfig):
        self.config = config
        self._token: Optional[Dict] = None
        self._session: Optional[OAuth2Session] = None
        self._state: Optional[str] = None

    def get_authorization_url(self) -> tuple[str, str]:
        """
        Generate authorization URL for OAuth flow.

        Returns:
            Tuple of (authorization_url, state)
        """
        oauth = OAuth2Session(
            self.config.client_id,
            redirect_uri=self.config.redirect_uri,
            scope=self.config.scope,
        )
        authorization_url, state = oauth.authorization_url(self.config.authorization_base_url)
        self._state = state  # Store state for validation
        return authorization_url, state

    def fetch_token(self, authorization_response: str, state: str) -> Dict:
        """
        Exchange authorization code for access token.

        Args:
            authorization_response: Full callback URL with code
            state: State parameter from authorization request

        Returns:
            Token dictionary

        Raises:
            ValueError: If state validation fails
        """
        # Validate state to prevent CSRF attacks
        if self._state is None or state != self._state:
            raise ValueError("Invalid state parameter - possible CSRF attack")

        oauth = OAuth2Session(
            self.config.client_id,
            redirect_uri=self.config.redirect_uri,
            state=state,
        )
        token = oauth.fetch_token(
            self.config.token_url,
            authorization_response=authorization_response,
            client_secret=self.config.client_secret,
            timeout=10,
        )

        # Add token expiration time if not present
        if "expires_at" not in token and "expires_in" in token:
            token["expires_at"] = time.time() + token["expires_in"]

        self._token = token
        self._save_token(token)
        self._state = None  # Clear state after use
        return token

    def _save_token(self, token: Dict):
        """Save token securely using keyring."""
        try:
            keyring.set_password(self.SERVICE_NAME, self.TOKEN_KEY, json.dumps(token))
            logger.info("Token saved securely")
        except Exception as e:
            # Log only non-sensitive error information
            logger.error(f"Failed to save token: {type(e).__name__}")

    def load_token(self) -> Optional[Dict]:
        """Load token from secure storage."""
        try:
            token_str = keyring.get_password(self.SERVICE_NAME, self.TOKEN_KEY)
            if token_str:
                self._token = json.loads(token_str)
                return self._token
        except Exception as e:
            # Log only non-sensitive error information
            logger.error(f"Failed to load token: {type(e).__name__}")
        return None

    def is_token_expired(self, token: Optional[Dict] = None) -> bool:
        """
        Check if token is expired.

        Args:
            token: Token to check, or None to check current token

        Returns:
            True if token is expired or will expire in the next 60 seconds
        """
        if token is None:
            token = self.get_token()

        if not token:
            return True

        expires_at = token.get("expires_at")
        if expires_at is None:
            # If no expiration info, assume token is valid
            return False

        # Add 60 second buffer to refresh before actual expiration
        return time.time() >= (expires_at - 60)

    def get_token(self) -> Optional[Dict]:
        """Get current token."""
        if not self._token:
            self._token = self.load_token()
        return self._token

    def is_authenticated(self) -> bool:
        """Check if user is authenticated with a valid, non-expired token."""
        token = self.get_token()
        return token is not None and not self.is_token_expired(token)

    def logout(self):
        """Clear authentication tokens."""
        try:
            keyring.delete_password(self.SERVICE_NAME, self.TOKEN_KEY)
            self._token = None
            logger.info("User logged out successfully")
        except Exception as e:
            # Log only non-sensitive error information
            logger.error(f"Failed to logout: {type(e).__name__}")

    def get_session(self) -> OAuth2Session:
        """Get authenticated OAuth session."""
        if not self._session or not self._token:
            self._token = self.load_token()
            if not self._token:
                raise ValueError("No valid token available")

            self._session = OAuth2Session(
                self.config.client_id,
                token=self._token,
            )
        return self._session
