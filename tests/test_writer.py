"""Tests for the WriterAgent."""

from unittest.mock import Mock

import pytest

from src.agents.writer import WriterAgent


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
        full_context="Full article context",
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


def test_create_outline_with_persona(writer_agent, mock_llm):
    """Test create_outline with a complete persona (happy path)."""
    # Mock response
    mock_llm.invoke.return_value.content = (
        "# Article Title\n\n"
        "## Introduction\nHook for business managers\n\n"
        "## Section 1\nKey points addressing cost reduction"
    )

    persona = {
        "persona_name": "Business Manager",
        "goals": {
            "primary_goal": "Reduce operational costs",
            "secondary_goals": ["Improve efficiency"],
        },
        "pain_points": ["High overhead", "Complex processes", "Limited budget"],
        "knowledge_state": {
            "what_they_know": "Basic concepts",
            "what_they_need": "Practical implementation strategies",
        },
    }

    result = writer_agent.create_outline(
        topic="Cost Optimization Strategies",
        research="Research content about cost optimization",
        persona=persona,
    )

    # Should return outline content
    assert "Article Title" in result
    assert mock_llm.invoke.called


def test_create_outline_without_persona(writer_agent, mock_llm):
    """Test create_outline without a persona (backward compatibility)."""
    # Mock response
    mock_llm.invoke.return_value.content = (
        "# Generic Article Title\n\n"
        "## Introduction\nGeneral hook\n\n"
        "## Main Section\nContent description"
    )

    result = writer_agent.create_outline(
        topic="General Topic",
        research="Some research content",
    )

    # Should return outline content without persona context
    assert "Generic Article Title" in result
    assert mock_llm.invoke.called


def test_create_outline_with_partial_persona(writer_agent, mock_llm):
    """Test create_outline with an incomplete persona dict (partial data)."""
    # Mock response
    mock_llm.invoke.return_value.content = (
        "# Partial Persona Article\n\n"
        "## Introduction\nIntro content\n\n"
        "## Section\nSection content"
    )

    # Persona with only some fields populated
    partial_persona = {
        "persona_name": "Developer",
        # Missing goals, pain_points, and knowledge_state
    }

    result = writer_agent.create_outline(
        topic="Development Best Practices",
        research="Research about development practices",
        persona=partial_persona,
    )

    # Should handle partial persona gracefully
    assert "Partial Persona Article" in result
    assert mock_llm.invoke.called


def test_create_outline_with_empty_persona(writer_agent, mock_llm):
    """Test create_outline with an empty persona dict."""
    # Mock response
    mock_llm.invoke.return_value.content = (
        "# Empty Persona Article\n\n"
        "## Introduction\nIntro content\n\n"
        "## Section\nSection content"
    )

    # Empty persona dict
    empty_persona = {}

    result = writer_agent.create_outline(
        topic="Some Topic",
        research="Some research",
        persona=empty_persona,
    )

    # Should handle empty persona gracefully (no persona context added)
    assert "Empty Persona Article" in result
    assert mock_llm.invoke.called


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
        tags_response,
    ]

    research_data = {
        "topic": "Test Topic",
        "analysis": "Test analysis",
        "research_brief": {
            "key_statistics": ["Stat 1", "Stat 2"],
            "expert_quotes": ["Quote 1"],
            "case_studies": ["Case 1"],
            "key_definitions": {"term1": "definition1"},
            "counter_arguments": ["Counter 1"],
            "raw_sources": [],
        },
    }

    result = writer_agent.write_article(
        topic="Test Topic",
        research_data=research_data,
        style="professional",
        target_audience="experts",
    )

    assert "content" in result
    assert "title" in result
    assert "meta_description" in result
    assert "tags" in result
    assert result["word_count"] > 0
