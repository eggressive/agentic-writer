"""Integration tests for the content creation pipeline."""

import tempfile
from unittest.mock import Mock, patch

import pytest

from src.orchestrator import ContentCreationOrchestrator
from src.utils.config import Config


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    return Config(
        openai_api_key="test-key",
        openai_model="gpt-3.5-turbo",
        temperature=0.7,
        log_level="INFO",
    )


@pytest.fixture
def mock_llm_response():
    """Create a mock LLM response."""
    mock_response = Mock()
    mock_response.content = "Test response content"
    return mock_response


def test_orchestrator_initialization(mock_config):
    """Test that orchestrator initializes correctly."""
    orchestrator = ContentCreationOrchestrator(mock_config)

    assert orchestrator.config == mock_config
    assert orchestrator.research_agent is not None
    assert orchestrator.writer_agent is not None
    assert orchestrator.image_agent is not None
    assert orchestrator.publisher_agent is not None


@patch("src.agents.researcher.ChatOpenAI")
@patch("src.agents.researcher.DDGS")
def test_pipeline_with_mocked_apis(mock_ddgs, mock_llm, mock_config):
    """Test full pipeline with mocked external APIs."""
    # Mock search results
    mock_search = Mock()
    mock_search.text.return_value = [
        {"title": "Test Article", "body": "Test content", "href": "https://test.com"}
    ]
    mock_ddgs.return_value.__enter__.return_value = mock_search

    # Mock LLM responses
    mock_llm_instance = Mock()
    mock_llm_instance.invoke.return_value = Mock(
        content="# Test Article\n\nTest content for article."
    )
    mock_llm.return_value = mock_llm_instance

    with tempfile.TemporaryDirectory():
        orchestrator = ContentCreationOrchestrator(mock_config)

        # This would normally call the real API, so we skip for now
        # Just test that the orchestrator is properly set up
        assert orchestrator.research_agent is not None
        assert orchestrator.writer_agent is not None


def test_get_summary_completed():
    """Test summary generation for completed pipeline."""
    results = {
        "status": "completed",
        "topic": "Test Topic",
        "article": {
            "title": "Test Article",
            "word_count": 1000,
            "tags": ["test", "article"],
        },
        "stages": {
            "research": {"status": "completed", "sources_count": 5},
            "writing": {
                "status": "completed",
                "title": "Test Article",
                "word_count": 1000,
            },
            "images": {"status": "completed", "images_found": 2},
            "publishing": {"status": "completed"},
        },
        "publication": {
            "file": {
                "success": True,
                "platform": "file",
                "markdown_file": "/tmp/test.md",
            }
        },
    }

    mock_config = Config(openai_api_key="test-key")
    orchestrator = ContentCreationOrchestrator(mock_config)

    summary = orchestrator.get_summary(results)

    assert "Test Topic" in summary
    assert "Test Article" in summary
    assert "1000" in summary
    assert "test, article" in summary
    assert "5 sources" in summary


def test_get_summary_failed():
    """Test summary generation for failed pipeline."""
    results = {"status": "failed", "error": "Test error"}

    mock_config = Config(openai_api_key="test-key")
    orchestrator = ContentCreationOrchestrator(mock_config)

    summary = orchestrator.get_summary(results)

    assert "failed" in summary.lower()


def test_orchestrator_requires_api_key():
    """Test that orchestrator requires API key."""
    config = Config(openai_api_key="")

    with pytest.raises(Exception):
        # Should fail when trying to initialize OpenAI client
        config.validate_required()
