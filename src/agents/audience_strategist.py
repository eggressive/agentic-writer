"""Audience strategist agent for creating reader personas."""

import json
import logging
from typing import Any, Dict, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

PERSONA_SYSTEM_PROMPT = """You are an audience research specialist. \
Create a detailed reader persona for someone who would benefit most from \
an article on the given topic.

Return your analysis as a JSON object with the following structure:
{
    "persona_name": "A descriptive name (e.g., 'Sarah, the Tech Startup CTO')",
    "demographics": {
        "job_title": "...",
        "industry": "...",
        "experience_level": "beginner|intermediate|expert"
    },
    "knowledge_state": {
        "what_they_know": "What they already understand about this topic",
        "what_they_need": "What they need to learn",
        "knowledge_gaps": ["specific gap 1", "specific gap 2"]
    },
    "goals": {
        "primary_goal": "What they want to achieve by reading this",
        "use_case": "How they will apply this information",
        "success_metric": "How they will know they succeeded"
    },
    "pain_points": [
        "Frustration 1 with existing content",
        "Frustration 2",
        "Frustration 3"
    ],
    "reading_context": {
        "when": "When they typically read this content",
        "where": "Where they read (mobile, desktop, etc.)",
        "attention_span": "How much time they have"
    },
    "content_preferences": {
        "tone": "preferred tone (e.g., conversational, formal, technical)",
        "depth": "preferred depth level",
        "format": "preferred format elements (e.g., code examples, diagrams)"
    }
}

Be specific and realistic. Base the persona on actual user behaviors, not stereotypes.
Return ONLY the JSON object, no additional text."""


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
