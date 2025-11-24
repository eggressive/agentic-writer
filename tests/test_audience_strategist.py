"""Tests for the AudienceStrategist."""

import json

import pytest

from src.agents.audience_strategist import AudienceStrategist


@pytest.fixture
def audience_strategist(mock_llm):
    """Create an AudienceStrategist instance."""
    return AudienceStrategist(llm=mock_llm)


def test_analyze_returns_persona_on_valid_json(audience_strategist, mock_llm):
    """Test analyze returns persona when LLM returns valid JSON."""
    valid_persona = {
        "persona_name": "Sarah, the Tech Startup CTO",
        "demographics": {
            "job_title": "CTO",
            "industry": "Technology",
            "experience_level": "expert",
        },
        "knowledge_state": {
            "what_they_know": "Basic cloud concepts",
            "what_they_need": "Advanced kubernetes strategies",
            "knowledge_gaps": ["service mesh", "observability"],
        },
        "goals": {
            "primary_goal": "Scale infrastructure efficiently",
            "use_case": "Production deployment",
            "success_metric": "99.9% uptime",
        },
        "pain_points": [
            "Complex documentation",
            "Lack of real-world examples",
        ],
        "reading_context": {
            "when": "During work hours",
            "where": "Desktop",
            "attention_span": "15-20 minutes",
        },
        "content_preferences": {
            "tone": "technical",
            "depth": "deep dive",
            "format": "code examples and diagrams",
        },
    }

    mock_llm.invoke.return_value.content = json.dumps(valid_persona)

    result = audience_strategist.analyze("Kubernetes Best Practices")

    assert result["persona_name"] == "Sarah, the Tech Startup CTO"
    assert result["demographics"]["job_title"] == "CTO"
    assert result["goals"]["primary_goal"] == "Scale infrastructure efficiently"


def test_analyze_with_audience_hint(audience_strategist, mock_llm):
    """Test analyze passes audience hint to LLM prompt."""
    valid_persona = {
        "persona_name": "Test Persona",
        "demographics": {"job_title": "Test"},
        "knowledge_state": {},
        "goals": {},
        "pain_points": [],
    }

    mock_llm.invoke.return_value.content = json.dumps(valid_persona)

    result = audience_strategist.analyze(
        "Remote Work", audience_hint="Enterprise executives"
    )

    assert result["persona_name"] == "Test Persona"
    # Verify the LLM was called
    mock_llm.invoke.assert_called_once()


def test_analyze_returns_empty_persona_on_invalid_json(audience_strategist, mock_llm):
    """Test analyze returns empty persona when LLM returns invalid JSON."""
    mock_llm.invoke.return_value.content = "This is not valid JSON"

    result = audience_strategist.analyze("Test Topic")

    # Should return empty persona structure
    assert result["persona_name"] == "General Reader"
    assert result["demographics"]["job_title"] == "Unknown"
    assert result["goals"]["primary_goal"] == "Learn about the topic"


def test_analyze_returns_empty_persona_on_non_object_json(
    audience_strategist, mock_llm
):
    """Test analyze returns empty persona when LLM returns non-object JSON."""
    mock_llm.invoke.return_value.content = '["item1", "item2"]'

    result = audience_strategist.analyze("Test Topic")

    # Should return empty persona structure
    assert result["persona_name"] == "General Reader"


def test_analyze_returns_empty_persona_on_string_json(audience_strategist, mock_llm):
    """Test analyze returns empty persona when LLM returns JSON string."""
    mock_llm.invoke.return_value.content = '"just a string"'

    result = audience_strategist.analyze("Test Topic")

    # Should return empty persona structure
    assert result["persona_name"] == "General Reader"


def test_validate_persona_with_valid_persona(audience_strategist):
    """Test validate_persona returns True for valid persona."""
    valid_persona = {
        "persona_name": "Test Persona",
        "demographics": {"job_title": "Developer"},
        "knowledge_state": {"what_they_know": "Basics"},
        "goals": {"primary_goal": "Learn"},
        "pain_points": ["Frustration 1"],
    }

    assert audience_strategist.validate_persona(valid_persona) is True


def test_validate_persona_with_missing_keys(audience_strategist):
    """Test validate_persona returns False for persona with missing keys."""
    invalid_persona = {
        "persona_name": "Test Persona",
        "demographics": {"job_title": "Developer"},
        # Missing knowledge_state, goals, pain_points
    }

    assert audience_strategist.validate_persona(invalid_persona) is False


def test_validate_persona_with_empty_dict(audience_strategist):
    """Test validate_persona returns False for empty dict."""
    assert audience_strategist.validate_persona({}) is False


def test_get_empty_persona_structure(audience_strategist):
    """Test _get_empty_persona returns correct structure."""
    empty_persona = audience_strategist._get_empty_persona()

    assert "persona_name" in empty_persona
    assert "demographics" in empty_persona
    assert "knowledge_state" in empty_persona
    assert "goals" in empty_persona
    assert "pain_points" in empty_persona
    assert "reading_context" in empty_persona
    assert "content_preferences" in empty_persona
    assert empty_persona["persona_name"] == "General Reader"
