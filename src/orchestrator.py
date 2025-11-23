"""Main orchestrator for the content creation pipeline."""

import logging
from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI

from .agents import ResearchAgent, WriterAgent, ImageAgent, PublisherAgent
from .utils import Config


class ContentCreationOrchestrator:
    """Orchestrates the entire content creation workflow."""

    def __init__(self, config: Config):
        """Initialize the orchestrator.

        Args:
            config: Configuration object
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=config.openai_model,
            temperature=config.temperature,
            api_key=config.openai_api_key,
        )

        # Initialize agents
        self.research_agent = ResearchAgent(
            llm=self.llm, max_sources=config.max_research_sources
        )
        self.writer_agent = WriterAgent(llm=self.llm)
        self.image_agent = ImageAgent(
            llm=self.llm,
            unsplash_key=config.unsplash_access_key,
            per_page=config.unsplash_per_page,
            order_by=config.unsplash_order_by,
            content_filter=config.unsplash_content_filter,
            orientation=config.unsplash_orientation,
        )
        self.publisher_agent = PublisherAgent(medium_token=config.medium_access_token)

        self.logger.info("Content creation orchestrator initialized")

    def create_content(
        self,
        topic: str,
        style: Optional[str] = None,
        target_audience: Optional[str] = None,
        platforms: Optional[List[str]] = None,
        output_dir: str = "output",
    ) -> Dict[str, Any]:
        """Execute the full content creation pipeline.

        Args:
            topic: Topic to create content about
            style: Writing style preference
            target_audience: Target audience description
            platforms: List of platforms to publish to
            output_dir: Output directory for saving files

        Returns:
            Dictionary containing all results from the pipeline
        """
        if platforms is None:
            platforms = ["file"]

        self.logger.info(f"Starting content creation pipeline for topic: {topic}")

        results = {"topic": topic, "status": "in_progress", "stages": {}}

        try:
            # Stage 1: Research
            self.logger.info("Stage 1/4: Researching topic...")
            research_data = self.research_agent.research(topic)
            results["stages"]["research"] = {
                "status": "completed",
                "sources_count": research_data.get("sources_count", 0),
            }
            self.logger.info(
                f"Research completed with {research_data.get('sources_count', 0)} sources"
            )

            # Stage 2: Writing
            self.logger.info("Stage 2/4: Writing article...")
            article_data = self.writer_agent.write_article(
                topic=topic,
                research_data=research_data,
                style=style,
                target_audience=target_audience,
            )
            results["stages"]["writing"] = {
                "status": "completed",
                "title": article_data.get("title"),
                "word_count": article_data.get("word_count"),
            }
            self.logger.info(
                f"Article completed: {article_data.get('title')} ({article_data.get('word_count')} words)"
            )

            # Stage 3: Finding images
            self.logger.info("Stage 3/4: Finding relevant images...")
            images = self.image_agent.find_images(topic, article_data)
            article_data["images"] = images
            article_data["sources_count"] = research_data.get("sources_count", 0)
            results["stages"]["images"] = {
                "status": "completed",
                "images_found": len(images),
            }
            self.logger.info(f"Found {len(images)} relevant images")

            # Stage 4: Publishing
            self.logger.info("Stage 4/4: Publishing content...")
            publish_results = self.publisher_agent.publish(
                article_data=article_data, platforms=platforms, output_dir=output_dir
            )
            results["stages"]["publishing"] = {
                "status": "completed",
                "results": publish_results,
            }
            self.logger.info("Publishing completed")

            # Final results
            results["status"] = "completed"
            results["article"] = {
                "title": article_data.get("title"),
                "word_count": article_data.get("word_count"),
                "tags": article_data.get("tags"),
                "meta_description": article_data.get("meta_description"),
            }
            results["publication"] = publish_results

            self.logger.info(
                f"Content creation pipeline completed successfully for: {topic}"
            )

        except Exception as e:
            self.logger.error(f"Content creation pipeline failed: {str(e)}")
            results["status"] = "failed"
            results["error"] = str(e)
            raise

        return results

    def get_summary(self, results: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the results.

        Args:
            results: Results dictionary from create_content

        Returns:
            Formatted summary string
        """
        if results.get("status") != "completed":
            return f"Pipeline status: {results.get('status')}"

        article = results.get("article", {})
        stages = results.get("stages", {})

        summary = f"""
Content Creation Summary
========================

Topic: {results.get('topic')}
Status: {results.get('status')}

Article Details:
- Title: {article.get('title')}
- Word Count: {article.get('word_count')}
- Tags: {', '.join(article.get('tags', []))}

Pipeline Stages:
- Research: {stages.get('research', {}).get('sources_count', 0)} sources found
- Writing: Completed
- Images: {stages.get('images', {}).get('images_found', 0)} images found
- Publishing: Completed

Publication Results:
"""

        for platform, result in results.get("publication", {}).items():
            if result.get("success"):
                summary += f"- {platform.capitalize()}: Success"
                if "markdown_file" in result:
                    summary += f" (saved to {result['markdown_file']})"
                summary += "\n"
            else:
                summary += f"- {platform.capitalize()}: Failed ({result.get('error', 'Unknown error')})\n"

        return summary
