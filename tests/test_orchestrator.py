"""Tests for the ContentCreationOrchestrator."""

import tempfile
import pytest
from unittest.mock import Mock, patch
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


@patch("src.orchestrator.ImageAgent")
@patch("src.orchestrator.WriterAgent")
@patch("src.orchestrator.ResearchAgent")
@patch("src.orchestrator.PublisherAgent")
@patch("src.orchestrator.ChatOpenAI")
def test_create_content_defaults_platforms_to_file(
    mock_llm, mock_publisher, mock_researcher, mock_writer, mock_image, mock_config
):
    """Test create_content defaults platforms parameter to ['file']."""
    # Setup mocks
    mock_llm_instance = Mock()
    mock_llm.return_value = mock_llm_instance
    
    mock_researcher_instance = Mock()
    mock_researcher_instance.research.return_value = {
        "topic": "Test",
        "analysis": "Analysis",
        "synthesis": "Synthesis",
        "search_results": [],
        "sources_count": 0
    }
    mock_researcher.return_value = mock_researcher_instance
    
    mock_writer_instance = Mock()
    # Return a dict-like mock that supports item assignment
    article_dict = {
        "content": "# Test\n\nContent",
        "title": "Test",
        "word_count": 100,
        "meta_description": "Meta",
        "tags": ["tag1"]
    }
    mock_writer_instance.write_article.return_value = article_dict
    mock_writer.return_value = mock_writer_instance
    
    mock_image_instance = Mock()
    mock_image_instance.find_images.return_value = []
    mock_image.return_value = mock_image_instance
    
    mock_publisher_instance = Mock()
    mock_publisher_instance.publish.return_value = [
        {
            "success": True,
            "platform": "file",
            "markdown_file": "/tmp/test.md"
        }
    ]
    mock_publisher.return_value = mock_publisher_instance
    
    with tempfile.TemporaryDirectory() as tmpdir:
        orchestrator = ContentCreationOrchestrator(mock_config)
        
        # Call without specifying platforms - should default to ["file"]
        result = orchestrator.create_content(
            topic="Test Topic",
            style="professional",
            target_audience="experts",
            platforms=None,  # Explicitly pass None
            output_dir=tmpdir
        )
        
        # Verify publisher was called with ["file"]
        mock_publisher_instance.publish.assert_called_once()
        call_args = mock_publisher_instance.publish.call_args
        assert call_args[1]["platforms"] == ["file"]


@patch("src.orchestrator.ImageAgent")
@patch("src.orchestrator.WriterAgent")
@patch("src.orchestrator.ResearchAgent")
@patch("src.orchestrator.PublisherAgent")
@patch("src.orchestrator.ChatOpenAI")
def test_create_content_handles_exception(
    mock_llm, mock_publisher, mock_researcher, mock_writer, mock_image, mock_config
):
    """Test create_content handles exceptions and sets failure status."""
    # Setup mocks
    mock_llm_instance = Mock()
    mock_llm.return_value = mock_llm_instance
    
    mock_researcher_instance = Mock()
    mock_researcher_instance.research.side_effect = Exception("Research failed")
    mock_researcher.return_value = mock_researcher_instance
    
    mock_writer.return_value = Mock()
    mock_image.return_value = Mock()
    mock_publisher.return_value = Mock()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        orchestrator = ContentCreationOrchestrator(mock_config)
        
        # Call should raise exception
        with pytest.raises(Exception, match="Research failed"):
            orchestrator.create_content(
                topic="Test Topic",
                style="professional",
                target_audience="experts",
                platforms=["file"],
                output_dir=tmpdir
            )


def test_get_summary_with_failed_publication(mock_config):
    """Test get_summary handles failed publication results."""
    orchestrator = ContentCreationOrchestrator(mock_config)
    
    results = {
        "status": "completed",
        "topic": "Test Topic",
        "article": {
            "title": "Test Article",
            "word_count": 1000,
            "tags": ["test"],
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
                "success": False,
                "platform": "file",
                "error": "Failed to write file"
            }
        },
    }
    
    summary = orchestrator.get_summary(results)
    
    # Should mention the failure
    assert "Failed" in summary or "failed" in summary
    assert "Failed to write file" in summary
