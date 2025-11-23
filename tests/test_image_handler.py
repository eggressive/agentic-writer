"""Tests for the ImageAgent with Unsplash API improvements."""

import pytest
from unittest.mock import Mock, patch
from src.agents.image_handler import ImageAgent


@pytest.fixture
def mock_llm():
    """Create a mock LLM."""
    mock = Mock()
    mock_response = Mock()
    mock_response.content = "technology\nartificial intelligence\nfuture"
    mock.invoke.return_value = mock_response
    return mock


@pytest.fixture
def image_agent_with_key(mock_llm):
    """Create an ImageAgent with Unsplash key."""
    return ImageAgent(
        llm=mock_llm,
        unsplash_key="test_key",
        per_page=10,
        order_by="relevant",
        content_filter="high",
        orientation="landscape",
    )


@pytest.fixture
def image_agent_without_key(mock_llm):
    """Create an ImageAgent without Unsplash key."""
    return ImageAgent(llm=mock_llm, unsplash_key=None)


@pytest.fixture
def mock_unsplash_response():
    """Create a mock Unsplash API response."""
    return {
        "results": [
            {
                "id": "photo1",
                "urls": {
                    "raw": "https://images.unsplash.com/photo1?raw",
                    "full": "https://images.unsplash.com/photo1?full",
                    "regular": "https://images.unsplash.com/photo1?regular",
                    "thumb": "https://images.unsplash.com/photo1?thumb",
                },
                "links": {
                    "html": "https://unsplash.com/photos/photo1",
                    "download": "https://unsplash.com/photos/photo1/download",
                    "download_location": "https://api.unsplash.com/photos/photo1/download",
                },
                "description": "A test image",
                "alt_description": "Test alt description",
                "user": {
                    "name": "Test Photographer",
                    "links": {"html": "https://unsplash.com/@test"},
                },
                "width": 1920,
                "height": 1080,
                "color": "#0000ff",
                "likes": 100,
                "tags": [{"title": "technology"}, {"title": "innovation"}],
            },
            {
                "id": "photo2",
                "urls": {
                    "raw": "https://images.unsplash.com/photo2?raw",
                    "full": "https://images.unsplash.com/photo2?full",
                    "regular": "https://images.unsplash.com/photo2?regular",
                    "thumb": "https://images.unsplash.com/photo2?thumb",
                },
                "links": {
                    "html": "https://unsplash.com/photos/photo2",
                    "download": "https://unsplash.com/photos/photo2/download",
                    "download_location": "https://api.unsplash.com/photos/photo2/download",
                },
                "description": None,
                "alt_description": "Another test image",
                "user": {
                    "name": "Another Photographer",
                    "links": {"html": "https://unsplash.com/@another"},
                },
                "width": 1920,
                "height": 1080,
                "color": "#ff0000",
                "likes": 50,
                "tags": [{"title": "tech"}],
            },
        ]
    }


def test_image_agent_initialization_with_defaults(mock_llm):
    """Test ImageAgent initializes with default parameters."""
    agent = ImageAgent(llm=mock_llm, unsplash_key="test_key")

    assert agent.llm == mock_llm
    assert agent.unsplash_key == "test_key"
    assert agent.per_page == 10
    assert agent.order_by == "relevant"
    assert agent.content_filter == "high"
    assert agent.orientation == "landscape"


def test_image_agent_initialization_with_custom_params(mock_llm):
    """Test ImageAgent initializes with custom parameters."""
    agent = ImageAgent(
        llm=mock_llm,
        unsplash_key="test_key",
        per_page=20,
        order_by="latest",
        content_filter="low",
        orientation="portrait",
    )

    assert agent.per_page == 20
    assert agent.order_by == "latest"
    assert agent.content_filter == "low"
    assert agent.orientation == "portrait"


@patch("src.agents.image_handler.requests.get")
def test_search_unsplash_with_all_params(
    mock_get, image_agent_with_key, mock_unsplash_response
):
    """Test search_unsplash with all parameters."""
    mock_response = Mock()
    mock_response.json.return_value = mock_unsplash_response
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    results = image_agent_with_key.search_unsplash(
        query="technology",
        per_page=15,
        order_by="latest",
        content_filter="high",
        color="blue",
        orientation="portrait",
    )

    # Verify API was called with correct parameters
    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert call_args[1]["params"]["query"] == "technology"
    assert call_args[1]["params"]["per_page"] == 15
    assert call_args[1]["params"]["order_by"] == "latest"
    assert call_args[1]["params"]["content_filter"] == "high"
    assert call_args[1]["params"]["color"] == "blue"
    assert call_args[1]["params"]["orientation"] == "portrait"

    # Verify results contain expected fields
    assert len(results) == 2
    assert results[0]["id"] == "photo1"
    assert results[0]["color"] == "#0000ff"
    assert results[0]["likes"] == 100
    assert results[0]["tags"] == ["technology", "innovation"]
    assert results[0]["photo_link"] == "https://unsplash.com/photos/photo1"
    assert (
        results[0]["download_location"]
        == "https://api.unsplash.com/photos/photo1/download"
    )
    assert results[0]["full_url"] == "https://images.unsplash.com/photo1?full"


@patch("src.agents.image_handler.requests.get")
def test_search_unsplash_without_color(
    mock_get, image_agent_with_key, mock_unsplash_response
):
    """Test search_unsplash without color parameter."""
    mock_response = Mock()
    mock_response.json.return_value = mock_unsplash_response
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    image_agent_with_key.search_unsplash(query="test")

    # Verify color is not in params when not specified
    call_args = mock_get.call_args
    assert "color" not in call_args[1]["params"]


@patch("src.agents.image_handler.requests.get")
def test_search_unsplash_respects_max_per_page(
    mock_get, image_agent_with_key, mock_unsplash_response
):
    """Test search_unsplash enforces max per_page of 30."""
    mock_response = Mock()
    mock_response.json.return_value = mock_unsplash_response
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    image_agent_with_key.search_unsplash(query="test", per_page=50)

    # Verify per_page is capped at 30
    call_args = mock_get.call_args
    assert call_args[1]["params"]["per_page"] == 30


def test_search_unsplash_without_api_key(image_agent_without_key):
    """Test search_unsplash returns empty list without API key."""
    results = image_agent_without_key.search_unsplash(query="test")

    assert results == []


@patch("src.agents.image_handler.requests.get")
def test_search_unsplash_handles_http_error(mock_get, image_agent_with_key):
    """Test search_unsplash handles HTTP errors gracefully."""
    import requests

    mock_get.side_effect = requests.exceptions.HTTPError("API Error")

    results = image_agent_with_key.search_unsplash(query="test")

    assert results == []


@patch("src.agents.image_handler.requests.get")
def test_search_unsplash_handles_general_exception(mock_get, image_agent_with_key):
    """Test search_unsplash handles general exceptions gracefully."""
    mock_get.side_effect = Exception("Network Error")

    results = image_agent_with_key.search_unsplash(query="test")

    assert results == []


@patch("src.agents.image_handler.requests.get")
def test_track_download_success(mock_get, image_agent_with_key):
    """Test track_download successfully tracks download."""
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = image_agent_with_key.track_download(
        "https://api.unsplash.com/photos/photo1/download"
    )

    assert result is True
    mock_get.assert_called_once()


@patch("src.agents.image_handler.requests.get")
def test_track_download_failure(mock_get, image_agent_with_key):
    """Test track_download handles failures gracefully."""
    mock_get.side_effect = Exception("Network Error")

    result = image_agent_with_key.track_download(
        "https://api.unsplash.com/photos/photo1/download"
    )

    assert result is False


def test_track_download_without_api_key(image_agent_without_key):
    """Test track_download returns False without API key."""
    result = image_agent_without_key.track_download("https://test.com/download")

    assert result is False


@patch("src.agents.image_handler.ImageAgent.track_download")
@patch("src.agents.image_handler.ImageAgent.search_unsplash")
def test_find_images_tracks_downloads(
    mock_search, mock_track, image_agent_with_key, mock_llm
):
    """Test find_images tracks downloads for selected images."""
    # Mock search results
    mock_search.return_value = [
        {
            "id": "photo1",
            "url": "https://test.com/photo1",
            "download_location": "https://api.unsplash.com/photos/photo1/download",
            "author": "Photographer 1",
        },
        {
            "id": "photo2",
            "url": "https://test.com/photo2",
            "download_location": "https://api.unsplash.com/photos/photo2/download",
            "author": "Photographer 2",
        },
    ]
    mock_track.return_value = True

    article_data = {"content": "Test article about technology"}
    image_agent_with_key.find_images("Technology", article_data)

    # Verify downloads were tracked
    assert mock_track.call_count >= 1
    # Verify at least one download location was tracked
    tracked_urls = [call[0][0] for call in mock_track.call_args_list]
    assert any("download" in url for url in tracked_urls)


@patch("src.agents.image_handler.ImageAgent.search_unsplash")
def test_find_images_uses_instance_params(mock_search, image_agent_with_key, mock_llm):
    """Test find_images uses instance configuration parameters."""
    mock_search.return_value = []

    article_data = {"content": "Test article"}
    image_agent_with_key.find_images("Test Topic", article_data)

    # Verify search was called with instance parameters
    assert mock_search.call_count > 0
    call_args = mock_search.call_args
    assert call_args[1]["per_page"] == image_agent_with_key.per_page
    assert call_args[1]["order_by"] == image_agent_with_key.order_by
    assert call_args[1]["content_filter"] == image_agent_with_key.content_filter
    assert call_args[1]["orientation"] == image_agent_with_key.orientation


def test_generate_image_queries(image_agent_with_key):
    """Test generate_image_queries creates appropriate queries."""
    topic = "Artificial Intelligence"
    content = "Article about AI and machine learning applications"

    queries = image_agent_with_key.generate_image_queries(topic, content)

    assert isinstance(queries, list)
    assert len(queries) <= 5
    assert all(isinstance(q, str) for q in queries)


def test_select_best_images_diversity(image_agent_with_key):
    """Test select_best_images prefers diversity of authors."""
    available_images = [
        {"id": "1", "author": "Photographer A", "url": "url1"},
        {"id": "2", "author": "Photographer A", "url": "url2"},
        {"id": "3", "author": "Photographer B", "url": "url3"},
        {"id": "4", "author": "Photographer C", "url": "url4"},
    ]

    selected = image_agent_with_key.select_best_images(
        "Test", {"content": "test"}, available_images
    )

    # Should select diverse authors first
    assert len(selected) <= 3
    authors = [img["author"] for img in selected]
    # Check that we prefer different authors
    assert len(set(authors)) >= min(len(selected), 3)


def test_select_best_images_empty_list(image_agent_with_key):
    """Test select_best_images handles empty list."""
    selected = image_agent_with_key.select_best_images("Test", {"content": "test"}, [])

    assert selected == []


def test_select_best_images_without_api_key(image_agent_without_key):
    """Test select_best_images returns empty list without API key."""
    available_images = [
        {"id": "1", "author": "Photographer A", "url": "url1"},
    ]

    selected = image_agent_without_key.select_best_images(
        "Test", {"content": "test"}, available_images
    )

    assert selected == []
