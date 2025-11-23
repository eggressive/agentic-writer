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
    
    # Mock analysis response with proper JSON
    analysis_dict = {"analysis": "Test analysis"}
    mock_llm.invoke.return_value.content = json.dumps(analysis_dict)
    
    # Conduct research
    result = research_agent.research("test topic")
    
    # Should have fallback synthesis
    assert result["synthesis"] == "No search results found. Proceeding with general knowledge."
    assert result["search_results"] == []
    assert "analysis" in result


@patch("src.agents.researcher.DDGS")
def test_research_with_successful_search(mock_ddgs, research_agent, mock_llm):
    """Test research with successful search results."""
    # Mock successful search results
    mock_search = Mock()
    mock_search.text.return_value = [
        {"title": "Article 1", "body": "Content 1", "href": "https://test1.com"},
        {"title": "Article 2", "body": "Content 2", "href": "https://test2.com"}
    ]
    mock_ddgs.return_value.__enter__.return_value = mock_search
    
    # Mock analysis and synthesis responses with proper JSON
    analysis_response = Mock()
    analysis_dict = {"analysis": "Test analysis"}
    analysis_response.content = json.dumps(analysis_dict)
    
    synthesis_response = Mock()
    synthesis_response.content = "Synthesized research content"
    
    mock_llm.invoke.side_effect = [analysis_response, synthesis_response]
    
    # Conduct research
    result = research_agent.research("test topic")
    
    # Should have synthesis from LLM
    assert result["synthesis"] == "Synthesized research content"
    assert len(result["search_results"]) == 2
    assert "analysis" in result
