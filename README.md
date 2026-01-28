# PyBrowser

A Python-based cross-platform web browser for businesses with OAuth authentication, team management, and application switching capabilities.

[![CI](https://github.com/afaryab/PyBrowser/workflows/CI/badge.svg)](https://github.com/afaryab/PyBrowser/actions)
[![codecov](https://codecov.io/gh/afaryab/PyBrowser/branch/main/graph/badge.svg)](https://codecov.io/gh/afaryab/PyBrowser)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔐 **OAuth 2.0 Authentication**: Secure login with OAuth providers
- 👥 **Team Management**: Organize applications by teams
- 🚀 **Application Switching**: Quickly switch between business applications
- ⚡ **Quick Links**: Fast access to frequently used features
- 🌍 **Cross-Platform**: Supports Windows, macOS, and Linux
- 🔒 **Secure Storage**: Encrypted credential storage using system keyring
- 🎨 **Modern UI**: Clean, intuitive interface built with PyQt6

## Screenshots

> Note: Add screenshots of the application here once running

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### From Source

```bash
# Clone the repository
git clone https://github.com/afaryab/PyBrowser.git
cd PyBrowser

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the application
pip install -e .
```

### From Release (Coming Soon)

Download the appropriate installer for your platform from the [Releases](https://github.com/afaryab/PyBrowser/releases) page.

- **Windows**: `pybrowser-windows.zip`
- **macOS**: `PyBrowser.dmg`
- **Linux**: `pybrowser-linux.tar.gz`

## Configuration

PyBrowser requires OAuth configuration to function. You can configure it using environment variables or a configuration file.

### Environment Variables

```bash
export PYBROWSER_CLIENT_ID="your_oauth_client_id"
export PYBROWSER_CLIENT_SECRET="your_oauth_client_secret"
export PYBROWSER_API_URL="https://api.example.com"
export PYBROWSER_AUTH_URL="https://auth.example.com/oauth/authorize"
export PYBROWSER_TOKEN_URL="https://auth.example.com/oauth/token"
export PYBROWSER_REDIRECT_URI="http://localhost:8080/callback"
```

### Configuration File

Create a configuration file at `~/.pybrowser/config.json`:

```json
{
  "api_base_url": "https://api.example.com",
  "oauth": {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "authorization_url": "https://auth.example.com/oauth/authorize",
    "token_url": "https://auth.example.com/oauth/token",
    "redirect_uri": "http://localhost:8080/callback",
    "scope": ["openid", "profile", "email"]
  },
  "log_level": "INFO"
}
```

## Usage

### Running the Application

```bash
# With environment variables set
python -m pybrowser.main

# Or use the installed command
pybrowser
```

### First Launch

1. The application will open a login dialog
2. Click "Start Login" to begin OAuth authentication
3. Complete the authentication in the web view
4. Once authenticated, the main window will open
5. Your teams and applications will be loaded automatically

### Using the Application

- **Left Sidebar**: Browse and select applications
- **Top Toolbar**: Access quick links for the current application
- **Main Area**: Web view displaying the selected application
- **Menu Bar**: 
  - File → Logout / Exit
  - View → Refresh Data

## Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (optional)
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=pybrowser --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

### Code Quality

```bash
# Format code
black src/pybrowser tests

# Lint code
flake8 src/pybrowser

# Type check
mypy src/pybrowser --ignore-missing-imports
```

### Building Installers

The application uses PyInstaller to create standalone executables.

```bash
# Linux/macOS
pyinstaller --name pybrowser \
  --onefile \
  --windowed \
  --add-data "src/pybrowser:pybrowser" \
  src/pybrowser/main.py

# Windows
pyinstaller --name pybrowser `
  --onefile `
  --windowed `
  --add-data "src/pybrowser;pybrowser" `
  src/pybrowser/main.py
```

## Architecture

### Project Structure

```
PyBrowser/
├── src/pybrowser/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── auth/                # Authentication module
│   │   └── __init__.py
│   ├── api/                 # API client
│   │   └── __init__.py
│   ├── ui/                  # User interface
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   └── login_dialog.py
│   ├── models/              # Data models
│   │   └── __init__.py
│   └── utils/               # Utilities
│       └── __init__.py
├── tests/                   # Test suite
├── .github/
│   ├── workflows/           # CI/CD workflows
│   └── copilot-instructions.md
├── requirements.txt
├── setup.py
└── README.md
```

### Technology Stack

- **GUI Framework**: PyQt6
- **Web Engine**: PyQt6-WebEngine (Chromium-based)
- **HTTP Client**: requests
- **OAuth**: requests-oauthlib
- **Data Validation**: Pydantic
- **Secure Storage**: keyring
- **Testing**: pytest, pytest-qt
- **Code Quality**: black, flake8, mypy

## API Specification

PyBrowser expects a backend API with the following endpoints:

### Authentication
- OAuth 2.0 Authorization Code Flow
- Scopes: `openid`, `profile`, `email`

### API Endpoints

#### Get User Profile
```
GET /api/user/profile
Authorization: Bearer {access_token}

Response:
{
  "id": "user123",
  "email": "user@example.com",
  "name": "John Doe",
  "avatar": "https://example.com/avatar.jpg"
}
```

#### List Teams
```
GET /api/teams
Authorization: Bearer {access_token}

Response:
{
  "teams": [
    {
      "id": "team1",
      "name": "Engineering",
      "description": "Engineering team"
    }
  ]
}
```

#### List Applications
```
GET /api/teams/{team_id}/applications
Authorization: Bearer {access_token}

Response:
{
  "applications": [
    {
      "id": "app1",
      "name": "Project Management",
      "url": "https://pm.example.com",
      "description": "Track projects and tasks",
      "icon": "https://example.com/icon.png"
    }
  ]
}
```

#### List Quick Links
```
GET /api/applications/{app_id}/quick-links
Authorization: Bearer {access_token}

Response:
{
  "quick_links": [
    {
      "id": "link1",
      "name": "Dashboard",
      "url": "https://app.example.com/dashboard",
      "icon": "https://example.com/icon.png",
      "order": 0
    }
  ]
}
```

## Security

### Security Features

- **OAuth 2.0**: Industry-standard authentication protocol
- **Encrypted Storage**: Credentials stored using system keyring
- **HTTPS Only**: All API communications over HTTPS
- **Token Refresh**: Automatic token refresh handling
- **Input Validation**: All inputs validated using Pydantic models

### Security Scanning

The project uses:
- **CodeQL**: Static analysis for security vulnerabilities
- **Safety**: Dependency vulnerability scanning
- **Bandit**: Python security linter

### Reporting Security Issues

Please report security vulnerabilities to the maintainers privately. Do not open public issues for security concerns.

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Maintain test coverage above 80%

## CI/CD

The project uses GitHub Actions for continuous integration and deployment:

- **CI Workflow**: Runs tests, linting, and security scans on all PRs and commits
- **Release Workflow**: Builds installers for all platforms when tags are pushed
- **CodeQL Workflow**: Performs security analysis weekly and on changes

## Roadmap

- [x] OAuth authentication
- [x] Team and application management
- [x] Quick links
- [x] Cross-platform support
- [x] CI/CD pipelines
- [ ] Multi-tab support with session persistence
- [ ] Bookmarks and favorites
- [ ] Custom themes
- [ ] Plugin system
- [ ] Offline mode
- [ ] Auto-update functionality

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- PyQt6 for the excellent GUI framework
- Chromium for the web engine
- All contributors and maintainers

## Support

For support, please open an issue on GitHub or contact the maintainers.

## Links

- [Documentation](https://github.com/afaryab/PyBrowser/wiki)
- [Issue Tracker](https://github.com/afaryab/PyBrowser/issues)
- [Changelog](CHANGELOG.md)
