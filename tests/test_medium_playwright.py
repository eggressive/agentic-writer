"""Tests for MediumPlaywrightPublisher and the medium_playwright platform."""

from unittest.mock import MagicMock, patch

import pytest

from src.agents.medium_playwright import (
    _INSTALL_HINT,
    MediumPlaywrightPublisher,
)
from src.agents.publisher import PublisherAgent


@pytest.fixture
def publisher():
    """MediumPlaywrightPublisher with test credentials."""
    return MediumPlaywrightPublisher(email="test@example.com", password="s3cr3t")


@pytest.fixture
def sample_article():
    """Minimal article data fixture."""
    return {
        "title": "My Test Article",
        "content": "## Intro\n\nHello world.",
        "tags": ["testing", "automation"],
        "meta_description": "A test article.",
    }


# ---------------------------------------------------------------------------
# MediumPlaywrightPublisher unit tests
# ---------------------------------------------------------------------------


def test_publish_when_playwright_not_installed(publisher, sample_article):
    """publish() returns an error dict when playwright is not available."""
    with patch("src.agents.medium_playwright.PLAYWRIGHT_AVAILABLE", False):
        result = publisher.publish(sample_article)

    assert result["success"] is False
    assert result["platform"] == "medium"
    assert "playwright" in result["error"].lower()
    assert _INSTALL_HINT in result["error"]


def _make_mock_playwright(published_url: str = "https://medium.com/@user/test-abc"):
    """Build a mock playwright context manager returning a page at published_url."""
    mock_page = MagicMock()
    mock_page.url = published_url

    # Differentiate locator calls: password input present, tag input absent.
    def _locator_side_effect(selector):
        loc = MagicMock()
        loc.count.return_value = 1 if "password" in selector else 0
        return loc

    mock_page.locator.side_effect = _locator_side_effect

    mock_context = MagicMock()
    mock_context.new_page.return_value = mock_page

    mock_browser = MagicMock()
    mock_browser.new_context.return_value = mock_context

    mock_pw = MagicMock()
    mock_pw.chromium.launch.return_value = mock_browser
    mock_pw.__enter__ = MagicMock(return_value=mock_pw)
    mock_pw.__exit__ = MagicMock(return_value=False)

    return mock_pw, mock_page


def test_publish_happy_path(publisher, sample_article):
    """publish() returns success with URL on a fully mocked Playwright session."""
    expected_url = "https://medium.com/@user/my-test-article-abc123"
    mock_pw, mock_page = _make_mock_playwright(published_url=expected_url)

    with patch("src.agents.medium_playwright.PLAYWRIGHT_AVAILABLE", True), patch(
        "src.agents.medium_playwright.sync_playwright", return_value=mock_pw
    ):
        result = publisher.publish(sample_article)

    assert result["success"] is True
    assert result["platform"] == "medium"
    assert result["url"] == expected_url


def test_publish_uses_title_and_content(publisher, sample_article):
    """publish() passes title and content to the Playwright page interactions."""
    mock_pw, mock_page = _make_mock_playwright()

    with patch("src.agents.medium_playwright.PLAYWRIGHT_AVAILABLE", True), patch(
        "src.agents.medium_playwright.sync_playwright", return_value=mock_pw
    ):
        publisher.publish(sample_article)

    # keyboard.type should have been called with the article content
    mock_page.keyboard.type.assert_called_once_with(sample_article["content"])


def test_publish_exception_returns_failure(publisher, sample_article):
    """publish() returns failure dict when an exception is raised inside Playwright."""
    mock_pw = MagicMock()
    mock_pw.__enter__ = MagicMock(return_value=mock_pw)
    mock_pw.__exit__ = MagicMock(return_value=False)
    mock_pw.chromium.launch.side_effect = RuntimeError("browser launch failed")

    with patch("src.agents.medium_playwright.PLAYWRIGHT_AVAILABLE", True), patch(
        "src.agents.medium_playwright.sync_playwright", return_value=mock_pw
    ):
        result = publisher.publish(sample_article)

    assert result["success"] is False
    assert result["platform"] == "medium"
    assert "browser launch failed" in result["error"]


def test_login_magic_link_raises(publisher):
    """_login() raises when Medium shows a magic-link prompt instead of password."""
    mock_page = MagicMock()
    # Simulate no password field visible
    mock_page.locator.return_value.count.return_value = 0

    with pytest.raises(RuntimeError, match="magic link"):
        publisher._login(mock_page)


def test_create_story_with_tags(publisher, sample_article):
    """_create_story() fills tag input when tags are present and input exists."""
    mock_page = MagicMock()
    mock_page.url = "https://medium.com/@user/story-abc"
    # Simulate tag input being present
    mock_tag_locator = MagicMock()
    mock_tag_locator.count.return_value = 1
    mock_page.locator.return_value = mock_tag_locator

    publisher._create_story(mock_page, "Title", "Content", ["tag1", "tag2"])

    mock_tag_locator.fill.assert_called_once_with("tag1, tag2")


def test_create_story_truncates_tags_to_five(publisher):
    """_create_story() passes at most 5 tags to Medium."""
    mock_page = MagicMock()
    mock_page.url = "https://medium.com/@user/story-abc"
    mock_tag_locator = MagicMock()
    mock_tag_locator.count.return_value = 1
    mock_page.locator.return_value = mock_tag_locator

    many_tags = ["t1", "t2", "t3", "t4", "t5", "t6", "t7"]
    publisher._create_story(mock_page, "Title", "Content", many_tags)

    filled_value = mock_tag_locator.fill.call_args[0][0]
    assert filled_value.count(",") == 4  # 5 tags → 4 commas


def test_create_story_no_tags(publisher):
    """_create_story() skips tag input when tags list is empty."""
    mock_page = MagicMock()
    mock_page.url = "https://medium.com/@user/story-abc"

    publisher._create_story(mock_page, "Title", "Content", [])

    # locator should not have been called for a tag fill
    mock_page.locator.return_value.fill.assert_not_called()


# ---------------------------------------------------------------------------
# PublisherAgent integration tests
# ---------------------------------------------------------------------------


def test_publisher_agent_medium_playwright_no_credentials(sample_article):
    """PublisherAgent returns error when medium_email/password are absent."""
    agent = PublisherAgent()
    result = agent.publish_to_medium_playwright(sample_article)

    assert result["success"] is False
    assert result["platform"] == "medium"
    assert "MEDIUM_EMAIL" in result["error"]


def test_publisher_agent_medium_playwright_with_credentials(sample_article):
    """PublisherAgent delegates to MediumPlaywrightPublisher when credentials set."""
    agent = PublisherAgent(
        medium_email="user@example.com", medium_password="password123"
    )
    expected_url = "https://medium.com/@user/article-xyz"
    mock_pw, mock_page = _make_mock_playwright(published_url=expected_url)

    with patch("src.agents.medium_playwright.PLAYWRIGHT_AVAILABLE", True), patch(
        "src.agents.medium_playwright.sync_playwright", return_value=mock_pw
    ):
        result = agent.publish_to_medium_playwright(sample_article)

    assert result["success"] is True
    assert result["url"] == expected_url


def test_publisher_agent_dispatch_medium_playwright(sample_article):
    """PublisherAgent.publish() routes 'medium_playwright' to the right method."""
    agent = PublisherAgent(
        medium_email="user@example.com", medium_password="password123"
    )
    mock_result = {"success": True, "platform": "medium", "url": "https://medium.com/x"}

    with patch.object(agent, "publish_to_medium_playwright", return_value=mock_result):
        results = agent.publish(sample_article, platforms=["medium_playwright"])

    assert "medium_playwright" in results
    assert results["medium_playwright"]["success"] is True
