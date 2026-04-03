"""Tests for logging utilities."""

import json
import logging

import pytest

from src.utils.logger import _JsonFormatter, setup_logger


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


def test_setup_logger_json_format():
    """Test logger setup with json format uses _JsonFormatter."""
    logger = setup_logger(name="json_test", log_format="json")
    assert len(logger.handlers) > 0
    assert isinstance(logger.handlers[0].formatter, _JsonFormatter)


def test_json_formatter_output():
    """Test that _JsonFormatter produces valid JSON with required keys."""
    formatter = _JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="hello world",
        args=(),
        exc_info=None,
    )
    output = formatter.format(record)
    parsed = json.loads(output)
    assert parsed["level"] == "INFO"
    assert parsed["logger"] == "test"
    assert parsed["message"] == "hello world"
    assert "timestamp" in parsed


def test_json_formatter_with_exception():
    """Test that _JsonFormatter includes exception info when present."""
    formatter = _JsonFormatter()
    try:
        raise ValueError("boom")
    except ValueError:
        import sys

        exc_info = sys.exc_info()

    record = logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname="",
        lineno=0,
        msg="something failed",
        args=(),
        exc_info=exc_info,
    )
    output = formatter.format(record)
    parsed = json.loads(output)
    assert "exception" in parsed
    assert "ValueError" in parsed["exception"]


def test_setup_logger_text_format_default():
    """Test that text format (default) does NOT use _JsonFormatter."""
    logger = setup_logger(name="text_test", log_format="text")
    assert not isinstance(logger.handlers[0].formatter, _JsonFormatter)


@pytest.mark.parametrize("bad_format", ["xml", "csv", "yaml"])
def test_setup_logger_invalid_format_falls_back_to_text(bad_format):
    """Unknown log_format values fall back to text (no crash)."""
    # The CLI enforces choices; calling setup_logger directly with unknown value
    # should not raise — it just uses text formatter (the else branch).
    logger = setup_logger(name=f"fallback_{bad_format}", log_format=bad_format)
    assert not isinstance(logger.handlers[0].formatter, _JsonFormatter)
