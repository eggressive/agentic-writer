"""Tests for the publisher agent."""

import json
import tempfile
from pathlib import Path
import pytest
from src.agents.publisher import PublisherAgent


@pytest.fixture
def sample_article():
    """Sample article data for testing."""
    return {
        "title": "Test Article",
        "topic": "Testing",
        "content": "# Test Article\n\nThis is a test article content.",
        "word_count": 100,
        "tags": ["test", "article", "sample"],
        "meta_description": "A test article for unit testing",
        "images": []
    }


def test_save_to_file(sample_article):
    """Test saving article to file system."""
    with tempfile.TemporaryDirectory() as temp_dir:
        publisher = PublisherAgent()
        result = publisher.save_to_file(sample_article, output_dir=temp_dir)
        
        assert result["success"] is True
        assert result["platform"] == "file"
        assert "markdown_file" in result
        assert "metadata_file" in result
        
        # Check files exist
        md_file = Path(result["markdown_file"])
        json_file = Path(result["metadata_file"])
        
        assert md_file.exists()
        assert json_file.exists()
        
        # Verify content
        with open(md_file, "r") as f:
            content = f.read()
            assert "Test Article" in content
            assert "test, article, sample" in content
        
        with open(json_file, "r") as f:
            metadata = json.load(f)
            assert metadata["title"] == "Test Article"
            assert metadata["word_count"] == 100


def test_publish_file_platform(sample_article):
    """Test publishing to file platform."""
    with tempfile.TemporaryDirectory() as temp_dir:
        publisher = PublisherAgent()
        results = publisher.publish(sample_article, platforms=["file"], output_dir=temp_dir)
        
        assert "file" in results
        assert results["file"]["success"] is True


def test_publish_medium_without_token(sample_article):
    """Test Medium publishing without token."""
    publisher = PublisherAgent()
    result = publisher.publish_to_medium(sample_article)
    
    assert result["success"] is False
    assert result["platform"] == "medium"
    assert "token not configured" in result["error"].lower()


def test_publish_unknown_platform(sample_article):
    """Test publishing to unknown platform."""
    publisher = PublisherAgent()
    results = publisher.publish(sample_article, platforms=["unknown"])
    
    assert "unknown" in results
    assert results["unknown"]["success"] is False
