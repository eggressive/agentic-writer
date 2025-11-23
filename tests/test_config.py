"""Tests for configuration management."""

import pytest
from src.utils.config import Config


def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    assert config.openai_model == "gpt-4-turbo-preview"
    assert config.temperature == 0.7
    assert config.log_level == "INFO"
    assert config.max_research_sources == 5


def test_config_from_env(monkeypatch):
    """Test loading configuration from environment variables."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-3.5-turbo")
    monkeypatch.setenv("TEMPERATURE", "0.5")

    config = Config.from_env()
    assert config.openai_api_key == "test-key"
    assert config.openai_model == "gpt-3.5-turbo"
    assert config.temperature == 0.5


def test_config_validation_missing_key():
    """Test validation fails when API key is missing."""
    config = Config(openai_api_key="")

    with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
        config.validate_required()


def test_config_validation_with_key():
    """Test validation passes when API key is present."""
    config = Config(openai_api_key="test-key")
    config.validate_required()  # Should not raise


def test_unsplash_per_page_validation():
    """Test unsplash_per_page validation."""
    # Valid values
    config = Config(unsplash_per_page=1)
    assert config.unsplash_per_page == 1

    config = Config(unsplash_per_page=30)
    assert config.unsplash_per_page == 30

    # Invalid values
    with pytest.raises(ValueError, match="unsplash_per_page must be between 1 and 30"):
        Config(unsplash_per_page=0)

    with pytest.raises(ValueError, match="unsplash_per_page must be between 1 and 30"):
        Config(unsplash_per_page=31)


def test_unsplash_order_by_validation():
    """Test unsplash_order_by validation."""
    # Valid values
    config = Config(unsplash_order_by="relevant")
    assert config.unsplash_order_by == "relevant"

    config = Config(unsplash_order_by="latest")
    assert config.unsplash_order_by == "latest"

    # Invalid value
    with pytest.raises(
        ValueError, match="unsplash_order_by must be 'relevant' or 'latest'"
    ):
        Config(unsplash_order_by="invalid")


def test_unsplash_content_filter_validation():
    """Test unsplash_content_filter validation."""
    # Valid values
    config = Config(unsplash_content_filter="low")
    assert config.unsplash_content_filter == "low"

    config = Config(unsplash_content_filter="high")
    assert config.unsplash_content_filter == "high"

    # Invalid value
    with pytest.raises(
        ValueError, match="unsplash_content_filter must be 'low' or 'high'"
    ):
        Config(unsplash_content_filter="medium")


def test_unsplash_orientation_validation():
    """Test unsplash_orientation validation."""
    # Valid values
    config = Config(unsplash_orientation="landscape")
    assert config.unsplash_orientation == "landscape"

    config = Config(unsplash_orientation="portrait")
    assert config.unsplash_orientation == "portrait"

    config = Config(unsplash_orientation="squarish")
    assert config.unsplash_orientation == "squarish"

    # Invalid value
    with pytest.raises(
        ValueError,
        match="unsplash_orientation must be 'landscape', 'portrait', or 'squarish'",
    ):
        Config(unsplash_orientation="diagonal")


def test_config_from_env_invalid_integers(monkeypatch):
    """Test that invalid integer environment variables raise meaningful errors."""
    monkeypatch.setenv("UNSPLASH_PER_PAGE", "abc")

    with pytest.raises(
        ValueError, match="Invalid value for UNSPLASH_PER_PAGE: must be an integer"
    ):
        Config.from_env()

    monkeypatch.setenv("UNSPLASH_PER_PAGE", "10")
    monkeypatch.setenv("MAX_RETRIES", "xyz")

    with pytest.raises(
        ValueError, match="Invalid value for MAX_RETRIES: must be an integer"
    ):
        Config.from_env()

    monkeypatch.setenv("MAX_RETRIES", "3")
    monkeypatch.setenv("MAX_RESEARCH_SOURCES", "invalid")

    with pytest.raises(
        ValueError, match="Invalid value for MAX_RESEARCH_SOURCES: must be an integer"
    ):
        Config.from_env()
