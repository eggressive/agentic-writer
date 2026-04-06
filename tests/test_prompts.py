"""Tests for the src/prompts/ module."""

import pytest

import src.prompts as prompts
from src.prompts.audience import PERSONA_SYSTEM_PROMPT
from src.prompts.image import (
    IMAGE_PLACEMENT_SYSTEM_PROMPT,
    IMAGE_QUERIES_SYSTEM_PROMPT,
    IMAGE_SUGGESTIONS_SYSTEM_PROMPT,
)
from src.prompts.researcher import (
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
    def test_persona_system_prompt_is_string(self):
        assert isinstance(PERSONA_SYSTEM_PROMPT, str)

    def test_persona_system_prompt_non_empty(self):
        assert len(PERSONA_SYSTEM_PROMPT) > 0

    def test_persona_system_prompt_contains_json_hint(self):
        assert "JSON" in PERSONA_SYSTEM_PROMPT

    def test_persona_system_prompt_contains_required_keys(self):
        for key in ("persona_name", "demographics", "goals", "pain_points"):
            assert key in PERSONA_SYSTEM_PROMPT


class TestResearcherPrompts:
    def test_analyze_topic_prompt_is_string(self):
        assert isinstance(ANALYZE_TOPIC_SYSTEM_PROMPT, str)

    def test_analyze_topic_prompt_non_empty(self):
        assert len(ANALYZE_TOPIC_SYSTEM_PROMPT) > 0

    def test_research_brief_prompt_is_string(self):
        assert isinstance(RESEARCH_BRIEF_SYSTEM_PROMPT, str)

    def test_research_brief_prompt_contains_json_fields(self):
        for field in (
            "key_statistics",
            "expert_quotes",
            "case_studies",
            "key_definitions",
        ):
            assert field in RESEARCH_BRIEF_SYSTEM_PROMPT

    def test_research_brief_prompt_instructs_json_only(self):
        assert "JSON" in RESEARCH_BRIEF_SYSTEM_PROMPT


class TestWriterPrompts:
    def test_outline_template_is_string(self):
        assert isinstance(OUTLINE_SYSTEM_PROMPT_TEMPLATE, str)

    def test_outline_template_has_placeholder(self):
        assert "{base_instructions}" in OUTLINE_SYSTEM_PROMPT_TEMPLATE

    def test_outline_template_formats_correctly(self):
        result = OUTLINE_SYSTEM_PROMPT_TEMPLATE.format(
            base_instructions="The outline should be logical."
        )
        assert "The outline should be logical." in result
        assert "{base_instructions}" not in result

    def test_section_prompt_is_string(self):
        assert isinstance(SECTION_SYSTEM_PROMPT, str)

    def test_section_prompt_non_empty(self):
        assert len(SECTION_SYSTEM_PROMPT) > 0

    def test_article_template_is_string(self):
        assert isinstance(ARTICLE_SYSTEM_PROMPT_TEMPLATE, str)

    def test_article_template_has_placeholders(self):
        assert "{style_instruction}" in ARTICLE_SYSTEM_PROMPT_TEMPLATE
        assert "{persona_instruction}" in ARTICLE_SYSTEM_PROMPT_TEMPLATE

    def test_article_template_formats_correctly(self):
        result = ARTICLE_SYSTEM_PROMPT_TEMPLATE.format(
            style_instruction="\nWriting Style: professional",
            persona_instruction="",
        )
        assert "professional" in result
        assert "{style_instruction}" not in result
        assert "{persona_instruction}" not in result

    def test_article_template_formats_with_empty_placeholders(self):
        result = ARTICLE_SYSTEM_PROMPT_TEMPLATE.format(
            style_instruction="", persona_instruction=""
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_meta_description_prompt_is_string(self):
        assert isinstance(META_DESCRIPTION_SYSTEM_PROMPT, str)

    def test_meta_description_prompt_mentions_characters(self):
        assert (
            "150" in META_DESCRIPTION_SYSTEM_PROMPT
            or "characters" in META_DESCRIPTION_SYSTEM_PROMPT
        )

    def test_tags_prompt_is_string(self):
        assert isinstance(TAGS_SYSTEM_PROMPT, str)

    def test_tags_prompt_mentions_tags(self):
        assert "tags" in TAGS_SYSTEM_PROMPT.lower()


class TestImagePrompts:
    def test_queries_prompt_is_string(self):
        assert isinstance(IMAGE_QUERIES_SYSTEM_PROMPT, str)

    def test_queries_prompt_non_empty(self):
        assert len(IMAGE_QUERIES_SYSTEM_PROMPT) > 0

    def test_suggestions_prompt_is_string(self):
        assert isinstance(IMAGE_SUGGESTIONS_SYSTEM_PROMPT, str)

    def test_suggestions_prompt_contains_format_guidance(self):
        assert "Image" in IMAGE_SUGGESTIONS_SYSTEM_PROMPT

    def test_placement_prompt_is_string(self):
        assert isinstance(IMAGE_PLACEMENT_SYSTEM_PROMPT, str)

    def test_placement_prompt_mentions_json(self):
        assert "JSON" in IMAGE_PLACEMENT_SYSTEM_PROMPT

    def test_placement_prompt_mentions_heading(self):
        assert "heading" in IMAGE_PLACEMENT_SYSTEM_PROMPT


class TestPromptsPackageExports:
    """Verify __init__.py re-exports all expected names."""

    @pytest.mark.parametrize(
        "name",
        [
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
        ],
    )
    def test_export_exists(self, name):
        assert hasattr(prompts, name), f"src.prompts is missing export: {name}"

    def test_all_list_matches_exports(self):
        for name in prompts.__all__:
            assert hasattr(prompts, name), f"{name} in __all__ but not exported"
