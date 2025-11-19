"""Tests for configuration management."""

import os
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
