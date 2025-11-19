"""Writer agent for creating content based on research."""

import logging
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage


class WriterAgent:
    """Agent responsible for writing articles based on research."""

    def __init__(self, llm: ChatOpenAI):
        """Initialize the writer agent.
        
        Args:
            llm: Language model for content generation
        """
        self.llm = llm
        self.logger = logging.getLogger(__name__)

    def create_outline(self, topic: str, research: str) -> str:
        """Create an article outline based on research.
        
        Args:
            topic: Article topic
            research: Research synthesis
            
        Returns:
            Article outline
        """
        self.logger.info(f"Creating outline for: {topic}")
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a professional content writer. Create a detailed article outline with:
1. An engaging title
2. Introduction hook
3. 3-5 main sections with subsections
4. Conclusion
5. Key points to cover in each section

The outline should be logical, engaging, and comprehensive."""),
            HumanMessage(content=f"Topic: {topic}\n\nResearch:\n{research}")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        
        return response.content

    def write_section(self, section_title: str, section_context: str, full_context: str) -> str:
        """Write a single section of the article.
        
        Args:
            section_title: Title of the section
            section_context: Specific context for this section
            full_context: Full article context
            
        Returns:
            Written section content
        """
        self.logger.info(f"Writing section: {section_title}")
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a professional content writer. Write an engaging, informative section for an article.
Requirements:
- Use clear, accessible language
- Include specific examples and details
- Maintain a professional yet conversational tone
- Use proper formatting with paragraphs
- Aim for 200-400 words per section"""),
            HumanMessage(content=f"Section Title: {section_title}\n\nSection Context:\n{section_context}\n\nFull Context:\n{full_context}")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        
        return response.content

    def write_article(
        self,
        topic: str,
        research_data: Dict[str, Any],
        style: Optional[str] = None,
        target_audience: Optional[str] = None
    ) -> Dict[str, Any]:
        """Write a complete article based on research.
        
        Args:
            topic: Article topic
            research_data: Research findings dictionary
            style: Writing style (e.g., "professional", "casual", "technical")
            target_audience: Target audience description
            
        Returns:
            Dictionary containing the article and metadata
        """
        self.logger.info(f"Writing article on: {topic}")
        
        # Extract research synthesis
        research_synthesis = research_data.get("synthesis", "")
        research_analysis = research_data.get("analysis", "")
        
        # Create style instructions
        style_instruction = ""
        if style:
            style_instruction += f"\nWriting Style: {style}"
        if target_audience:
            style_instruction += f"\nTarget Audience: {target_audience}"
        
        # Create outline
        outline = self.create_outline(topic, research_synthesis)
        
        # Generate full article
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=f"""You are a professional content writer. Write a comprehensive, engaging article based on the provided research and outline.

Requirements:
- Follow the outline structure
- Write 1200-1500 words
- Use clear, engaging language
- Include an introduction, body sections, and conclusion
- Add smooth transitions between sections
- Cite key facts and statistics when relevant
- Use markdown formatting (headers, bold, italics, lists)
- Make it informative yet accessible{style_instruction}"""),
            HumanMessage(content=f"Topic: {topic}\n\nOutline:\n{outline}\n\nResearch:\n{research_synthesis}\n\nAnalysis:\n{research_analysis}")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        article_content = response.content
        
        # Generate title
        title = self._extract_title(article_content) or f"A Comprehensive Guide to {topic}"
        
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
            "topic": topic
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
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="Generate a compelling meta description (150-160 characters) for this article."),
            HumanMessage(content=f"Topic: {topic}\n\nContent preview:\n{content[:500]}")
        ])
        
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
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="Generate 5-8 relevant tags for this article. Return only the tags, comma-separated."),
            HumanMessage(content=f"Topic: {topic}\n\nResearch: {research_data.get('synthesis', '')[:500]}")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        tags = [tag.strip() for tag in response.content.split(",")]
        
        return tags[:8]  # Limit to 8 tags
