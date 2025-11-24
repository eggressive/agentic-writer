"""Tests for logging utilities."""

import logging

from src.utils.logger import setup_logger


def test_setup_logger_default():
    """Test logger setup with defaults."""
    logger = setup_logger()
    assert logger.name == "content_agent"
    assert logger.level == logging.INFO


def test_setup_logger_custom_level():
    """Test logger setup with custom level."""
    logger = setup_logger(name="test", level="DEBUG")
    assert logger.name == "test"
    assert logger.level == logging.DEBUG


def test_setup_logger_custom_format():
    """Test logger setup with custom format."""
    custom_format = "%(levelname)s - %(message)s"
    logger = setup_logger(format_string=custom_format)
    assert len(logger.handlers) > 0
