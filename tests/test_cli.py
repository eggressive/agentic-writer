"""Tests for CLI commands."""

from unittest.mock import Mock, patch

import click
import openai
import pytest
from click.testing import CliRunner

from src import __version__
from src.cli import (
    MAX_TOPIC_LENGTH,
    MIN_TOPIC_LENGTH,
    VALID_LOG_LEVELS,
    VALID_STYLES,
    cli,
    validate_create_inputs,
)
from src.utils.config import Config


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    config = Config(
        openai_api_key="test-key",
        openai_model="gpt-3.5-turbo",
        temperature=0.7,
        log_level="INFO",
    )
    return config


@pytest.fixture
def mock_orchestrator():
    """Create a mock orchestrator."""
    mock = Mock()
    mock.create_content.return_value = {
        "status": "completed",
        "topic": "Test Topic",
        "article": {
            "title": "Test Article",
            "word_count": 1000,
            "tags": ["test", "article"],
        },
        "stages": {
            "research": {"status": "completed", "sources_count": 5},
            "writing": {
                "status": "completed",
                "title": "Test Article",
                "word_count": 1000,
            },
            "images": {"status": "completed", "images_found": 2},
            "publishing": {"status": "completed"},
        },
        "publication": {
            "file": {
                "success": True,
                "platform": "file",
                "markdown_file": "/tmp/test.md",
            }
        },
    }
    mock.get_summary.return_value = "Test summary"
    return mock


def test_cli_group_exists(runner):
    """Test that the main CLI group exists and shows help."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Automated Content Creation & Management Agent" in result.output


def test_create_command_help(runner):
    """Test that the create command shows help."""
    result = runner.invoke(cli, ["create", "--help"])
    assert result.exit_code == 0
    assert "Create and publish content on a given TOPIC" in result.output
    assert "--style" in result.output
    assert "--audience" in result.output
    assert "--platform" in result.output
    assert "--output-dir" in result.output
    assert "--log-level" in result.output


@patch("src.cli.ContentCreationOrchestrator")
@patch("src.cli.Config")
@patch("src.cli.setup_logger")
def test_create_command_success(
    mock_setup_logger,
    mock_config_class,
    mock_orchestrator_class,
    runner,
    mock_orchestrator,
):
    """Test successful execution of the create command."""
    # Setup mocks
    mock_config = Mock()
    mock_config_class.from_env.return_value = mock_config
    mock_orchestrator_class.return_value = mock_orchestrator
    mock_logger = Mock()
    mock_setup_logger.return_value = mock_logger

    # Run command
    result = runner.invoke(
        cli,
        [
            "create",
            "Test Topic",
            "--style",
            "professional",
            "--audience",
            "developers",
            "--platform",
            "file",
            "--output-dir",
            "output",
        ],
    )

    # Assertions
    assert result.exit_code == 0
    assert "Content creation completed successfully" in result.output
    mock_config_class.from_env.assert_called_once()
    mock_config.validate_required.assert_called_once()
    mock_setup_logger.assert_called_once_with(level="INFO")
    mock_orchestrator_class.assert_called_once_with(mock_config)
    mock_orchestrator.create_content.assert_called_once_with(
        topic="Test Topic",
        style="professional",
        target_audience="developers",
        platforms=["file"],
        output_dir="output",
    )


@patch("src.cli.ContentCreationOrchestrator")
@patch("src.cli.Config")
@patch("src.cli.setup_logger")
def test_create_command_with_multiple_platforms(
    mock_setup_logger,
    mock_config_class,
    mock_orchestrator_class,
    runner,
    mock_orchestrator,
):
    """Test create command with multiple platforms."""
    # Setup mocks
    mock_config = Mock()
    mock_config_class.from_env.return_value = mock_config
    mock_orchestrator_class.return_value = mock_orchestrator
    mock_logger = Mock()
    mock_setup_logger.return_value = mock_logger

    # Run command with multiple platforms
    result = runner.invoke(
        cli,
        [
            "create",
            "AI Testing",
            "--platform",
            "file",
            "--platform",
            "medium",
        ],
    )

    # Assertions
    assert result.exit_code == 0
    mock_orchestrator.create_content.assert_called_once()
    call_kwargs = mock_orchestrator.create_content.call_args[1]
    assert call_kwargs["platforms"] == ["file", "medium"]


@patch("src.cli.ContentCreationOrchestrator")
@patch("src.cli.Config")
@patch("src.cli.setup_logger")
def test_create_command_default_values(
    mock_setup_logger,
    mock_config_class,
    mock_orchestrator_class,
    runner,
    mock_orchestrator,
):
    """Test create command uses default values when options are not specified."""
    # Setup mocks
    mock_config = Mock()
    mock_config_class.from_env.return_value = mock_config
    mock_orchestrator_class.return_value = mock_orchestrator
    mock_logger = Mock()
    mock_setup_logger.return_value = mock_logger

    # Run command with minimal arguments
    result = runner.invoke(cli, ["create", "Test Topic"])

    # Assertions
    assert result.exit_code == 0
    mock_orchestrator.create_content.assert_called_once()
    call_kwargs = mock_orchestrator.create_content.call_args[1]
    assert call_kwargs["topic"] == "Test Topic"
    assert call_kwargs["style"] is None
    assert call_kwargs["target_audience"] is None
    assert call_kwargs["platforms"] == ["file"]
    assert call_kwargs["output_dir"] == "output"
    mock_setup_logger.assert_called_once_with(level="INFO")


@patch("src.cli.Config")
@patch("src.cli.setup_logger")
def test_create_command_config_validation_error(
    mock_setup_logger, mock_config_class, runner
):
    """Test create command handles configuration validation errors."""
    # Setup mocks
    mock_config = Mock()
    mock_config.validate_required.side_effect = ValueError("OPENAI_API_KEY is required")
    mock_config_class.from_env.return_value = mock_config
    mock_logger = Mock()
    mock_setup_logger.return_value = mock_logger

    # Run command
    result = runner.invoke(cli, ["create", "Test Topic"])

    # Assertions
    # CLI handles the exception and prints an error message without exiting with an error code
    assert result.exit_code == 0
    assert "Configuration Error" in result.output
    assert "OPENAI_API_KEY is required" in result.output


@patch("src.cli.ContentCreationOrchestrator")
@patch("src.cli.Config")
@patch("src.cli.setup_logger")
def test_create_command_general_exception(
    mock_setup_logger, mock_config_class, mock_orchestrator_class, runner
):
    """Test create command handles general exceptions."""
    # Setup mocks
    mock_config = Mock()
    mock_config_class.from_env.return_value = mock_config
    mock_orchestrator = Mock()
    mock_orchestrator.create_content.side_effect = Exception("Test error")
    mock_orchestrator_class.return_value = mock_orchestrator
    mock_logger = Mock()
    mock_setup_logger.return_value = mock_logger

    # Run command
    result = runner.invoke(cli, ["create", "Test Topic"])

    # Assertions
    assert result.exit_code == 0
    assert "Error:" in result.output
    assert "Test error" in result.output
    mock_logger.exception.assert_called_once_with("Content creation failed")


@patch("src.cli.ContentCreationOrchestrator")
@patch("src.cli.Config")
@patch("src.cli.setup_logger")
def test_create_command_failed_status(
    mock_setup_logger, mock_config_class, mock_orchestrator_class, runner
):
    """Test create command handles failed status from orchestrator."""
    # Setup mocks
    mock_config = Mock()
    mock_config_class.from_env.return_value = mock_config
    mock_orchestrator = Mock()
    mock_orchestrator.create_content.return_value = {
        "status": "failed",
        "error": "Pipeline failed",
    }
    mock_orchestrator_class.return_value = mock_orchestrator
    mock_logger = Mock()
    mock_setup_logger.return_value = mock_logger

    # Run command
    result = runner.invoke(cli, ["create", "Test Topic"])

    # Assertions
    assert result.exit_code == 0
    assert "Content creation failed" in result.output
    assert "Pipeline failed" in result.output


def test_config_command_help(runner):
    """Test that the config command shows help."""
    result = runner.invoke(cli, ["config", "--help"])
    assert result.exit_code == 0
    assert "Display current configuration" in result.output


@patch("src.cli.Config")
def test_config_command_success(mock_config_class, runner, mock_config):
    """Test successful execution of the config command."""
    # Setup mocks
    mock_config_class.from_env.return_value = mock_config

    # Run command
    result = runner.invoke(cli, ["config"])

    # Assertions
    assert result.exit_code == 0
    assert "Current Configuration" in result.output
    assert "OpenAI Model:" in result.output
    assert mock_config.openai_model in result.output
    assert "Temperature:" in result.output
    assert str(mock_config.temperature) in result.output
    assert "Max Research Sources:" in result.output
    assert "Log Level:" in result.output
    assert "API Keys Status:" in result.output


@patch("src.cli.Config")
def test_config_command_shows_api_key_status(mock_config_class, runner):
    """Test config command shows API key status correctly."""
    # Setup mock with all API keys set
    mock_config = Config(
        openai_api_key="test-key",
        medium_access_token="medium-token",
        unsplash_access_key="unsplash-key",
    )
    mock_config_class.from_env.return_value = mock_config

    # Run command
    result = runner.invoke(cli, ["config"])

    # Assertions
    assert result.exit_code == 0
    assert "OpenAI:" in result.output
    assert "Medium:" in result.output
    assert "Unsplash:" in result.output


@patch("src.cli.Config")
def test_config_command_error_handling(mock_config_class, runner):
    """Test config command handles errors gracefully."""
    # Setup mocks
    mock_config_class.from_env.side_effect = Exception("Config error")

    # Run command
    result = runner.invoke(cli, ["config"])

    # Assertions
    assert result.exit_code == 0
    assert "Error:" in result.output
    assert "Config error" in result.output


def test_version_command_help(runner):
    """Test that the version command shows help."""
    result = runner.invoke(cli, ["version", "--help"])
    assert result.exit_code == 0
    assert "Display version information" in result.output


def test_version_command_success(runner):
    """Test successful execution of the version command."""
    result = runner.invoke(cli, ["version"])

    # Assertions
    assert result.exit_code == 0
    assert "Content Creation Agent" in result.output
    assert "version" in result.output
    assert __version__ in result.output


@patch("src.cli.ContentCreationOrchestrator")
@patch("src.cli.Config")
@patch("src.cli.setup_logger")
def test_create_command_dry_run(
    mock_setup_logger, mock_config_class, mock_orchestrator_class, runner
):
    """Test --dry-run validates config and shows plan without calling APIs."""
    mock_config = Mock()
    mock_config.openai_model = "gpt-4-turbo-preview"
    mock_config_class.from_env.return_value = mock_config
    mock_setup_logger.return_value = Mock()

    result = runner.invoke(
        cli,
        [
            "create",
            "Test Topic",
            "--style",
            "professional",
            "--audience",
            "developers",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    assert "Dry Run" in result.output
    assert "Test Topic" in result.output
    assert "professional" in result.output
    assert "developers" in result.output
    assert "no APIs called" in result.output
    mock_config.validate_required.assert_called_once()
    mock_orchestrator_class.assert_not_called()


@patch("src.cli.Config")
@patch("src.cli.setup_logger")
def test_create_command_dry_run_config_error(
    mock_setup_logger, mock_config_class, runner
):
    """Test --dry-run still fails on invalid config."""
    mock_config = Mock()
    mock_config.validate_required.side_effect = ValueError("OPENAI_API_KEY is required")
    mock_config_class.from_env.return_value = mock_config
    mock_setup_logger.return_value = Mock()

    result = runner.invoke(cli, ["create", "Test Topic", "--dry-run"])

    assert result.exit_code == 0
    assert "Configuration Error" in result.output
    assert "OPENAI_API_KEY is required" in result.output


@patch("src.cli.setup_logger")
def test_create_command_custom_log_level(mock_setup_logger, runner):
    """Test create command respects custom log level."""
    mock_logger = Mock()
    mock_setup_logger.return_value = mock_logger

    # Mock Config to prevent actual API validation
    with patch("src.cli.Config") as mock_config_class:
        mock_config = Mock()
        mock_config.validate_required.side_effect = ValueError("Test early exit")
        mock_config_class.from_env.return_value = mock_config

        runner.invoke(
            cli,
            ["create", "Test Topic", "--log-level", "DEBUG"],
        )

        # Verify logger was setup with correct level
        mock_setup_logger.assert_called_once_with(level="DEBUG")


# ---------------------------------------------------------------------------
# Input validation tests
# ---------------------------------------------------------------------------


class TestValidateCreateInputs:
    """Unit tests for the validate_create_inputs helper."""

    def test_valid_inputs_pass(self):
        """Valid topic, style, and log_level raise no error."""
        validate_create_inputs("Artificial Intelligence", "professional", "INFO")

    def test_topic_empty_raises(self):
        """Empty topic raises BadParameter."""
        with pytest.raises(click.exceptions.BadParameter, match="empty"):
            validate_create_inputs("", None, "INFO")

    def test_topic_whitespace_only_raises(self):
        """Whitespace-only topic raises BadParameter."""
        with pytest.raises(click.exceptions.BadParameter, match="empty"):
            validate_create_inputs("   ", None, "INFO")

    def test_topic_too_short_raises(self):
        """Topic shorter than MIN_TOPIC_LENGTH raises BadParameter."""
        short = "a" * (MIN_TOPIC_LENGTH - 1)
        with pytest.raises(click.exceptions.BadParameter, match="at least"):
            validate_create_inputs(short, None, "INFO")

    def test_topic_at_min_length_passes(self):
        """Topic exactly at MIN_TOPIC_LENGTH is accepted."""
        validate_create_inputs("a" * MIN_TOPIC_LENGTH, None, "INFO")

    def test_topic_too_long_raises(self):
        """Topic exceeding MAX_TOPIC_LENGTH raises BadParameter."""
        long_topic = "a" * (MAX_TOPIC_LENGTH + 1)
        with pytest.raises(click.exceptions.BadParameter, match="at most"):
            validate_create_inputs(long_topic, None, "INFO")

    def test_topic_at_max_length_passes(self):
        """Topic exactly at MAX_TOPIC_LENGTH is accepted."""
        validate_create_inputs("a" * MAX_TOPIC_LENGTH, None, "INFO")

    def test_topic_at_max_length_with_trailing_spaces_passes(self):
        """Topic at MAX_TOPIC_LENGTH with trailing whitespace is accepted (stripped check)."""
        topic_with_spaces = "a" * MAX_TOPIC_LENGTH + "   "
        validate_create_inputs(topic_with_spaces, None, "INFO")

    def test_invalid_style_raises(self):
        """Unknown style value raises BadParameter."""
        with pytest.raises(click.exceptions.BadParameter, match="Invalid style"):
            validate_create_inputs("Valid Topic", "jargon", "INFO")

    def test_style_none_is_valid(self):
        """Style=None (omitted) is always valid."""
        validate_create_inputs("Valid Topic", None, "INFO")

    def test_all_valid_styles_pass(self):
        """Every style in VALID_STYLES is accepted."""
        for style in VALID_STYLES:
            validate_create_inputs("Valid Topic", style, "INFO")

    def test_style_case_insensitive(self):
        """Style matching is case-insensitive."""
        validate_create_inputs("Valid Topic", "Professional", "INFO")
        validate_create_inputs("Valid Topic", "TECHNICAL", "INFO")

    def test_style_with_surrounding_whitespace_passes(self):
        """Style with surrounding whitespace is accepted (stripped before check)."""
        validate_create_inputs("Valid Topic", "professional ", "INFO")
        validate_create_inputs("Valid Topic", " Professional ", "INFO")

    def test_invalid_log_level_raises(self):
        """Unknown log level raises BadParameter."""
        with pytest.raises(click.exceptions.BadParameter, match="Invalid log level"):
            validate_create_inputs("Valid Topic", None, "VERBOSE")

    def test_all_valid_log_levels_pass(self):
        """Every level in VALID_LOG_LEVELS is accepted."""
        for level in VALID_LOG_LEVELS:
            validate_create_inputs("Valid Topic", None, level)

    def test_log_level_case_insensitive(self):
        """Log-level matching is case-insensitive."""
        validate_create_inputs("Valid Topic", None, "debug")
        validate_create_inputs("Valid Topic", None, "Warning")


class TestCreateCommandValidationIntegration:
    """Integration tests: validation errors surface correctly in the CLI."""

    def test_empty_topic_exits_with_error(self, runner):
        """Empty topic string causes exit code 2 (UsageError)."""
        result = runner.invoke(cli, ["create", "  "])
        assert result.exit_code == 2
        assert "Error" in result.output

    def test_too_long_topic_exits_with_error(self, runner):
        """Oversized topic causes exit code 2."""
        long_topic = "a" * (MAX_TOPIC_LENGTH + 1)
        result = runner.invoke(cli, ["create", long_topic])
        assert result.exit_code == 2
        assert "at most" in result.output

    def test_invalid_style_exits_with_error(self, runner):
        """Unknown style causes exit code 2."""
        result = runner.invoke(cli, ["create", "Valid Topic", "--style", "jargon"])
        assert result.exit_code == 2
        assert "Invalid style" in result.output

    def test_invalid_log_level_exits_with_error(self, runner):
        """Unknown log level causes exit code 2."""
        result = runner.invoke(cli, ["create", "Valid Topic", "--log-level", "VERBOSE"])
        assert result.exit_code == 2
        assert "Invalid log level" in result.output

    @patch("src.cli.ContentCreationOrchestrator")
    @patch("src.cli.Config")
    @patch("src.cli.setup_logger")
    def test_valid_inputs_proceed_normally(
        self,
        mock_setup_logger,
        mock_config_class,
        mock_orchestrator_class,
        runner,
        mock_orchestrator,
    ):
        """Valid inputs pass validation and invoke the pipeline."""
        mock_config = Mock()
        mock_config_class.from_env.return_value = mock_config
        mock_orchestrator_class.return_value = mock_orchestrator
        mock_setup_logger.return_value = Mock()

        result = runner.invoke(
            cli,
            [
                "create",
                "Artificial Intelligence in Healthcare",
                "--style",
                "professional",
                "--log-level",
                "DEBUG",
            ],
        )

        assert result.exit_code == 0
        mock_orchestrator.create_content.assert_called_once()

    @patch("src.cli.ContentCreationOrchestrator")
    @patch("src.cli.Config")
    @patch("src.cli.setup_logger")
    def test_topic_is_stripped_before_pipeline(
        self,
        mock_setup_logger,
        mock_config_class,
        mock_orchestrator_class,
        runner,
        mock_orchestrator,
    ):
        """Topic with surrounding whitespace is stripped before being passed downstream."""
        mock_config = Mock()
        mock_config_class.from_env.return_value = mock_config
        mock_orchestrator_class.return_value = mock_orchestrator
        mock_setup_logger.return_value = Mock()

        result = runner.invoke(cli, ["create", "  AI in Healthcare  "])

        assert result.exit_code == 0
        call_kwargs = mock_orchestrator.create_content.call_args
        assert call_kwargs.kwargs["topic"] == "AI in Healthcare"

    @patch("src.cli.ContentCreationOrchestrator")
    @patch("src.cli.Config")
    @patch("src.cli.setup_logger")
    def test_style_is_normalized_to_lowercase_before_pipeline(
        self,
        mock_setup_logger,
        mock_config_class,
        mock_orchestrator_class,
        runner,
        mock_orchestrator,
    ):
        """Style with mixed case is lowercased before being passed downstream."""
        mock_config = Mock()
        mock_config_class.from_env.return_value = mock_config
        mock_orchestrator_class.return_value = mock_orchestrator
        mock_setup_logger.return_value = Mock()

        result = runner.invoke(
            cli, ["create", "AI in Healthcare", "--style", "Professional"]
        )

        assert result.exit_code == 0
        call_kwargs = mock_orchestrator.create_content.call_args
        assert call_kwargs.kwargs["style"] == "professional"


# --- health command tests ---


def test_health_command_help(runner):
    """Test that the health command shows help."""
    result = runner.invoke(cli, ["health", "--help"])
    assert result.exit_code == 0
    assert "Verify that configured API keys are working" in result.output


@patch("src.cli.requests.get")
@patch("src.cli.openai.OpenAI")
@patch("src.cli.Config")
def test_health_command_all_configured_ok(
    mock_config_class, mock_openai_class, mock_requests_get, runner
):
    """Happy path: all services configured and responding correctly."""
    mock_config = Config(
        openai_api_key="sk-test",
        unsplash_access_key="unsplash-key",
        medium_access_token="medium-token",
    )
    mock_config_class.from_env.return_value = mock_config

    mock_client = Mock()
    mock_openai_class.return_value = mock_client

    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_requests_get.return_value = mock_resp

    result = runner.invoke(cli, ["health"])

    assert result.exit_code == 0
    assert "✓ OK" in result.output
    assert "All configured services are healthy" in result.output
    mock_client.models.list.assert_called_once()
    assert mock_requests_get.call_count == 2


@patch("src.cli.openai.OpenAI")
@patch("src.cli.Config")
def test_health_command_optional_services_not_configured(
    mock_config_class, mock_openai_class, runner
):
    """Optional services not configured show as skipped, not errors."""
    mock_config = Config(openai_api_key="sk-test")
    mock_config_class.from_env.return_value = mock_config

    mock_client = Mock()
    mock_openai_class.return_value = mock_client

    result = runner.invoke(cli, ["health"])

    assert result.exit_code == 0
    assert "All configured services are healthy" in result.output
    assert "Not configured (optional)" in result.output


@patch("src.cli.Config")
def test_health_command_openai_key_missing(mock_config_class, runner):
    """OpenAI key missing causes exit code 1."""
    mock_config = Config(openai_api_key="")
    mock_config_class.from_env.return_value = mock_config

    result = runner.invoke(cli, ["health"])

    assert result.exit_code == 1
    assert "API key not set" in result.output
    assert "One or more health checks failed" in result.output


@patch("src.cli.openai.OpenAI")
@patch("src.cli.Config")
def test_health_command_openai_auth_error(mock_config_class, mock_openai_class, runner):
    """Invalid OpenAI key causes exit code 1."""
    mock_config = Config(openai_api_key="sk-invalid")
    mock_config_class.from_env.return_value = mock_config

    mock_client = Mock()
    mock_client.models.list.side_effect = openai.AuthenticationError(
        message="Invalid API key",
        response=Mock(status_code=401, headers={}),
        body={"error": {"message": "Invalid API key"}},
    )
    mock_openai_class.return_value = mock_client

    result = runner.invoke(cli, ["health"])

    assert result.exit_code == 1
    assert "Invalid API key" in result.output
    assert "One or more health checks failed" in result.output


@patch("src.cli.requests.get")
@patch("src.cli.openai.OpenAI")
@patch("src.cli.Config")
def test_health_command_unsplash_auth_error(
    mock_config_class, mock_openai_class, mock_requests_get, runner
):
    """Invalid Unsplash key causes exit code 1."""
    mock_config = Config(openai_api_key="sk-test", unsplash_access_key="bad-key")
    mock_config_class.from_env.return_value = mock_config

    mock_openai_class.return_value = Mock()

    mock_resp = Mock()
    mock_resp.status_code = 401
    mock_requests_get.return_value = mock_resp

    result = runner.invoke(cli, ["health"])

    assert result.exit_code == 1
    assert "Invalid API key (HTTP 401)" in result.output
    assert "One or more health checks failed" in result.output


@patch("src.cli.requests.get")
@patch("src.cli.openai.OpenAI")
@patch("src.cli.Config")
def test_health_command_medium_auth_error(
    mock_config_class, mock_openai_class, mock_requests_get, runner
):
    """Invalid Medium token causes exit code 1."""
    mock_config = Config(openai_api_key="sk-test", medium_access_token="bad-token")
    mock_config_class.from_env.return_value = mock_config

    mock_openai_class.return_value = Mock()

    mock_resp = Mock()
    mock_resp.status_code = 401
    mock_requests_get.return_value = mock_resp

    result = runner.invoke(cli, ["health"])

    assert result.exit_code == 1
    assert "Invalid token (HTTP 401)" in result.output
    assert "One or more health checks failed" in result.output


@patch("src.cli.requests.get")
@patch("src.cli.openai.OpenAI")
@patch("src.cli.Config")
def test_health_command_network_error(
    mock_config_class, mock_openai_class, mock_requests_get, runner
):
    """Network error on an optional service causes exit code 1."""
    mock_config = Config(openai_api_key="sk-test", unsplash_access_key="key")
    mock_config_class.from_env.return_value = mock_config

    mock_openai_class.return_value = Mock()
    mock_requests_get.side_effect = Exception("Connection refused")

    result = runner.invoke(cli, ["health"])

    assert result.exit_code == 1
    assert "Connection refused" in result.output
