"""Research agent for gathering information on a given topic."""

import json
import logging
from typing import Any, Dict, List

from ddgs import DDGS
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
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

    def _get_empty_research_brief(
        self, search_results: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Return an empty research brief structure.

        Args:
            search_results: Optional list of search results to include

        Returns:
            Dictionary with empty research brief structure
        """
        return {
            "key_statistics": [],
            "expert_quotes": [],
            "case_studies": [],
            "key_definitions": {},
            "counter_arguments": [],
            "raw_sources": search_results or [],
        }

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
                f"Source {i + 1}: {result.get('title', 'Unknown')}\n{result.get('body', '')}"
                for i, result in enumerate(search_results[: self.max_sources])
            ]
        )

        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are a research analyst. From the provided text, extract the following information relevant to the research angle. Structure your output as a JSON object with the specified keys and formats.

- key_statistics: A list of 5-7 strings. Each string should state a verifiable statistic and include its source inline, e.g., "80% of companies use AI for automation (McKinsey, 2023)".
- expert_quotes: A list of 3-5 strings. Each string should be a quote with attribution, e.g., "\"AI will transform every industry.\" — Sundar Pichai, Google CEO".
- case_studies: A list of 2-3 strings. Each string should briefly describe a named company or project and its relevance.
- key_definitions: A dictionary where each key is an important term and each value is its definition.
- counter_arguments: A list of strings, each describing a common counter-argument or alternative viewpoint.

Ensure all extracted data is directly relevant to the research angle.

Output format example:
{
  "key_statistics": [
    "80% of companies use AI for automation (McKinsey, 2023)",
    "Global AI market expected to reach $190B by 2025 (Statista, 2022)"
  ],
  "expert_quotes": [
    "\"AI will transform every industry.\" — Sundar Pichai, Google CEO",
    "\"Ethical AI is essential for trust.\" — Fei-Fei Li, Stanford"
  ],
  "case_studies": [
    "Netflix uses machine learning to personalize recommendations, increasing user engagement.",
    "Siemens implemented AI-driven predictive maintenance, reducing downtime by 30%."
  ],
  "key_definitions": {
    "Machine Learning": "A subset of AI focused on algorithms that improve through experience.",
    "Neural Network": "A computational model inspired by the human brain's network of neurons."
  },
  "counter_arguments": [
    "AI adoption may lead to significant job displacement.",
    "Bias in AI systems can perpetuate social inequalities."
  ]
}

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
            if not isinstance(brief, dict):
                self.logger.error(
                    "Research brief JSON is not an object, falling back to empty brief"
                )
                return self._get_empty_research_brief(search_results)
            brief["raw_sources"] = search_results  # Keep raw sources for citation
            return brief
        except json.JSONDecodeError:
            self.logger.error("Failed to parse research brief JSON")
            return self._get_empty_research_brief(search_results)

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
            research_brief = self._get_empty_research_brief()

        return {
            "topic": topic,
            "analysis": analysis["analysis"],
            "search_results": search_results,
            "research_brief": research_brief,
            "sources_count": len(search_results),
        }
