# Contributing to Agentic-Writer

Thank you for your interest in contributing to Agentic-Writer! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## Code of Conduct

### Our Standards

- **Be respectful and inclusive** - Welcome all contributors
- **Be constructive** - Provide helpful feedback
- **Be collaborative** - Work together towards common goals
- **Be patient** - Help newcomers learn
- **Be professional** - Maintain a positive environment

### Unacceptable Behavior

- Harassment or discrimination of any kind
- Trolling or insulting comments
- Spam or off-topic content
- Sharing others' private information
- Disruptive behavior

**Violations**: Report to maintainers via GitHub or email.

## Getting Started

### Prerequisites

- Git knowledge
- Python 3.8+ experience
- Understanding of LangChain and AI agents (helpful)
- Familiarity with the codebase

### First Steps

1. **Star the repository** ⭐
2. **Fork the repository** on GitHub
3. **Read the documentation**:
   - [README](https://github.com/eggressive/agentic-writer/blob/main/README.md)
   - [Architecture](Architecture.md)
   - [Usage Guide](Usage-Guide.md)
4. **Join discussions** on GitHub
5. **Look for good first issues**

### Good First Issues

Look for issues labeled:

- `good first issue` - Perfect for newcomers
- `help wanted` - Community help needed
- `documentation` - Docs improvements
- `bug` - Bug fixes needed

## How to Contribute

### Reporting Bugs

1. **Search existing issues** first
2. **Use the bug report template**
3. **Include**:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System info (OS, Python version)
   - Error messages and logs
   - Configuration (redact API keys!)

**Example Bug Report**:

```markdown
### Description
Research agent fails when topic contains special characters

### Steps to Reproduce
1. Run: `python main.py create "AI & ML"`
2. Error occurs during research phase

### Expected
Should handle special characters in topics

### Actual
Error: UnicodeEncodeError...

### Environment
- OS: Ubuntu 22.04
- Python: 3.10.5
- Version: 0.1.0
```

### Suggesting Features

1. **Check the [Roadmap](Roadmap.md)** first
2. **Search existing issues**
3. **Use the feature request template**
4. **Include**:
   - Clear description
   - Use case and benefits
   - Proposed implementation (optional)
   - Examples (optional)

**Example Feature Request**:

```markdown
### Feature
Support for custom article length

### Use Case
Users want to generate articles of varying lengths 
(500 words, 2000 words, etc.)

### Proposed Implementation
Add `--word-count` CLI option and config parameter

### Benefits
- More flexibility
- Better control over output
- Wider use cases
```

### Improving Documentation

Documentation improvements are always welcome!

**What to improve**:

- Fix typos or grammar
- Add examples
- Clarify confusing sections
- Add diagrams or visuals
- Improve code comments
- Update outdated information

**Process**:

1. Fork repository
2. Edit documentation
3. Submit PR
4. No tests required for docs-only changes

## Development Setup

### 1. Fork and Clone

```bash
# Fork on GitHub first
git clone https://github.com/YOUR_USERNAME/agentic-writer.git
cd agentic-writer
```

### 2. Create Branch

```bash
git checkout -b feature/amazing-feature
# or
git checkout -b fix/bug-description
```

**Branch naming**:

- `feature/feature-name` - New features
- `fix/bug-name` - Bug fixes
- `docs/change-description` - Documentation
- `refactor/component-name` - Code refactoring
- `test/test-description` - Test additions

### 3. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black ruff

# Configure environment
cp .env.example .env
# Add your API keys to .env
```

### 4. Verify Setup

```bash
# Run verification
python verify_installation.py

# Run tests
pytest tests/ -v

# Check code formatting
black --check src/ tests/

# Check linting
ruff check src/ tests/
```

## Development Workflow

### 1. Make Changes

- Keep changes focused and minimal
- Follow existing code style
- Add comments where needed
- Update docstrings

### 2. Write Tests

```bash
# Add tests in tests/ directory
# Test file: tests/test_your_feature.py

def test_new_feature():
    """Test new feature functionality."""
    # Your test code
    assert result == expected
```

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_config.py -v
```

### 4. Format Code

```bash
# Format with black
black src/ tests/

# Check formatting
black --check src/ tests/
```

### 5. Lint Code

```bash
# Run ruff
ruff check src/ tests/ --fix

# Check without fixing
ruff check src/ tests/
```

### 6. Commit Changes

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "feat: add custom article length support"
```

**Commit message format**:

```text
<type>: <description>

[optional body]

[optional footer]
```

**Types**:

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `test` - Tests
- `refactor` - Code refactoring
- `style` - Formatting
- `chore` - Maintenance

**Examples**:

```bash
git commit -m "feat: add WordPress publishing support"
git commit -m "fix: handle special characters in topics"
git commit -m "docs: improve installation guide"
git commit -m "test: add tests for WriterAgent"
```

### 7. Push Changes

```bash
git push origin feature/amazing-feature
```

### 8. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out PR template
5. Submit PR

## Code Standards

### Python Style

Follow PEP 8 with these specifics:

**Line Length**: 88 characters (Black default)

*Note: This differs from PEP 8's traditional 79-character limit. We use Black's default of 88 characters for better code readability.*

**Quotes**: Double quotes for strings

```python
# Good
message = "Hello, world!"

# Avoid
message = 'Hello, world!'
```

**Type Hints**: Use where helpful

```python
def process_data(topic: str, style: str = "professional") -> Dict[str, Any]:
    """Process data and return results."""
    pass
```

**Docstrings**: Google-style for all public functions

```python
def create_article(topic: str, style: str) -> Dict[str, Any]:
    """Create article on given topic.
    
    Args:
        topic: The topic to write about
        style: Writing style to use
        
    Returns:
        Dictionary containing article data including:
        - title: Article title
        - content: Full article content
        - word_count: Number of words
        
    Raises:
        ValueError: If topic is empty
        APIError: If OpenAI API fails
    """
    pass
```

**Imports**: Organized and sorted

```python
# Standard library
import logging
import os
from typing import Dict, List, Any, Optional

# Third-party
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

# Local
from src.utils import Config
from src.agents import ResearchAgent
```

### Project Structure

```python
# Agent structure
class Agent:
    """Agent description."""
    
    def __init__(self, llm: ChatOpenAI):
        """Initialize agent."""
        self.llm = llm
        self.logger = logging.getLogger(__name__)
        
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data."""
        self.logger.info("Processing...")
        try:
            result = self._perform_task(data)
            return {"success": True, "data": result}
        except Exception as e:
            self.logger.error(f"Error: {e}")
            raise
```

### Best Practices

1. **Single Responsibility** - Each function/class does one thing
2. **DRY** - Don't repeat yourself
3. **KISS** - Keep it simple
4. **Error Handling** - Handle errors gracefully
5. **Logging** - Use logging, not print()
6. **Comments** - Explain why, not what
7. **Type Safety** - Use type hints

## Testing

### Writing Tests

**Location**: `tests/` directory

**Structure**:

```python
"""Tests for WriterAgent."""

import pytest
from src.agents import WriterAgent
from unittest.mock import Mock, patch


class TestWriterAgent:
    """Test WriterAgent functionality."""
    
    def test_write_article(self):
        """Test article writing."""
        # Arrange
        mock_llm = Mock()
        writer = WriterAgent(mock_llm)
        research_data = {...}
        
        # Act
        result = writer.write_article(research_data)
        
        # Assert
        assert result["title"] is not None
        assert result["word_count"] > 0
        
    def test_write_article_error(self):
        """Test error handling."""
        writer = WriterAgent(Mock())
        
        with pytest.raises(ValueError):
            writer.write_article({})
```

### Test Coverage

Aim for:

- **Core components**: >80% coverage
- **Utilities**: 100% coverage
- **Integration**: Key workflows covered

Check coverage:

```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

### Mocking

Mock external APIs in tests:

```python
@patch('src.agents.researcher.DDGS')
def test_search_web(mock_ddgs):
    """Test web search with mocked DuckDuckGo."""
    mock_ddgs.return_value.text.return_value = [
        {"title": "Result 1", "body": "Content", "href": "url"}
    ]
    
    researcher = ResearchAgent(Mock())
    results = researcher.search_web("test topic")
    
    assert len(results) > 0
```

## Documentation

### Code Documentation

**Docstrings**: All public functions/classes

```python
def function(param: str) -> Dict:
    """Brief description.
    
    Longer description if needed.
    
    Args:
        param: Parameter description
        
    Returns:
        Dictionary with keys:
        - key1: Description
        - key2: Description
        
    Raises:
        ValueError: When something is wrong
    """
```

**Comments**: Explain complex logic

```python
# Calculate optimal temperature based on style
# Higher temp for creative styles, lower for factual
if style in ["casual", "creative"]:
    temperature = 0.8  # More creative
else:
    temperature = 0.3  # More focused
```

### User Documentation

Update when adding features:

- README.md - Overview and quick start
- Wiki pages - Detailed documentation
- DEMO.md - Usage examples
- ARCHITECTURE.md - System design

## Pull Request Process

### Before Submitting

- [ ] Code follows style guide
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] Commits are clean and descriptive
- [ ] Branch is up to date with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring
- [ ] Tests

## Testing
How was this tested?

## Checklist
- [ ] Tests pass
- [ ] Code formatted (black)
- [ ] Code linted (ruff)
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated checks** run (tests, linting)
2. **Maintainer review** (1-3 days)
3. **Feedback addressed**
4. **Approval and merge**

### After Merge

- Your contribution is live! 🎉
- You're credited in contributors
- Mentioned in release notes
- Thank you! 🙏

## Community

### Communication Channels

- **GitHub Issues** - Bug reports, features
- **GitHub Discussions** - Questions, ideas
- **Pull Requests** - Code contributions

### Getting Help

- Read the documentation
- Search existing issues
- Ask in discussions
- Be patient and respectful

### Recognition

Contributors are recognized through:

- GitHub contributors page
- Release notes
- Special mentions for significant contributions
- Community appreciation

## Questions?

- 📖 Read the [documentation](Home.md)
- 💬 Ask in [Discussions](https://github.com/eggressive/agentic-writer/discussions)
- 🐛 Report [Issues](https://github.com/eggressive/agentic-writer/issues)

## Thank You!

Every contribution, no matter how small, makes Agentic-Writer better. Thank you for being part of our community! 🎉

---

**Ready to contribute?** [Fork the repository](https://github.com/eggressive/agentic-writer/fork) and get started!

**Have questions?** [Open a discussion](https://github.com/eggressive/agentic-writer/discussions) - we're here to help!
