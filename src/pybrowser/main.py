"""Main application entry point."""

import sys
import logging
from PyQt6.QtWidgets import QApplication, QMessageBox

from pybrowser.auth import AuthenticationManager, OAuthConfig
from pybrowser.api import APIClient
from pybrowser.ui import MainWindow, LoginDialog
from pybrowser.utils import Config


def setup_logging(level: str = "INFO"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def main():
    """Main application entry point."""
    # Load configuration
    config = Config()

    # Set up logging
    setup_logging(config.get("log_level", "INFO"))
    logger = logging.getLogger(__name__)

    logger.info("Starting PyBrowser...")

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("PyBrowser")
    app.setOrganizationName("PyBrowser")

    # Set up OAuth configuration
    oauth_config = OAuthConfig(
        client_id=config.get("oauth.client_id", ""),
        client_secret=config.get("oauth.client_secret", ""),
        authorization_base_url=config.get("oauth.authorization_url", ""),
        token_url=config.get("oauth.token_url", ""),
        redirect_uri=config.get("oauth.redirect_uri", "http://localhost:8080/callback"),
        scope=config.get("oauth.scope", ["openid", "profile", "email"]),
    )

    # Check if OAuth is configured
    if not oauth_config.client_id or not oauth_config.client_secret:
        QMessageBox.critical(
            None,
            "Configuration Error",
            "OAuth is not configured. Please set PYBROWSER_CLIENT_ID and PYBROWSER_CLIENT_SECRET "
            "environment variables or create a configuration file.",
        )
        return 1

    # Create authentication manager
    auth_manager = AuthenticationManager(oauth_config)

    # Check if already authenticated
    if not auth_manager.is_authenticated():
        logger.info("User not authenticated, showing login dialog")
        login_dialog = LoginDialog(auth_manager)
        if login_dialog.exec() != LoginDialog.DialogCode.Accepted:
            logger.info("Login cancelled")
            return 0

    # Create API client
    api_client = APIClient(base_url=config.get("api_base_url", "https://api.example.com"), auth_manager=auth_manager)

    # Create and show main window
    main_window = MainWindow(auth_manager, api_client)
    main_window.show()

    logger.info("PyBrowser started successfully")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
