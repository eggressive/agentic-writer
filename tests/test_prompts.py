"""Tests for the src/prompts/ module."""

import pytest

from src.prompts.audience import PERSONA_SYSTEM_PROMPT
from src.prompts.image import (
    IMAGE_PLACEMENT_SYSTEM_PROMPT,
    IMAGE_QUERIES_SYSTEM_PROMPT,
    IMAGE_SUGGESTIONS_SYSTEM_PROMPT,
)
from src.prompts.research import (
    ANALYZE_TOPIC_SYSTEM_PROMPT,
    RESEARCH_BRIEF_SYSTEM_PROMPT,
)
from src.prompts.writer import (
    ARTICLE_SYSTEM_PROMPT_TEMPLATE,
    META_DESCRIPTION_SYSTEM_PROMPT,
    OUTLINE_SYSTEM_PROMPT_TEMPLATE,
    SECTION_SYSTEM_PROMPT,
    TAGS_SYSTEM_PROMPT,
)


class TestAudiencePrompts:
    def test_persona_prompt_is_nonempty_string(self):
        assert isinstance(PERSONA_SYSTEM_PROMPT, str)
        assert len(PERSONA_SYSTEM_PROMPT) > 0

    def test_persona_prompt_requests_json_output(self):
        assert "JSON" in PERSONA_SYSTEM_PROMPT

    def test_persona_prompt_includes_required_fields(self):
        for field in ["persona_name", "demographics", "goals", "pain_points"]:
            assert field in PERSONA_SYSTEM_PROMPT


class TestResearchPrompts:
    def test_analyze_topic_prompt_is_nonempty_string(self):
        assert isinstance(ANALYZE_TOPIC_SYSTEM_PROMPT, str)
        assert len(ANALYZE_TOPIC_SYSTEM_PROMPT) > 0

    def test_research_brief_prompt_is_nonempty_string(self):
        assert isinstance(RESEARCH_BRIEF_SYSTEM_PROMPT, str)
        assert len(RESEARCH_BRIEF_SYSTEM_PROMPT) > 0

    def test_research_brief_prompt_requests_json_output(self):
        assert "JSON" in RESEARCH_BRIEF_SYSTEM_PROMPT

    def test_research_brief_prompt_includes_required_keys(self):
        for key in [
            "key_statistics",
            "expert_quotes",
            "case_studies",
            "key_definitions",
        ]:
            assert key in RESEARCH_BRIEF_SYSTEM_PROMPT


class TestWriterPrompts:
    def test_static_prompts_are_nonempty_strings(self):
        for prompt in [
            SECTION_SYSTEM_PROMPT,
            META_DESCRIPTION_SYSTEM_PROMPT,
            TAGS_SYSTEM_PROMPT,
        ]:
            assert isinstance(prompt, str)
            assert len(prompt) > 0

    def test_outline_template_formats_with_base_instructions(self):
        result = OUTLINE_SYSTEM_PROMPT_TEMPLATE.format(
            base_instructions="Tailor for engineers."
        )
        assert "Tailor for engineers." in result
        assert "outline" in result.lower()

    def test_outline_template_raises_on_missing_placeholder(self):
        with pytest.raises(KeyError):
            OUTLINE_SYSTEM_PROMPT_TEMPLATE.format()

    def test_article_template_formats_with_instructions(self):
        result = ARTICLE_SYSTEM_PROMPT_TEMPLATE.format(
            style_instruction="\nWriting Style: casual",
            persona_instruction="\nTarget Reader: Jane",
        )
        assert "casual" in result
        assert "Jane" in result

    def test_article_template_raises_on_missing_placeholder(self):
        with pytest.raises(KeyError):
            ARTICLE_SYSTEM_PROMPT_TEMPLATE.format()

    def test_article_template_supports_empty_dynamic_parts(self):
        result = ARTICLE_SYSTEM_PROMPT_TEMPLATE.format(
            style_instruction="",
            persona_instruction="",
        )
        assert "1200-1500 words" in result


class TestImagePrompts:
    def test_all_image_prompts_are_nonempty_strings(self):
        for prompt in [
            IMAGE_QUERIES_SYSTEM_PROMPT,
            IMAGE_SUGGESTIONS_SYSTEM_PROMPT,
            IMAGE_PLACEMENT_SYSTEM_PROMPT,
        ]:
            assert isinstance(prompt, str)
            assert len(prompt) > 0

    def test_image_queries_prompt_mentions_queries(self):
        assert "queries" in IMAGE_QUERIES_SYSTEM_PROMPT.lower()

    def test_image_placement_prompt_mentions_json(self):
        assert "JSON" in IMAGE_PLACEMENT_SYSTEM_PROMPT


class TestPromptsPackageExports:
    """Verify the top-level src.prompts package exports all expected names."""

    def test_all_exports_importable(self):
        import src.prompts as prompts

        expected = [
            "PERSONA_SYSTEM_PROMPT",
            "ANALYZE_TOPIC_SYSTEM_PROMPT",
            "RESEARCH_BRIEF_SYSTEM_PROMPT",
            "OUTLINE_SYSTEM_PROMPT_TEMPLATE",
            "SECTION_SYSTEM_PROMPT",
            "ARTICLE_SYSTEM_PROMPT_TEMPLATE",
            "META_DESCRIPTION_SYSTEM_PROMPT",
            "TAGS_SYSTEM_PROMPT",
            "IMAGE_QUERIES_SYSTEM_PROMPT",
            "IMAGE_SUGGESTIONS_SYSTEM_PROMPT",
            "IMAGE_PLACEMENT_SYSTEM_PROMPT",
        ]
        for name in expected:
            assert hasattr(prompts, name), f"Missing export: {name}"
