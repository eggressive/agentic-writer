# Contributing to Agentic-V

Thank you for your interest in contributing to Agentic-V! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Maintain a professional environment

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/eggressive/agentic-v/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Relevant logs or error messages

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Proposed implementation (if applicable)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
6. Format code with black
7. Run linting with ruff
8. Commit with clear messages
9. Push to your fork
10. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Setup Instructions

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/agentic-v.git
cd agentic-v

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black ruff

# Set up environment
cp .env.example .env
# Add your API keys to .env
```

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

- Line length: 88 characters (black default)
- Use double quotes for strings
- Use type hints where helpful
- Write docstrings for all public functions/classes

### Formatting

Format your code with black:

```bash
black src/ tests/
```

### Linting

Check your code with ruff:

```bash
ruff check src/ tests/ --fix
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_config.py -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use fixtures for common setup
- Aim for high test coverage
- Test edge cases and error conditions

Example test:

```python
import pytest
from src.utils.config import Config


def test_config_validation():
    """Test configuration validation."""
    config = Config(openai_api_key="test-key")
    config.validate_required()  # Should not raise


def test_config_validation_fails():
    """Test validation fails without API key."""
    config = Config(openai_api_key="")
    with pytest.raises(ValueError):
        config.validate_required()
```

## Project Structure

```
agentic-v/
├── src/                    # Source code
│   ├── agents/            # Agent implementations
│   ├── utils/             # Utility functions
│   ├── orchestrator.py    # Main orchestration
│   └── cli.py             # CLI interface
├── tests/                 # Test suite
├── output/                # Default output directory
├── main.py               # Entry point
├── example.py            # Example usage
├── requirements.txt      # Dependencies
└── setup.py             # Package setup
```

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
Add feature X to improve Y

- Implement feature X
- Add tests for X
- Update documentation
```

Types of commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Maintenance tasks

## Adding New Features

### Adding a New Agent

1. Create agent file in `src/agents/`
2. Implement agent class with required methods
3. Add to `src/agents/__init__.py`
4. Update orchestrator to use new agent
5. Write tests
6. Update documentation

Example agent structure:

```python
"""Description of the agent."""

import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI


class NewAgent:
    """Agent description."""

    def __init__(self, llm: ChatOpenAI):
        """Initialize the agent."""
        self.llm = llm
        self.logger = logging.getLogger(__name__)

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data and return results."""
        self.logger.info("Processing data...")
        # Implementation
        return {"result": "success"}
```

### Adding a Publishing Platform

1. Add platform method to `PublisherAgent`
2. Update `publish()` method to handle new platform
3. Add configuration for platform API keys
4. Write tests
5. Update documentation

## Documentation

### Code Documentation

- Write docstrings for all public classes and functions
- Use Google-style docstrings
- Include type hints
- Document parameters and return values

Example:

```python
def research(self, topic: str) -> Dict[str, Any]:
    """Conduct full research on a topic.
    
    Args:
        topic: Topic to research
        
    Returns:
        Dictionary containing research findings including:
        - topic: Original topic
        - analysis: Topic analysis
        - search_results: List of search results
        - synthesis: Research synthesis
        - sources_count: Number of sources found
    """
    pass
```

### User Documentation

- Update README.md for user-facing changes
- Add examples for new features
- Update DEMO.md with usage examples
- Keep documentation in sync with code

## Review Process

### What We Look For

- **Functionality**: Does it work as intended?
- **Tests**: Are there tests? Do they pass?
- **Code Quality**: Is it readable and maintainable?
- **Documentation**: Is it documented?
- **Style**: Does it follow our style guide?

### Review Timeline

- Initial review: 2-3 days
- Follow-up: 1-2 days per iteration
- Merge: After approval and CI passes

## Release Process

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes

## Getting Help

- Open a discussion on GitHub
- Check existing documentation
- Look at similar implementations
- Ask questions in issues

## Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes
- Special mentions for significant contributions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to reach out by:
- Opening an issue
- Starting a discussion
- Contacting maintainers

Thank you for contributing to Agentic-V! 🎉
