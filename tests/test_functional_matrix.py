"""Functional tests for article generation with parameter matrix."""

import os
import shutil
from unittest.mock import Mock, patch

import pytest

from src.orchestrator import ContentCreationOrchestrator
from src.utils.config import Config

# Test Matrix
TOPICS = ["Remote Work", "AI Ethics"]
STYLES = ["Professional", "Casual"]
AUDIENCES = ["Experts", "Beginners"]


@pytest.fixture
def output_dir():
    """Create and clean up a temporary output directory."""
    dir_path = "tests/output/functional"
    os.makedirs(dir_path, exist_ok=True)
    yield dir_path
    # Cleanup after tests
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    return Config(
        openai_api_key="test-key",
        openai_model="gpt-3.5-turbo",
        temperature=0.7,
    )


@pytest.mark.functional
@pytest.mark.parametrize("topic", TOPICS)
@pytest.mark.parametrize("style", STYLES)
@pytest.mark.parametrize("audience", AUDIENCES)
@patch("src.orchestrator.ChatOpenAI")
@patch("src.agents.researcher.DDGS")
def test_article_generation_matrix(
    mock_ddgs, mock_llm, topic, style, audience, mock_config, output_dir
):
    """Test article generation with various combinations of parameters."""

    # --- Mock Setup ---
    # Mock Search
    mock_search = Mock()
    mock_search.text.return_value = [
        {"title": f"Source for {topic}", "body": "Content", "href": "http://test.com"}
    ]
    mock_ddgs.return_value.__enter__.return_value = mock_search

    # Mock LLM
    mock_llm_instance = Mock()
    # We need to handle multiple calls (research, outline, writing, etc.)
    # A simple way is to return a generic response that works for all
    mock_llm_instance.invoke.return_value = Mock(
        content=f"# {topic}\n\nStyle: {style}\nAudience: {audience}\n\nContent goes here."
    )
    mock_llm.return_value = mock_llm_instance

    # --- Execution ---
    orchestrator = ContentCreationOrchestrator(mock_config)

    results = orchestrator.create_content(
        topic=topic,
        style=style,
        target_audience=audience,
        platforms=["file"],
        output_dir=output_dir,
    )

    # --- Verification ---
    assert results["status"] == "completed"
    assert results["stages"]["writing"]["status"] == "completed"

    # Verify file creation
    expected_filename = topic.lower().replace(" ", "_") + ".md"
    expected_path = os.path.join(output_dir, expected_filename)
    assert os.path.exists(expected_path)

    # Verify content (mocked content should be in the file)
    with open(expected_path, "r") as f:
        content = f.read()
        assert f"# {topic}" in content
        assert f"Style: {style}" in content
