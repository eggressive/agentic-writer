"""Research agent for gathering information on a given topic."""

import json
import logging
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from ddgs import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential


class ResearchAgent:
    """Agent responsible for researching topics and gathering information."""

    def __init__(self, llm: ChatOpenAI, max_sources: int = 5):
        """Initialize the research agent.

        Args:
            llm: Language model for processing research
            max_sources: Maximum number of sources to gather
        """
        self.llm = llm
        self.max_sources = max_sources
        self.logger = logging.getLogger(__name__)

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def search_web(self, query: str) -> List[Dict[str, Any]]:
        """Search the web for information on a topic.

        Args:
            query: Search query

        Returns:
            List of search results with title, body, and href
        """
        self.logger.info(f"Searching web for: {query}")

        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=self.max_sources))
                self.logger.info(f"Found {len(results)} search results")
                return results
        except Exception as e:
            self.logger.error(f"Web search failed: {str(e)}")
            return []

    def analyze_topic(self, topic: str) -> Dict[str, Any]:
        """Analyze a topic and generate research questions.

        Args:
            topic: Topic to analyze

        Returns:
            Dictionary with analysis and research questions
        """
        self.logger.info(f"Analyzing topic: {topic}")

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are a research assistant. Given a topic, analyze it and:
1. Identify key aspects to research
2. Generate 3-5 specific research questions
3. Suggest relevant subtopics
4. Determine the target audience

Return your analysis in a structured format."""
                ),
                HumanMessage(content=f"Topic: {topic}"),
            ]
        )

        response = self.llm.invoke(prompt.format_messages())

        return {"topic": topic, "analysis": response.content}

    def create_research_brief(
        self, angle: str, search_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a structured research brief from search results.

        Args:
            angle: Research angle/topic
            search_results: List of search results

        Returns:
            Dictionary containing structured research data
        """
        self.logger.info("Creating structured research brief...")

        # Prepare search results text
        results_text = "\n\n".join(
            [
                f"Source {i+1}: {result.get('title', 'Unknown')}\n{result.get('body', '')}"
                for i, result in enumerate(search_results[: self.max_sources])
            ]
        )

        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are a research analyst. From the provided text, extract the following information relevant to the research angle. Structure your output as a JSON object with the specified keys.

            - key_statistics: A list of 5-7 verifiable statistics with their sources.
            - expert_quotes: A list of 3-5 insightful quotes from named experts or publications.
            - case_studies: A list of 2-3 brief case studies of named companies or projects.
            - key_definitions: A dictionary of important terms and their definitions.
            - counter_arguments: A list of common counter-arguments or alternative viewpoints.

            Ensure all extracted data is directly relevant to the research angle.
            Return ONLY the JSON object, no additional text."""
                ),
                HumanMessage(
                    content=f"Research Angle: {angle}\n\nSearch Results:\n{results_text}"
                ),
            ]
        )

        response = self.llm.invoke(prompt_template.format_messages())

        # Parse the JSON output
        try:
            brief = json.loads(response.content)
            brief["raw_sources"] = search_results  # Keep raw sources for citation
            return brief
        except json.JSONDecodeError:
            self.logger.error("Failed to parse research brief JSON")
            return {
                "key_statistics": [],
                "expert_quotes": [],
                "case_studies": [],
                "key_definitions": {},
                "counter_arguments": [],
                "raw_sources": search_results,
            }

    def research(self, topic: str) -> Dict[str, Any]:
        """Conduct full research on a topic.

        Args:
            topic: Topic to research

        Returns:
            Dictionary containing research findings
        """
        self.logger.info(f"Starting research on: {topic}")

        # Analyze the topic
        analysis = self.analyze_topic(topic)

        # Search for information
        search_results = self.search_web(topic)

        # Create structured research brief
        if search_results:
            research_brief = self.create_research_brief(topic, search_results)
        else:
            research_brief = {
                "key_statistics": [],
                "expert_quotes": [],
                "case_studies": [],
                "key_definitions": {},
                "counter_arguments": [],
                "raw_sources": [],
            }

        return {
            "topic": topic,
            "analysis": analysis["analysis"],
            "search_results": search_results,
            "research_brief": research_brief,
            "sources_count": len(search_results),
        }
