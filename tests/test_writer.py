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


def test_build_persona_context_without_persona(writer_agent):
    """Test _build_persona_context returns empty string for None persona."""
    result = writer_agent._build_persona_context(None)
    assert result == ""

    result = writer_agent._build_persona_context({})
    assert result == ""


def test_build_persona_context_basic(writer_agent):
    """Test _build_persona_context for outline (include_content_prefs=False)."""
    persona = {
        "persona_name": "Tech Lead",
        "goals": {"primary_goal": "Learn best practices"},
        "pain_points": ["Time constraints", "Legacy code", "Documentation gaps"],
        "knowledge_state": {"what_they_need": "Practical examples"},
    }

    result = writer_agent._build_persona_context(persona, include_content_prefs=False)

    assert "Target Audience: Tech Lead" in result
    assert "Audience Goal: Learn best practices" in result
    assert (
        "Address Pain Points: Time constraints, Legacy code, Documentation gaps"
        in result
    )
    assert "Information Needs: Practical examples" in result
    # Should NOT include content preferences
    assert "Preferred Tone" not in result
    assert "Depth Level" not in result
    assert "Reader Time Available" not in result


def test_build_persona_context_full(writer_agent):
    """Test _build_persona_context for article (include_content_prefs=True)."""
    persona = {
        "persona_name": "Tech Lead",
        "goals": {"primary_goal": "Learn best practices"},
        "pain_points": ["Time constraints", "Legacy code", "Documentation gaps"],
        "knowledge_state": {"what_they_need": "Practical examples"},
        "content_preferences": {"tone": "professional", "depth": "advanced"},
        "reading_context": {"attention_span": "15 minutes"},
    }

    result = writer_agent._build_persona_context(persona, include_content_prefs=True)

    assert "Target Reader: Tech Lead" in result
    assert "Reader's Goal: Learn best practices" in result
    assert (
        "Address Pain Points: Time constraints, Legacy code, Documentation gaps"
        in result
    )
    assert "What Reader Needs: Practical examples" in result
    assert "Preferred Tone: professional" in result
    assert "Depth Level: advanced" in result
    assert "Reader Time Available: 15 minutes" in result


def test_build_persona_context_with_non_string_pain_points(writer_agent):
    """Test _build_persona_context handles non-string pain points."""
    persona = {
        "persona_name": "Developer",
        "pain_points": [{"issue": "bug"}, "string point", 123],
    }

    result = writer_agent._build_persona_context(persona)

    # Should convert non-strings to strings
    assert "Address Pain Points:" in result


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
