"""Research agent for gathering information on a given topic."""

import logging
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from duckduckgo_search import DDGS
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

    def synthesize_research(
        self, topic: str, search_results: List[Dict[str, Any]]
    ) -> str:
        """Synthesize research findings into a coherent summary.

        Args:
            topic: Original topic
            search_results: List of search results

        Returns:
            Synthesized research summary
        """
        self.logger.info(f"Synthesizing research for: {topic}")

        # Prepare search results text
        results_text = "\n\n".join(
            [
                f"Source {i+1}: {result.get('title', 'Unknown')}\n{result.get('body', '')}"
                for i, result in enumerate(search_results[: self.max_sources])
            ]
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are a research analyst. Synthesize the following search results into a comprehensive research summary.
Focus on:
1. Key facts and statistics
2. Different perspectives and viewpoints
3. Recent developments and trends
4. Important context and background

Provide a well-structured summary that will be useful for writing an article."""
                ),
                HumanMessage(
                    content=f"Topic: {topic}\n\nSearch Results:\n{results_text}"
                ),
            ]
        )

        response = self.llm.invoke(prompt.format_messages())

        return response.content

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

        # Synthesize findings
        if search_results:
            synthesis = self.synthesize_research(topic, search_results)
        else:
            synthesis = "No search results found. Proceeding with general knowledge."

        return {
            "topic": topic,
            "analysis": analysis["analysis"],
            "search_results": search_results,
            "synthesis": synthesis,
            "sources_count": len(search_results),
        }
