# PyBrowser - GitHub Copilot Instructions

## Project Overview
PyBrowser is a Python-based cross-platform web browser for businesses with OAuth authentication, team management, and application switching capabilities.

## Architecture

### Core Components
1. **Authentication (`src/pybrowser/auth/`)**: OAuth2 authentication flow with secure token storage
2. **API Client (`src/pybrowser/api/`)**: Communication with backend server for teams, applications, and quick links
3. **UI (`src/pybrowser/ui/`)**: PyQt6-based user interface with main window and login dialog
4. **Models (`src/pybrowser/models/`)**: Pydantic data models for type safety
5. **Utils (`src/pybrowser/utils/`)**: Configuration and utility functions

### Key Technologies
- **PyQt6**: Cross-platform GUI framework
- **PyQt6-WebEngine**: Web rendering engine
- **Pydantic**: Data validation and models
- **requests-oauthlib**: OAuth authentication
- **keyring**: Secure credential storage

## Code Style

### Python Standards
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Maximum line length: 127 characters
- Use Black for code formatting
- Use flake8 for linting
- Use mypy for type checking

### Documentation
- Use docstrings for all public classes and methods
- Follow Google-style docstrings format
- Include type information in docstrings

### Example
```python
def fetch_teams(self, user_id: str) -> List[Team]:
    """
    Fetch teams for a user.
    
    Args:
        user_id: User identifier
        
    Returns:
        List of Team objects
        
    Raises:
        ValueError: If user_id is invalid
    """
```

## Development Workflow

### Setting Up Development Environment
```bash
# Clone repository
git clone https://github.com/afaryab/PyBrowser.git
cd PyBrowser

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
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

### Code Quality Checks
```bash
# Format code
black src/pybrowser tests

# Lint code
flake8 src/pybrowser

# Type check
mypy src/pybrowser --ignore-missing-imports
```

### Running the Application
```bash
# Set required environment variables
export PYBROWSER_CLIENT_ID="your_client_id"
export PYBROWSER_CLIENT_SECRET="your_client_secret"
export PYBROWSER_API_URL="https://api.example.com"

# Run application
python -m pybrowser.main
```

## Git Workflow

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches
- `release/*`: Release preparation branches

### Commit Messages
Follow Conventional Commits specification:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Example:
```
feat: add OAuth authentication support

- Implement OAuth2 flow with authorization code grant
- Add secure token storage using keyring
- Create login dialog with web view
```

### Pull Request Process
1. Create feature branch from `develop`
2. Make changes and commit
3. Write/update tests
4. Run code quality checks
5. Push branch and create PR
6. Wait for CI checks to pass
7. Get code review approval
8. Merge to `develop`

## Testing Guidelines

### Unit Tests
- Test individual functions and classes
- Mock external dependencies
- Aim for >80% code coverage
- Place in `tests/test_*.py`

### Integration Tests
- Test component interactions
- Use real dependencies where possible
- Mark with `@pytest.mark.integration`

### Test Structure
```python
def test_function_name_scenario():
    """Test description."""
    # Arrange
    setup_data = create_test_data()
    
    # Act
    result = function_under_test(setup_data)
    
    # Assert
    assert result == expected_value
```

## Security Best Practices

1. **Credential Storage**: Always use keyring for storing sensitive data
2. **Input Validation**: Validate all user inputs using Pydantic models
3. **HTTPS Only**: Enforce HTTPS for all API communications
4. **Token Refresh**: Implement token refresh logic for OAuth
5. **Error Handling**: Never expose sensitive information in error messages

## API Integration

### Backend API Endpoints
The application expects the following endpoints:

- `GET /api/user/profile`: Get user profile
- `GET /api/teams`: List user teams
- `GET /api/teams/{team_id}/applications`: List team applications
- `GET /api/applications/{app_id}/quick-links`: List application quick links

### Response Format
All endpoints should return JSON with appropriate status codes.

Example response for teams:
```json
{
  "teams": [
    {
      "id": "team1",
      "name": "Engineering",
      "description": "Engineering team",
      "applications": []
    }
  ]
}
```

## UI Guidelines

### Layout Structure
- Left sidebar: Application switcher (max 250px)
- Top toolbar: Quick links for current application
- Main area: Web view with tabs
- Menu bar: File, View menus

### User Experience
- Show loading indicators for API calls
- Display user-friendly error messages
- Persist window size and position
- Auto-refresh data on focus

## Building and Releasing

### Creating a Release
1. Update version in `src/pybrowser/__init__.py`
2. Update CHANGELOG.md
3. Commit changes
4. Create and push tag: `git tag v0.1.0 && git push origin v0.1.0`
5. GitHub Actions will automatically build and create release

### Manual Build
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --name pybrowser \
  --onefile \
  --windowed \
  --add-data "src/pybrowser:pybrowser" \
  src/pybrowser/main.py
```

## Troubleshooting

### Common Issues

**Issue**: PyQt6 import errors
**Solution**: Install system dependencies (see CI workflow for list)

**Issue**: OAuth redirect not working
**Solution**: Ensure redirect URI matches OAuth provider configuration

**Issue**: Keyring backend not available
**Solution**: Install appropriate keyring backend for your OS

## Contributing

1. Read CONTRIBUTING.md (if exists)
2. Follow code style guidelines
3. Write tests for new features
4. Update documentation
5. Submit PR with clear description

## Resources

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
