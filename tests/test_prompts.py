"""Tests for the src/prompts module."""

import pytest

from src.prompts import (
    ANALYZE_TOPIC_SYSTEM,
    IMAGE_PLACEMENT_SYSTEM,
    IMAGE_QUERIES_SYSTEM,
    IMAGE_SUGGESTIONS_SYSTEM,
    META_DESCRIPTION_SYSTEM,
    OUTLINE_SYSTEM,
    PERSONA_SYSTEM_PROMPT,
    RESEARCH_BRIEF_SYSTEM,
    TAGS_SYSTEM,
    WRITE_ARTICLE_SYSTEM,
    WRITE_SECTION_SYSTEM,
)


class TestPromptConstants:
    """All prompt constants are importable, non-empty strings."""

    @pytest.mark.parametrize(
        "constant",
        [
            PERSONA_SYSTEM_PROMPT,
            ANALYZE_TOPIC_SYSTEM,
            RESEARCH_BRIEF_SYSTEM,
            OUTLINE_SYSTEM,
            WRITE_SECTION_SYSTEM,
            WRITE_ARTICLE_SYSTEM,
            META_DESCRIPTION_SYSTEM,
            TAGS_SYSTEM,
            IMAGE_QUERIES_SYSTEM,
            IMAGE_SUGGESTIONS_SYSTEM,
            IMAGE_PLACEMENT_SYSTEM,
        ],
    )
    def test_constant_is_nonempty_string(self, constant):
        assert isinstance(constant, str) and len(constant) > 0

    def test_persona_prompt_mentions_json(self):
        assert "JSON" in PERSONA_SYSTEM_PROMPT

    def test_research_brief_mentions_key_statistics(self):
        assert "key_statistics" in RESEARCH_BRIEF_SYSTEM

    def test_write_article_mentions_word_count(self):
        assert "1200-1500" in WRITE_ARTICLE_SYSTEM

    def test_outline_system_ends_with_newline(self):
        """OUTLINE_SYSTEM ends with newline so callers can append base_instructions."""
        assert OUTLINE_SYSTEM.endswith("\n")

    def test_image_placement_mentions_json_array(self):
        assert "JSON array" in IMAGE_PLACEMENT_SYSTEM


class TestPromptComposition:
    """Verify dynamic-composition patterns used by agents work correctly."""

    def test_outline_system_plus_instructions(self):
        """OUTLINE_SYSTEM can be appended with runtime instructions."""
        instructions = "The outline should be logical, engaging, and comprehensive."
        composed = OUTLINE_SYSTEM + instructions
        assert "professional content writer" in composed
        assert instructions in composed

    def test_write_article_system_plus_style(self):
        """WRITE_ARTICLE_SYSTEM can be appended with style and persona instructions."""
        style = "\nWriting Style: casual"
        persona = "\nTarget Reader: Jane"
        composed = WRITE_ARTICLE_SYSTEM + style + persona
        assert "1200-1500" in composed
        assert "casual" in composed
        assert "Jane" in composed
