"""Tests for per-agent LLM configuration."""

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


@patch("src.orchestrator.AudienceStrategist")
@patch("src.orchestrator.ImageAgent")
@patch("src.orchestrator.WriterAgent")
@patch("src.orchestrator.ResearchAgent")
@patch("src.orchestrator.PublisherAgent")
@patch("src.orchestrator.ChatOpenAI")
def test_orchestrator_has_per_agent_llms(
    mock_chat,
    mock_publisher,
    mock_researcher,
    mock_writer,
    mock_image,
    mock_audience,
    mock_config,
):
    """Test that the orchestrator creates separate LLM instances for creative, analytical, and writer tasks."""
    mock_chat.return_value = Mock()

    orchestrator = ContentCreationOrchestrator(mock_config)

    assert hasattr(orchestrator, "llm_creative")
    assert hasattr(orchestrator, "llm_analytical")
    assert hasattr(orchestrator, "llm_writer")
