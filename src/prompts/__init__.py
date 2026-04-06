"""Prompt templates for agentic-writer agents.

Each sub-module contains the system-prompt constants for one agent.
Import from the sub-module directly, or re-export through this package.
"""

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

__all__ = [
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
