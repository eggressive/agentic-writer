"""Writer agent for creating content based on research."""

import logging
from typing import Any, Dict, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class WriterAgent:
    """Agent responsible for writing articles based on research."""

    def __init__(self, llm: ChatOpenAI):
        """Initialize the writer agent.

        Args:
            llm: Language model for content generation
        """
        self.llm = llm
        self.logger = logging.getLogger(__name__)

    def _format_research_brief(self, research_brief: Dict[str, Any]) -> str:
        """Format structured research brief into text for article writing.

        Args:
            research_brief: Structured research brief dictionary

        Returns:
            Formatted text representation of the research brief
        """
        sections = []

        # Key Statistics
        key_statistics = research_brief.get("key_statistics", [])
        if key_statistics:
            sections.append("Key Statistics:")
            for stat in key_statistics:
                if isinstance(stat, dict):
                    sections.append(f"- {stat.get('statistic', str(stat))}")
                else:
                    sections.append(f"- {stat}")

        # Expert Quotes
        expert_quotes = research_brief.get("expert_quotes", [])
        if expert_quotes:
            sections.append("\nExpert Quotes:")
            for quote in expert_quotes:
                if isinstance(quote, dict):
                    sections.append(f"- {quote.get('quote', str(quote))}")
                else:
                    sections.append(f"- {quote}")

        # Case Studies
        case_studies = research_brief.get("case_studies", [])
        if case_studies:
            sections.append("\nCase Studies:")
            for study in case_studies:
                if isinstance(study, dict):
                    sections.append(f"- {study.get('summary', str(study))}")
                else:
                    sections.append(f"- {study}")

        # Key Definitions
        key_definitions = research_brief.get("key_definitions", {})
        if key_definitions:
            sections.append("\nKey Definitions:")
            for term, definition in key_definitions.items():
                sections.append(f"- {term}: {definition}")

        # Counter Arguments
        counter_arguments = research_brief.get("counter_arguments", [])
        if counter_arguments:
            sections.append("\nCounter Arguments:")
            for arg in counter_arguments:
                sections.append(f"- {arg}")

        return "\n".join(sections) if sections else ""

    def create_outline(
        self, topic: str, research: str, persona: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create an article outline based on research.

        Args:
            topic: Article topic
            research: Formatted research text
            persona: Detailed reader persona from audience strategist

        Returns:
            Article outline
        """
        self.logger.info(f"Creating outline for: {topic}")

        # Build persona context for structure
        persona_context = ""
        if persona and isinstance(persona, dict):
            persona_name = persona.get("persona_name", "")
            goals = persona.get("goals", {})
            pain_points = persona.get("pain_points", [])
            knowledge_state = persona.get("knowledge_state", {})

            if persona_name:
                persona_context += f"\nTarget Audience: {persona_name}"
            if goals.get("primary_goal"):
                persona_context += f"\nAudience Goal: {goals.get('primary_goal')}"
            if pain_points:
                pain_points_str = ", ".join(pain_points[:3])
                persona_context += f"\nAddress Pain Points: {pain_points_str}"
            if knowledge_state.get("what_they_need"):
                persona_context += (
                    f"\nInformation Needs: {knowledge_state.get('what_they_need')}"
                )

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=f"""You are a professional content writer. Create a detailed article outline with:
1. An engaging title
2. Introduction hook
3. 3-5 main sections with subsections
4. Conclusion
5. Key points to cover in each section

The outline should be logical, engaging, and comprehensive.
Tailor the structure to the target audience:{persona_context}"""
                ),
                HumanMessage(content=f"Topic: {topic}\n\nResearch:\n{research}"),
            ]
        )

        response = self.llm.invoke(prompt.format_messages())

        return response.content

    def write_section(
        self, section_title: str, section_context: str, full_context: str
    ) -> str:
        """Write a single section of the article.

        Args:
            section_title: Title of the section
            section_context: Specific context for this section
            full_context: Full article context

        Returns:
            Written section content
        """
        self.logger.info(f"Writing section: {section_title}")

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are a professional content writer. Write an engaging, informative section for an article.
Requirements:
- Use clear, accessible language
- Include specific examples and details
- Maintain a professional yet conversational tone
- Use proper formatting with paragraphs
- Aim for 200-400 words per section"""
                ),
                HumanMessage(
                    content=f"Section Title: {section_title}\n\nSection Context:\n{section_context}\n\nFull Context:\n{full_context}"
                ),
            ]
        )

        response = self.llm.invoke(prompt.format_messages())

        return response.content

    def write_article(
        self,
        topic: str,
        research_data: Dict[str, Any],
        style: Optional[str] = None,
        target_audience: Optional[str] = None,
        persona: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Write a complete article based on research.

        Args:
            topic: Article topic
            research_data: Research findings dictionary
            style: Writing style (e.g., "professional", "casual", "technical")
            target_audience: Target audience description
            persona: Detailed reader persona from audience strategist

        Returns:
            Dictionary containing the article and metadata
        """
        self.logger.info(f"Writing article on: {topic}")

        # Extract research brief and format it for use
        research_brief = research_data.get("research_brief", {})
        research_synthesis = self._format_research_brief(research_brief)
        research_analysis = research_data.get("analysis", "")

        # Create style instructions
        style_instruction = ""
        if style:
            style_instruction += f"\nWriting Style: {style}"
        if target_audience:
            style_instruction += f"\nTarget Audience: {target_audience}"

        # Add persona-based instructions if available
        persona_instruction = ""
        if persona and isinstance(persona, dict):
            persona_name = persona.get("persona_name", "")
            content_prefs = persona.get("content_preferences", {})
            goals = persona.get("goals", {})
            knowledge_state = persona.get("knowledge_state", {})
            pain_points = persona.get("pain_points", [])
            reading_context = persona.get("reading_context", {})

            if persona_name:
                persona_instruction += f"\nTarget Reader: {persona_name}"
            if content_prefs.get("tone"):
                persona_instruction += f"\nPreferred Tone: {content_prefs.get('tone')}"
            if content_prefs.get("depth"):
                persona_instruction += f"\nDepth Level: {content_prefs.get('depth')}"
            if goals.get("primary_goal"):
                persona_instruction += f"\nReader's Goal: {goals.get('primary_goal')}"
            if knowledge_state.get("what_they_need"):
                persona_instruction += (
                    f"\nWhat Reader Needs: {knowledge_state.get('what_they_need')}"
                )
            if pain_points:
                pain_points_str = ", ".join(pain_points[:3])
                persona_instruction += f"\nAddress Pain Points: {pain_points_str}"
            if reading_context.get("attention_span"):
                persona_instruction += (
                    f"\nReader Time Available: {reading_context.get('attention_span')}"
                )

        # Create outline
        outline = self.create_outline(topic, research_synthesis, persona)

        # Generate full article
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=f"""You are a professional content writer. Write a comprehensive, engaging article based on the provided research and outline.

Requirements:
- Follow the outline structure
- Write 1200-1500 words
- Use clear, engaging language
- Include an introduction, body sections, and conclusion
- Add smooth transitions between sections
- Cite key facts and statistics when relevant
- Use markdown formatting (headers, bold, italics, lists)
- Make it informative yet accessible{style_instruction}{persona_instruction}"""
                ),
                HumanMessage(
                    content=f"Topic: {topic}\n\nOutline:\n{outline}\n\nResearch:\n{research_synthesis}\n\nAnalysis:\n{research_analysis}"
                ),
            ]
        )

        response = self.llm.invoke(prompt.format_messages())
        article_content = response.content

        # Generate title
        title = (
            self._extract_title(article_content) or f"A Comprehensive Guide to {topic}"
        )

        # Generate meta description
        meta_description = self._generate_meta_description(topic, article_content)

        # Generate tags
        tags = self._generate_tags(topic, research_data)

        return {
            "title": title,
            "content": article_content,
            "outline": outline,
            "meta_description": meta_description,
            "tags": tags,
            "word_count": len(article_content.split()),
            "topic": topic,
        }

    def _extract_title(self, content: str) -> Optional[str]:
        """Extract title from article content.

        Args:
            content: Article content

        Returns:
            Extracted title or None
        """
        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        return None

    def _generate_meta_description(self, topic: str, content: str) -> str:
        """Generate a meta description for the article.

        Args:
            topic: Article topic
            content: Article content

        Returns:
            Meta description
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="Generate a compelling meta description (150-160 characters) for this article."
                ),
                HumanMessage(
                    content=f"Topic: {topic}\n\nContent preview:\n{content[:500]}"
                ),
            ]
        )

        response = self.llm.invoke(prompt.format_messages())

        return response.content.strip()

    def _generate_tags(self, topic: str, research_data: Dict[str, Any]) -> list:
        """Generate relevant tags for the article.

        Args:
            topic: Article topic
            research_data: Research data

        Returns:
            List of tags
        """
        # Format research brief for tag generation
        research_brief = research_data.get("research_brief", {})
        research_text = self._format_research_brief(research_brief)[:500]

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="Generate 5-8 relevant tags for this article. Return only the tags, comma-separated."
                ),
                HumanMessage(content=f"Topic: {topic}\n\nResearch: {research_text}"),
            ]
        )

        response = self.llm.invoke(prompt.format_messages())
        tags = [tag.strip() for tag in response.content.split(",")]

        return tags[:8]  # Limit to 8 tags
