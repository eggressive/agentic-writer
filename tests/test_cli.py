"""Tests for CLI commands."""

import pytest
from unittest.mock import Mock, patch
from click.testing import CliRunner
from src.cli import cli
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
    # The version should be displayed (currently 0.1.0)
    assert "0.1.0" in result.output


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
