"""Main browser window UI."""

import logging
from typing import Optional, List
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QLabel, QMessageBox, QListWidget, QListWidgetItem,
    QStackedWidget, QPushButton, QSplitter
)
from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView

from pybrowser.models import Team, Application, QuickLink
from pybrowser.api import APIClient
from pybrowser.auth import AuthenticationManager

logger = logging.getLogger(__name__)


class BrowserTab(QWidget):
    """Individual browser tab with web view."""
    
    def __init__(self, url: str = "", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.web_view = QWebEngineView()
        if url:
            self.web_view.setUrl(QUrl(url))
        
        layout.addWidget(self.web_view)
        self.setLayout(layout)
    
    def load_url(self, url: str):
        """Load a URL in the web view."""
        self.web_view.setUrl(QUrl(url))


class QuickLinksBar(QToolBar):
    """Toolbar showing quick links for current application."""
    
    link_clicked = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__("Quick Links", parent)
        self.setMovable(False)
        
    def set_links(self, links: List[QuickLink]):
        """Set quick links to display."""
        self.clear()
        
        for link in sorted(links, key=lambda x: x.order):
            action = QAction(link.name, self)
            action.setData(str(link.url))
            action.triggered.connect(lambda checked, url=str(link.url): self.link_clicked.emit(url))
            self.addAction(action)


class ApplicationSidebar(QWidget):
    """Sidebar for switching between applications."""
    
    application_selected = pyqtSignal(Application)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Applications")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 10px;")
        layout.addWidget(title)
        
        # Application list
        self.app_list = QListWidget()
        self.app_list.itemClicked.connect(self._on_app_clicked)
        layout.addWidget(self.app_list)
        
        self.setLayout(layout)
        self.applications: List[Application] = []
    
    def set_applications(self, applications: List[Application]):
        """Set applications to display."""
        self.applications = applications
        self.app_list.clear()
        
        for app in applications:
            item = QListWidgetItem(app.name)
            item.setData(Qt.ItemDataRole.UserRole, app)
            self.app_list.addItem(item)
    
    def _on_app_clicked(self, item: QListWidgetItem):
        """Handle application selection."""
        app = item.data(Qt.ItemDataRole.UserRole)
        if app:
            self.application_selected.emit(app)


class MainWindow(QMainWindow):
    """Main browser window."""
    
    def __init__(self, auth_manager: AuthenticationManager, api_client: APIClient):
        super().__init__()
        self.auth_manager = auth_manager
        self.api_client = api_client
        self.current_app: Optional[Application] = None
        
        self.setWindowTitle("PyBrowser")
        self.setGeometry(100, 100, 1200, 800)
        
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Create main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Quick links toolbar
        self.quick_links_bar = QuickLinksBar(self)
        self.quick_links_bar.link_clicked.connect(self._on_quick_link_clicked)
        self.addToolBar(self.quick_links_bar)
        
        # Splitter for sidebar and content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sidebar
        self.sidebar = ApplicationSidebar()
        self.sidebar.application_selected.connect(self._on_application_selected)
        self.sidebar.setMaximumWidth(250)
        splitter.addWidget(self.sidebar)
        
        # Browser area
        self.browser_tabs = QStackedWidget()
        splitter.addWidget(self.browser_tabs)
        
        # Set splitter sizes (sidebar smaller than content)
        splitter.setSizes([250, 950])
        
        main_layout.addWidget(splitter)
        
        # Menu bar
        self._setup_menu()
    
    def _setup_menu(self):
        """Set up menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        logout_action = QAction("&Logout", self)
        logout_action.triggered.connect(self._logout)
        file_menu.addAction(logout_action)
        
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        refresh_action = QAction("&Refresh Data", self)
        refresh_action.triggered.connect(self._load_data)
        view_menu.addAction(refresh_action)
    
    def _load_data(self):
        """Load teams and applications from server."""
        try:
            teams = self.api_client.get_teams()
            if teams:
                # For now, use the first team
                team = teams[0]
                applications = self.api_client.get_applications(team.id)
                self.sidebar.set_applications(applications)
                
                # Load first application by default
                if applications:
                    self._on_application_selected(applications[0])
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to load data from server: {str(e)}"
            )
    
    def _on_application_selected(self, app: Application):
        """Handle application selection."""
        self.current_app = app
        
        # Load quick links
        quick_links = self.api_client.get_quick_links(app.id)
        app.quick_links = quick_links
        self.quick_links_bar.set_links(quick_links)
        
        # Create or switch to browser tab for this app
        # Check if tab already exists
        for i in range(self.browser_tabs.count()):
            widget = self.browser_tabs.widget(i)
            if hasattr(widget, 'app_id') and widget.app_id == app.id:
                self.browser_tabs.setCurrentWidget(widget)
                return
        
        # Create new tab
        tab = BrowserTab(str(app.url))
        tab.app_id = app.id
        self.browser_tabs.addWidget(tab)
        self.browser_tabs.setCurrentWidget(tab)
    
    def _on_quick_link_clicked(self, url: str):
        """Handle quick link click."""
        current_tab = self.browser_tabs.currentWidget()
        if isinstance(current_tab, BrowserTab):
            current_tab.load_url(url)
    
    def _logout(self):
        """Handle logout action."""
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.auth_manager.logout()
            self.close()
