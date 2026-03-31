"""Audience strategist agent for creating reader personas."""

import json
import logging
from typing import Any, Dict, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from ..prompts import PERSONA_SYSTEM_PROMPT


class AudienceStrategist:
    """Agent responsible for analyzing target audience and creating personas."""

    def __init__(self, llm: ChatOpenAI):
        """Initialize the audience strategist.

        Args:
            llm: Language model for persona generation
        """
        self.llm = llm
        self.logger = logging.getLogger(__name__)

    def _get_empty_persona(self) -> Dict[str, Any]:
        """Return an empty persona structure.

        Returns:
            Dictionary with empty persona structure
        """
        return {
            "persona_name": "General Reader",
            "demographics": {
                "job_title": "Unknown",
                "industry": "Unknown",
                "experience_level": "intermediate",
            },
            "knowledge_state": {
                "what_they_know": "Basic understanding of the topic",
                "what_they_need": "Comprehensive overview",
                "knowledge_gaps": [],
            },
            "goals": {
                "primary_goal": "Learn about the topic",
                "use_case": "General understanding",
                "success_metric": "Improved knowledge",
            },
            "pain_points": [],
            "reading_context": {
                "when": "During work hours",
                "where": "Desktop",
                "attention_span": "10-15 minutes",
            },
            "content_preferences": {
                "tone": "professional",
                "depth": "moderate",
                "format": "structured with examples",
            },
        }

    def analyze(
        self, topic: str, audience_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a detailed reader persona for the topic.

        Args:
            topic: The article topic
            audience_hint: Optional hint about target audience

        Returns:
            Dictionary containing detailed persona information
        """
        self.logger.info(f"Creating audience persona for: {topic}")

        audience_context = (
            f"\nTarget Audience Hint: {audience_hint}" if audience_hint else ""
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=PERSONA_SYSTEM_PROMPT),
                HumanMessage(content=f"Topic: {topic}{audience_context}"),
            ]
        )

        response = self.llm.invoke(prompt.format_messages())

        try:
            persona = json.loads(response.content)
            if not isinstance(persona, dict):
                self.logger.error(
                    "Persona JSON is not an object, returning empty persona"
                )
                return self._get_empty_persona()
            persona_name = persona.get("persona_name", "Unknown")
            self.logger.info(f"Created persona: {persona_name}")
            return persona
        except json.JSONDecodeError:
            self.logger.error("Failed to parse persona JSON, returning empty persona")
            return self._get_empty_persona()

    def validate_persona(self, persona: Dict[str, Any]) -> bool:
        """Validate that a persona has all required fields.

        Args:
            persona: Persona dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_keys = [
            "persona_name",
            "demographics",
            "knowledge_state",
            "goals",
            "pain_points",
            "reading_context",
            "content_preferences",
        ]
        return all(key in persona for key in required_keys)
