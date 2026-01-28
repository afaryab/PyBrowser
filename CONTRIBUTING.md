# Contributing to PyBrowser

Thank you for your interest in contributing to PyBrowser! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate in all interactions. We aim to create a welcoming environment for all contributors.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/PyBrowser.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Commit your changes following our commit message guidelines
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/afaryab/PyBrowser.git
cd PyBrowser

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, missing semi-colons, etc.)
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

## Code Style

- Follow PEP 8 style guide
- Use type hints for all function signatures
- Maximum line length: 127 characters
- Use Black for code formatting: `black src/pybrowser tests`
- Use flake8 for linting: `flake8 src/pybrowser`
- Use mypy for type checking: `mypy src/pybrowser --ignore-missing-imports`

## Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Run tests before submitting PR: `pytest tests/ -v --cov=pybrowser`
- Use descriptive test names and docstrings

## Pull Request Process

1. Update documentation if needed
2. Add/update tests for your changes
3. Ensure all tests pass
4. Ensure code quality checks pass (black, flake8, mypy)
5. Update CHANGELOG.md with your changes
6. Create a Pull Request with a clear description of changes
7. Link any related issues
8. Wait for review and address feedback

## Reporting Bugs

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Any error messages or logs

## Suggesting Enhancements

When suggesting enhancements, please:

- Check if the feature has already been suggested
- Provide a clear description of the enhancement
- Explain the use case and benefits
- Consider backward compatibility

## Questions?

Feel free to open an issue for any questions about contributing.

Thank you for contributing to PyBrowser!
