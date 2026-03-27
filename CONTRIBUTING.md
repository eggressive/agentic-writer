# Contributing to Agentic-Writer

Thank you for your interest in contributing to Agentic-Writer! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Maintain a professional environment

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/eggressive/agentic-writer/issues)
1. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Relevant logs or error messages

### Suggesting Features

1. Check existing issues for similar suggestions
1. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Proposed implementation (if applicable)

### Pull Requests

1. Fork the repository
1. Create a feature branch (`git checkout -b feat/amazing-feature`)
1. Make your changes
1. Write or update tests
1. Run the preflight checks (all three must pass before CI will accept your PR):

   ```bash
   black src/ tests/                            # fix formatting
   ruff check src/ tests/ --fix                 # fix lint issues
   pytest --cov=src --cov-fail-under=60         # run tests
   ```

1. Commit using [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, etc.)
1. Push to your fork
1. Open a Pull Request (the PR template will guide you)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Setup Instructions

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/agentic-writer.git
cd agentic-writer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies (includes dev tools: pytest, black, ruff)
pip install -r requirements.txt

# Set up pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install

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

```text
agentic-writer/
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

We use [Conventional Commits](https://www.conventionalcommits.org/) for automated release management.

### Format

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Examples

```text
feat: add support for custom image generation
fix: resolve crash when API key is missing
docs: update installation instructions
chore: upgrade langchain dependencies
```

### Commit Types

- `feat:` New feature (triggers minor version bump)
- `fix:` Bug fix (triggers patch version bump)
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Maintenance tasks
- `build:` Build system changes
- `ci:` CI/CD changes

> **Note:** Commits with certain types (such as `style:`, `chore:`, `build:`, and `ci:`) do **not** trigger changelog entries and will not appear in the generated changelog. Only `feat:`, `fix:`, and other types explicitly configured in `release-please-config.json` are included. This helps keep the changelog focused on user-facing changes.

### Breaking Changes

For breaking changes, add `!` after the type or add `BREAKING CHANGE:` in the footer:

```text
feat!: change API signature for ContentCreationOrchestrator

BREAKING CHANGE: create_content() now requires additional parameter
```

This triggers a major version bump (e.g., 0.1.0 → 1.0.0)

## Adding New Features

### Adding a New Agent

1. Create agent file in `src/agents/`
1. Implement agent class with required methods
1. Add to `src/agents/__init__.py`
1. Update orchestrator to use new agent
1. Write tests
1. Update documentation

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
1. Update `publish()` method to handle new platform
1. Add configuration for platform API keys
1. Write tests
1. Update documentation

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

## CI Pipeline

All PRs are validated by the CI pipeline (`.github/workflows/ci.yml`):

1. **Preflight gate** — `black --check` and `ruff check` must pass
1. **Test gate** — `pytest` with minimum 60% coverage

See `.github/merge-policy.yml` for the machine-readable merge contract defining risk tiers and required checks per tier.

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

We use [release-please](https://github.com/googleapis/release-please) for automated release management based on [Semantic Versioning](https://semver.org/).

### Repository Setup for Release-Please

The release-please workflow requires a Personal Access Token (PAT) to create pull requests. Repository maintainers must:

1. Create a GitHub Personal Access Token (classic) with `repo` scope
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select the `repo` scope (full control of private repositories)
   - Generate and copy the token
2. Add the token as a repository secret named `RELEASE_PLEASE_TOKEN`
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `RELEASE_PLEASE_TOKEN`
   - Value: Paste the PAT from step 1
3. The workflow will use this token to create release PRs

This is required because organization or repository security settings may prevent the default `GITHUB_TOKEN` from creating pull requests.

### Version Numbering (MAJOR.MINOR.PATCH)

- **MAJOR**: Breaking changes (e.g., 1.0.0 → 2.0.0)
- **MINOR**: New features (backwards compatible) (e.g., 1.0.0 → 1.1.0)
- **PATCH**: Bug fixes (e.g., 1.0.0 → 1.0.1)

### How Releases Work

1. **Commits**: Use conventional commits (see Commit Message Guidelines above)
1. **Pull Request**: When commits are merged to `main`, release-please analyzes them
1. **Release PR**: release-please automatically creates/updates a release PR with:
   - Updated version numbers in `setup.py` and `src/__init__.py`
   - Generated CHANGELOG.md entries
   - Proper version bump based on commit types
1. **Publishing**: When the release PR is merged:
   - A GitHub release is created automatically
   - Release notes are generated from commits
   - Version tags are created

### Manual Release Steps

Maintainers only need to:

1. Review and merge the release-please PR when ready
1. The GitHub release is created automatically
1. Optional: Publish to PyPI manually (if configured)

### Creating a Release

No manual version bumping needed! Just:

1. Use conventional commits in your PRs
1. Merge PRs to `main`
1. Wait for release-please to create a release PR
1. Review and merge the release PR when ready for release

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

Thank you for contributing to Agentic-Writer! 🎉
