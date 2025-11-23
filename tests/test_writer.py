"""Tests for the WriterAgent."""

import pytest
from unittest.mock import Mock
from src.agents.writer import WriterAgent


@pytest.fixture
def mock_llm():
    """Create a mock LLM."""
    mock = Mock()
    mock_response = Mock()
    mock_response.content = "Test content"
    mock.invoke.return_value = mock_response
    return mock


@pytest.fixture
def writer_agent(mock_llm):
    """Create a WriterAgent instance."""
    return WriterAgent(llm=mock_llm)


def test_write_section(writer_agent, mock_llm):
    """Test write_section method."""
    # Mock response
    mock_llm.invoke.return_value.content = "Section content here"
    
    # Write section
    result = writer_agent.write_section(
        section_title="Introduction",
        section_context="Context about the section",
        full_context="Full article context"
    )
    
    # Should return section content
    assert result == "Section content here"
    assert mock_llm.invoke.called


def test_extract_title_with_title(writer_agent):
    """Test _extract_title with valid title."""
    content = "# My Article Title\n\nSome content here."
    
    title = writer_agent._extract_title(content)
    
    assert title == "My Article Title"


def test_extract_title_without_title(writer_agent):
    """Test _extract_title when no title is found."""
    content = "Some content without a title heading.\nMore content here."
    
    title = writer_agent._extract_title(content)
    
    assert title is None


def test_extract_title_with_multiple_headings(writer_agent):
    """Test _extract_title returns first title."""
    content = "# First Title\n\nContent here.\n\n# Second Title\n\nMore content."
    
    title = writer_agent._extract_title(content)
    
    assert title == "First Title"


def test_extract_title_with_whitespace(writer_agent):
    """Test _extract_title handles whitespace correctly."""
    content = "#   Title With Spaces   \n\nContent."
    
    title = writer_agent._extract_title(content)
    
    assert title == "Title With Spaces"


def test_write_article(writer_agent, mock_llm):
    """Test write_article creates article with sections."""
    # Mock responses for outline, sections, meta, and tags
    outline_response = Mock()
    outline_response.content = "## Section 1\nDescription\n\n## Section 2\nDescription"
    
    section1_response = Mock()
    section1_response.content = "Section 1 content"
    
    section2_response = Mock()
    section2_response.content = "Section 2 content"
    
    meta_response = Mock()
    meta_response.content = "Article meta description"
    
    tags_response = Mock()
    tags_response.content = "tag1, tag2, tag3"
    
    mock_llm.invoke.side_effect = [
        outline_response,
        section1_response,
        section2_response,
        meta_response,
        tags_response
    ]
    
    research_data = {
        "topic": "Test Topic",
        "analysis": "Test analysis",
        "synthesis": "Test synthesis"
    }
    
    result = writer_agent.write_article(
        topic="Test Topic",
        research_data=research_data,
        style="professional",
        target_audience="experts"
    )
    
    assert "content" in result
    assert "title" in result
    assert "meta_description" in result
    assert "tags" in result
    assert result["word_count"] > 0
