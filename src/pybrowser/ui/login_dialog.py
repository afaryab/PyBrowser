"""Login dialog for OAuth authentication."""

import logging
from typing import Optional
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTextEdit
from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage

from pybrowser.auth import AuthenticationManager

logger = logging.getLogger(__name__)


class LoginDialog(QDialog):
    """Dialog for OAuth authentication flow."""

    authenticated = pyqtSignal(dict)

    def __init__(self, auth_manager: AuthenticationManager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.state: Optional[str] = None

        self.setWindowTitle("Login - PyBrowser")
        self.setGeometry(200, 200, 600, 700)

        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()

        # Title
        title = QLabel("Sign in to PyBrowser")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Web view for OAuth flow
        self.web_view = QWebEngineView()
        self.web_view.page().urlChanged.connect(self._on_url_changed)
        layout.addWidget(self.web_view)

        # Login button
        self.login_button = QPushButton("Start Login")
        self.login_button.clicked.connect(self._start_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def _start_login(self):
        """Start OAuth login flow."""
        try:
            auth_url, self.state = self.auth_manager.get_authorization_url()
            self.web_view.setUrl(QUrl(auth_url))
            self.login_button.setEnabled(False)
        except Exception as e:
            logger.error(f"Failed to start login: {e}")
            QMessageBox.critical(self, "Login Error", f"Failed to start login: {str(e)}")

    def _on_url_changed(self, url: QUrl):
        """Handle URL changes during OAuth flow."""
        url_string = url.toString()

        # Check if this is the callback URL
        if url_string.startswith(self.auth_manager.config.redirect_uri):
            try:
                token = self.auth_manager.fetch_token(url_string, self.state)
                self.authenticated.emit(token)
                self.accept()
            except Exception as e:
                logger.error(f"Failed to complete authentication: {e}")
                QMessageBox.critical(self, "Authentication Error", f"Failed to complete authentication: {str(e)}")
                self.reject()
