"""Tests for logging utilities."""

import json
import logging

from src.utils.logger import JsonFormatter, setup_logger


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


# ---------------------------------------------------------------------------
# JsonFormatter tests
# ---------------------------------------------------------------------------


def _make_record(msg="hello", level=logging.INFO):
    record = logging.LogRecord(
        name="test",
        level=level,
        pathname="",
        lineno=0,
        msg=msg,
        args=(),
        exc_info=None,
    )
    return record


def test_json_formatter_returns_valid_json():
    """JsonFormatter output can be parsed as JSON."""
    fmt = JsonFormatter()
    output = fmt.format(_make_record("test message"))
    data = json.loads(output)
    assert isinstance(data, dict)


def test_json_formatter_contains_required_fields():
    """JsonFormatter output contains timestamp, level, logger, message."""
    fmt = JsonFormatter()
    data = json.loads(fmt.format(_make_record("hello world", logging.WARNING)))
    assert data["message"] == "hello world"
    assert data["level"] == "WARNING"
    assert data["logger"] == "test"
    assert "timestamp" in data


def test_json_formatter_timestamp_is_iso8601_utc():
    """Timestamp is a UTC ISO-8601 string (ends with +00:00)."""
    fmt = JsonFormatter()
    data = json.loads(fmt.format(_make_record("ts check")))
    ts = data["timestamp"]
    assert "T" in ts
    assert ts.endswith("+00:00")


def test_json_formatter_exc_info_included():
    """JsonFormatter includes exc_info when an exception is logged."""
    fmt = JsonFormatter()
    try:
        raise ValueError("boom")
    except ValueError:
        import sys

        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="error occurred",
            args=(),
            exc_info=sys.exc_info(),
        )
    data = json.loads(fmt.format(record))
    assert "exc_info" in data
    assert "ValueError" in data["exc_info"]


# ---------------------------------------------------------------------------
# setup_logger log_format tests
# ---------------------------------------------------------------------------


def test_setup_logger_json_format_uses_json_formatter():
    """setup_logger with log_format='json' attaches a JsonFormatter."""
    logger = setup_logger(name="json_test", log_format="json")
    assert len(logger.handlers) > 0
    assert isinstance(logger.handlers[0].formatter, JsonFormatter)


def test_setup_logger_text_format_uses_standard_formatter():
    """setup_logger with log_format='text' uses a plain Formatter."""
    logger = setup_logger(name="text_test", log_format="text")
    assert len(logger.handlers) > 0
    assert not isinstance(logger.handlers[0].formatter, JsonFormatter)


def test_setup_logger_json_format_produces_valid_json_output(capsys):
    """Logger configured with json format emits parseable JSON lines."""
    logger = setup_logger(name="json_output_test", log_format="json")
    logger.info("structured message")
    captured = capsys.readouterr()
    data = json.loads(captured.out.strip())
    assert data["message"] == "structured message"
    assert data["level"] == "INFO"


def test_setup_logger_normalizes_log_format_case():
    """setup_logger accepts uppercase/mixed-case log_format values."""
    logger = setup_logger(name="case_test_json", log_format="JSON")
    assert isinstance(logger.handlers[0].formatter, JsonFormatter)

    logger2 = setup_logger(name="case_test_text", log_format="TEXT")
    assert not isinstance(logger2.handlers[0].formatter, JsonFormatter)


def test_setup_logger_invalid_log_format_raises():
    """setup_logger raises ValueError for unsupported log_format values."""
    import pytest

    with pytest.raises(ValueError, match="Unsupported log_format"):
        setup_logger(name="bad_format_test", log_format="xml")
