"""Tests for the ResearchAgent."""

import json
import pytest
from unittest.mock import Mock, patch
from src.agents.researcher import ResearchAgent


@pytest.fixture
def research_agent(mock_llm):
    """Create a ResearchAgent instance."""
    return ResearchAgent(llm=mock_llm, max_sources=5)


@patch("src.agents.researcher.DDGS")
def test_search_web_exception_handling(mock_ddgs, research_agent):
    """Test search_web handles exceptions gracefully."""
    # Mock DDGS to raise an exception
    mock_ddgs.return_value.__enter__.side_effect = Exception("Network error")

    # Should return empty list on exception
    results = research_agent.search_web("test query")

    assert results == []


@patch("src.agents.researcher.DDGS")
def test_research_with_empty_search_results(mock_ddgs, research_agent, mock_llm):
    """Test research handles empty search results."""
    # Mock empty search results
    mock_search = Mock()
    mock_search.text.return_value = []
    mock_ddgs.return_value.__enter__.return_value = mock_search

    # analyze_topic method returns a plain string
    mock_llm.invoke.return_value.content = "Test analysis"

    # Conduct research
    result = research_agent.research("test topic")

    # Should have fallback research brief with empty data
    assert "research_brief" in result
    assert result["research_brief"]["key_statistics"] == []
    assert result["research_brief"]["expert_quotes"] == []
    assert result["research_brief"]["case_studies"] == []
    assert result["research_brief"]["key_definitions"] == {}
    assert result["research_brief"]["counter_arguments"] == []
    assert result["search_results"] == []
    assert "analysis" in result


@patch("src.agents.researcher.DDGS")
def test_research_with_successful_search(mock_ddgs, research_agent, mock_llm):
    """Test research with successful search results."""
    # Mock successful search results
    mock_search = Mock()
    mock_search.text.return_value = [
        {"title": "Article 1", "body": "Content 1", "href": "https://test1.com"},
        {"title": "Article 2", "body": "Content 2", "href": "https://test2.com"},
    ]
    mock_ddgs.return_value.__enter__.return_value = mock_search

    # Mock analysis response
    analysis_response = Mock()
    analysis_response.content = "Test analysis"

    # Mock research brief JSON response
    research_brief_response = Mock()
    research_brief_response.content = json.dumps(
        {
            "key_statistics": ["Stat 1", "Stat 2"],
            "expert_quotes": ["Quote 1"],
            "case_studies": ["Case 1"],
            "key_definitions": {"term1": "definition1"},
            "counter_arguments": ["Counter 1"],
        }
    )

    mock_llm.invoke.side_effect = [analysis_response, research_brief_response]

    # Conduct research
    result = research_agent.research("test topic")

    # Should have research brief from LLM
    assert "research_brief" in result
    assert result["research_brief"]["key_statistics"] == ["Stat 1", "Stat 2"]
    assert result["research_brief"]["expert_quotes"] == ["Quote 1"]
    assert result["research_brief"]["case_studies"] == ["Case 1"]
    assert result["research_brief"]["key_definitions"] == {"term1": "definition1"}
    assert result["research_brief"]["counter_arguments"] == ["Counter 1"]
    assert len(result["research_brief"]["raw_sources"]) == 2
    assert len(result["search_results"]) == 2
    assert "analysis" in result


@patch("src.agents.researcher.DDGS")
def test_create_research_brief_json_parse_error(mock_ddgs, research_agent, mock_llm):
    """Test create_research_brief handles JSON parse errors gracefully."""
    search_results = [
        {"title": "Article 1", "body": "Content 1", "href": "https://test1.com"},
    ]

    # Mock invalid JSON response
    mock_llm.invoke.return_value.content = "This is not valid JSON"

    # Call create_research_brief
    result = research_agent.create_research_brief("test angle", search_results)

    # Should return default structure with empty data
    assert result["key_statistics"] == []
    assert result["expert_quotes"] == []
    assert result["case_studies"] == []
    assert result["key_definitions"] == {}
    assert result["counter_arguments"] == []
    assert result["raw_sources"] == search_results


@patch("src.agents.researcher.DDGS")
def test_create_research_brief_non_object_json(mock_ddgs, research_agent, mock_llm):
    """Test create_research_brief handles non-object JSON gracefully."""
    search_results = [
        {"title": "Article 1", "body": "Content 1", "href": "https://test1.com"},
    ]

    # Mock valid JSON that is not an object (a list)
    mock_llm.invoke.return_value.content = '["item1", "item2"]'

    # Call create_research_brief
    result = research_agent.create_research_brief("test angle", search_results)

    # Should return default structure with empty data
    assert result["key_statistics"] == []
    assert result["expert_quotes"] == []
    assert result["case_studies"] == []
    assert result["key_definitions"] == {}
    assert result["counter_arguments"] == []
    assert result["raw_sources"] == search_results


@patch("src.agents.researcher.DDGS")
def test_create_research_brief_string_json(mock_ddgs, research_agent, mock_llm):
    """Test create_research_brief handles JSON string gracefully."""
    search_results = [
        {"title": "Article 1", "body": "Content 1", "href": "https://test1.com"},
    ]

    # Mock valid JSON that is a string
    mock_llm.invoke.return_value.content = '"just a string"'

    # Call create_research_brief
    result = research_agent.create_research_brief("test angle", search_results)

    # Should return default structure with empty data
    assert result["key_statistics"] == []
    assert result["expert_quotes"] == []
    assert result["case_studies"] == []
    assert result["key_definitions"] == {}
    assert result["counter_arguments"] == []
    assert result["raw_sources"] == search_results
