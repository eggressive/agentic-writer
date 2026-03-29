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


# --- Ghost ---


def test_publish_to_ghost_without_credentials(sample_article):
    """Test Ghost publishing without credentials."""
    publisher = PublisherAgent()
    result = publisher.publish_to_ghost(sample_article)

    assert result["success"] is False
    assert result["platform"] == "ghost"
    assert "required" in result["error"].lower()


def test_publish_to_ghost_missing_api_key(sample_article):
    """Test Ghost publishing with URL but no API key."""
    publisher = PublisherAgent(ghost_api_url="https://myblog.ghost.io")
    result = publisher.publish_to_ghost(sample_article)

    assert result["success"] is False
    assert result["platform"] == "ghost"


def test_publish_to_ghost_with_credentials(sample_article):
    """Test Ghost publishing with credentials returns not-implemented error."""
    publisher = PublisherAgent(
        ghost_api_url="https://myblog.ghost.io",
        ghost_admin_api_key="test_id:test_secret",
    )
    result = publisher.publish_to_ghost(sample_article)

    assert result["success"] is False
    assert result["platform"] == "ghost"
    assert "not implemented" in result["error"].lower()


def test_publish_to_ghost_invalid_key_format(sample_article):
    """Test Ghost publishing with malformed API key (missing id:secret format)."""
    publisher = PublisherAgent(
        ghost_api_url="https://myblog.ghost.io",
        ghost_admin_api_key="invalid_key_no_colon",
    )
    result = publisher.publish_to_ghost(sample_article)

    assert result["success"] is False
    assert result["platform"] == "ghost"
    assert "id:secret" in result["error"]


def test_publish_to_ghost_exception_handling(sample_article):
    """Test Ghost publishing exception handling."""
    publisher = PublisherAgent(
        ghost_api_url="https://myblog.ghost.io",
        ghost_admin_api_key="test_id:test_secret",
    )
    with patch.object(
        publisher.logger, "info", side_effect=Exception("Ghost API Error")
    ):
        result = publisher.publish_to_ghost(sample_article)

    assert result["success"] is False
    assert result["platform"] == "ghost"
    assert "Ghost API Error" in result["error"]


def test_publish_ghost_via_publish_method(sample_article):
    """Test Ghost publishing through the main publish method returns not-implemented."""
    publisher = PublisherAgent(
        ghost_api_url="https://myblog.ghost.io",
        ghost_admin_api_key="test_id:test_secret",
    )
    results = publisher.publish(sample_article, platforms=["ghost"])

    assert "ghost" in results
    assert results["ghost"]["success"] is False
    assert results["ghost"]["platform"] == "ghost"


# --- WordPress ---


def test_publish_to_wordpress_without_credentials(sample_article):
    """Test WordPress publishing without credentials."""
    publisher = PublisherAgent()
    result = publisher.publish_to_wordpress(sample_article)

    assert result["success"] is False
    assert result["platform"] == "wordpress"
    assert "required" in result["error"].lower()


def test_publish_to_wordpress_partial_credentials(sample_article):
    """Test WordPress publishing with only URL (missing username/password)."""
    publisher = PublisherAgent(wordpress_url="https://myblog.com")
    result = publisher.publish_to_wordpress(sample_article)

    assert result["success"] is False
    assert result["platform"] == "wordpress"


def test_publish_to_wordpress_with_credentials(sample_article):
    """Test WordPress publishing with credentials returns not-implemented error."""
    publisher = PublisherAgent(
        wordpress_url="https://myblog.com",
        wordpress_username="admin",
        wordpress_app_password="xxxx yyyy zzzz",
    )
    result = publisher.publish_to_wordpress(sample_article)

    assert result["success"] is False
    assert result["platform"] == "wordpress"
    assert "not implemented" in result["error"].lower()


def test_publish_to_wordpress_exception_handling(sample_article):
    """Test WordPress publishing exception handling."""
    publisher = PublisherAgent(
        wordpress_url="https://myblog.com",
        wordpress_username="admin",
        wordpress_app_password="xxxx yyyy zzzz",
    )
    with patch.object(publisher.logger, "info", side_effect=Exception("WP API Error")):
        result = publisher.publish_to_wordpress(sample_article)

    assert result["success"] is False
    assert result["platform"] == "wordpress"
    assert "WP API Error" in result["error"]


def test_publish_wordpress_via_publish_method(sample_article):
    """Test WordPress publishing through the main publish method."""
    publisher = PublisherAgent(
        wordpress_url="https://myblog.com",
        wordpress_username="admin",
        wordpress_app_password="xxxx yyyy zzzz",
    )
    results = publisher.publish(sample_article, platforms=["wordpress"])

    assert "wordpress" in results
    assert results["wordpress"]["success"] is False
    assert results["wordpress"]["platform"] == "wordpress"


# --- Hashnode ---


def test_publish_to_hashnode_without_credentials(sample_article):
    """Test Hashnode publishing without credentials."""
    publisher = PublisherAgent()
    result = publisher.publish_to_hashnode(sample_article)

    assert result["success"] is False
    assert result["platform"] == "hashnode"
    assert "required" in result["error"].lower()


def test_publish_to_hashnode_missing_publication_id(sample_article):
    """Test Hashnode publishing with API key but no publication ID."""
    publisher = PublisherAgent(hashnode_api_key="test_key")
    result = publisher.publish_to_hashnode(sample_article)

    assert result["success"] is False
    assert result["platform"] == "hashnode"


def test_publish_to_hashnode_with_credentials(sample_article):
    """Test Hashnode publishing with credentials returns not-implemented error."""
    publisher = PublisherAgent(
        hashnode_api_key="test_hashnode_key",
        hashnode_publication_id="pub123",
    )
    result = publisher.publish_to_hashnode(sample_article)

    assert result["success"] is False
    assert result["platform"] == "hashnode"
    assert "not implemented" in result["error"].lower()


def test_publish_to_hashnode_exception_handling(sample_article):
    """Test Hashnode publishing exception handling."""
    publisher = PublisherAgent(
        hashnode_api_key="test_hashnode_key",
        hashnode_publication_id="pub123",
    )
    with patch.object(publisher.logger, "info", side_effect=Exception("HN API Error")):
        result = publisher.publish_to_hashnode(sample_article)

    assert result["success"] is False
    assert result["platform"] == "hashnode"
    assert "HN API Error" in result["error"]


def test_publish_hashnode_via_publish_method(sample_article):
    """Test Hashnode publishing through the main publish method."""
    publisher = PublisherAgent(
        hashnode_api_key="test_hashnode_key",
        hashnode_publication_id="pub123",
    )
    results = publisher.publish(sample_article, platforms=["hashnode"])

    assert "hashnode" in results
    assert results["hashnode"]["success"] is False
    assert results["hashnode"]["platform"] == "hashnode"


# --- _embed_images_in_content ---


def test_embed_images_no_images():
    """_embed_images_in_content returns content unchanged when images list is empty."""
    content = "## Intro\n\nSome text.\n"
    result = PublisherAgent._embed_images_in_content(content, [])
    assert result == content


def test_embed_images_all_unplaced_appended_at_end():
    """Images without a section key are appended after all content."""
    content = "## Intro\n\nSome text.\n"
    images = [
        {
            "description": "A photo",
            "url": "https://example.com/photo.jpg",
            "author": "Alice",
            "author_url": "https://example.com/alice",
            "source": "Unsplash",
        }
    ]
    result = PublisherAgent._embed_images_in_content(content, images)
    assert "https://example.com/photo.jpg" in result
    # Image appears after the original content
    assert result.index("https://example.com/photo.jpg") > result.index("Some text.")


def test_embed_images_with_section_inserted_after_first_paragraph():
    """Images with a matching section are embedded after the first paragraph."""
    content = (
        "## Introduction\n\n"
        "First paragraph text.\n\n"
        "## Conclusion\n\n"
        "Last paragraph.\n"
    )
    images = [
        {
            "section": "Introduction",
            "description": "Intro image",
            "url": "https://example.com/intro.jpg",
            "author": "Bob",
            "author_url": "https://example.com/bob",
            "source": "Unsplash",
        }
    ]
    result = PublisherAgent._embed_images_in_content(content, images)
    assert "https://example.com/intro.jpg" in result
    # Image must appear before Conclusion heading
    assert result.index("intro.jpg") < result.index("## Conclusion")


def test_embed_images_section_not_in_content_falls_to_end():
    """Images whose section heading doesn't exist in the article are appended at end."""
    content = "## Overview\n\nSome overview.\n"
    images = [
        {
            "section": "Nonexistent Section",
            "description": "Orphan image",
            "url": "https://example.com/orphan.jpg",
            "author": "Carol",
            "author_url": "",
            "source": "Unsplash",
        }
    ]
    result = PublisherAgent._embed_images_in_content(content, images)
    assert "https://example.com/orphan.jpg" in result
    # Appended after all original content
    assert result.index("orphan.jpg") > result.index("Some overview.")


def test_embed_images_mixed_placed_and_unplaced():
    """Mixed images: placed ones go inline, unplaced ones are appended."""
    content = (
        "## Section A\n\n"
        "Content of section A.\n\n"
        "## Section B\n\n"
        "Content of section B.\n"
    )
    images = [
        {
            "section": "Section A",
            "description": "Section A image",
            "url": "https://example.com/a.jpg",
            "author": "Dave",
            "author_url": "https://example.com/dave",
            "source": "Unsplash",
        },
        {
            "description": "Unplaced image",
            "url": "https://example.com/unplaced.jpg",
            "author": "Eve",
            "author_url": "",
            "source": "Unsplash",
        },
    ]
    result = PublisherAgent._embed_images_in_content(content, images)
    assert "https://example.com/a.jpg" in result
    assert "https://example.com/unplaced.jpg" in result
    # Placed image before Section B, unplaced at end
    assert result.index("a.jpg") < result.index("## Section B")
    assert result.index("unplaced.jpg") > result.index("Content of section B.")
