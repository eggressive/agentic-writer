"""Shared test fixtures for all test modules."""

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
