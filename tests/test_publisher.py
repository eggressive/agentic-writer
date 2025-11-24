"""Tests for the publisher agent."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch
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
        "images": [],
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
        results = publisher.publish(
            sample_article, platforms=["file"], output_dir=temp_dir
        )

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


def test_publish_to_medium_with_token(sample_article):
    """Test Medium publishing with token (simulated success)."""
    publisher = PublisherAgent(medium_token="test_token")
    result = publisher.publish_to_medium(sample_article)

    assert result["success"] is True
    assert result["platform"] == "medium"
    assert "message" in result
    assert "url" in result


def test_save_to_file_with_images():
    """Test saving article with images to file system."""
    article_with_images = {
        "title": "Article With Images",
        "topic": "Images Test",
        "content": "This article has images.",
        "word_count": 50,
        "tags": ["images", "test"],
        "meta_description": "An article with images",
        "images": [
            {
                "description": "A beautiful sunset",
                "url": "https://example.com/sunset.jpg",
                "author": "John Doe",
                "author_url": "https://example.com/johndoe",
                "source": "Unsplash",
            },
            {
                "description": "Mountain landscape",
                "url": "https://example.com/mountain.jpg",
                "author": "Jane Smith",
                "author_url": "",
                "source": "Unsplash",
            },
        ],
    }

    with tempfile.TemporaryDirectory() as temp_dir:
        publisher = PublisherAgent()
        result = publisher.save_to_file(article_with_images, output_dir=temp_dir)

        assert result["success"] is True
        assert result["platform"] == "file"

        # Verify images are in the markdown
        md_file = Path(result["markdown_file"])
        with open(md_file, "r") as f:
            content = f.read()
            assert "## Visuals" in content
            assert "A beautiful sunset" in content
            assert "https://example.com/sunset.jpg" in content
            assert "[John Doe]" in content
            assert "Photo by Jane Smith on Unsplash" in content


def test_save_to_file_exception_handling(sample_article):
    """Test exception handling when saving to file fails."""
    publisher = PublisherAgent()

    # Mock Path.mkdir to raise an exception to test the except block
    with patch.object(Path, "mkdir", side_effect=PermissionError("Permission denied")):
        result = publisher.save_to_file(sample_article, output_dir="/test/dir")

    assert result["success"] is False
    assert result["platform"] == "file"
    assert "error" in result


def test_publish_default_platforms(sample_article):
    """Test publishing with default platforms (None)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        publisher = PublisherAgent()
        results = publisher.publish(sample_article, platforms=None, output_dir=temp_dir)

        # Default should be file platform
        assert "file" in results
        assert results["file"]["success"] is True


def test_publish_medium_platform_via_publish(sample_article):
    """Test Medium publishing through the main publish method."""
    publisher = PublisherAgent(medium_token="test_token")
    results = publisher.publish(sample_article, platforms=["medium"])

    assert "medium" in results
    assert results["medium"]["success"] is True
    assert results["medium"]["platform"] == "medium"


def test_publish_to_medium_exception_handling(sample_article):
    """Test Medium publishing exception handling."""
    publisher = PublisherAgent(medium_token="test_token")

    # Mock the logger.info to raise an exception to test the except block
    with patch.object(publisher.logger, "info", side_effect=Exception("API Error")):
        result = publisher.publish_to_medium(sample_article)

    assert result["success"] is False
    assert result["platform"] == "medium"
    assert "API Error" in result["error"]
