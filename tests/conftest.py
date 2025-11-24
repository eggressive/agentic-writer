"""Shared test fixtures for all test modules.

This module provides common pytest fixtures that can be used across all test files.

Fixtures include mock LLM (Large Language Model) instances, such as a mock ChatOpenAI,
to ensure consistent and isolated testing of agent behavior. Use these fixtures in your
tests to avoid making real API calls and to control the responses returned by LLMs.

Example:
    def test_agent_behavior(mock_llm):
        mock_llm.invoke.return_value.content = "Custom response"
        # test code using mock_llm
"""

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_llm():
    """Create a mock LLM for testing.

    Returns a mock ChatOpenAI instance with a default response.
    Tests can override the return value by setting mock_llm.invoke.return_value.
    """
    mock = Mock()
    mock_response = Mock()
    mock_response.content = "Test response content"
    mock.invoke.return_value = mock_response
    return mock
