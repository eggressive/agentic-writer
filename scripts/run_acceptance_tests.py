"""
Script to run acceptance tests for Agentic Writer.
Generates real articles using the OpenAI API to verify quality across different styles and audiences.
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator import ContentCreationOrchestrator
from src.utils.config import Config
from src.utils.logger import setup_logger


def run_acceptance_tests():
    """Run a set of acceptance tests with real API calls."""

    # Setup
    logger = setup_logger(name="acceptance_tests", level="INFO")

    try:
        config = Config.from_env()
        config.validate_required()
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please ensure .env file is set up with OPENAI_API_KEY")
        return

    output_base = "output/acceptance_tests"
    os.makedirs(output_base, exist_ok=True)

    # Test Matrix (Subset for cost/time efficiency)
    tests = [
        {
            "topic": "The Future of Remote Work",
            "style": "Professional",
            "audience": "Business Executives",
        },
        {
            "topic": "How Neural Networks Work",
            "style": "Casual",
            "audience": "High School Students",
        },
        {
            "topic": "Rust vs C++ for Systems Programming",
            "style": "Technical",
            "audience": "Software Engineers",
        },
    ]

    logger.info(f"Starting acceptance tests. Output directory: {output_base}")

    for i, test in enumerate(tests, 1):
        logger.info(f"\n--- Running Test {i}/{len(tests)} ---")
        logger.info(f"Topic: {test['topic']}")
        logger.info(f"Style: {test['style']}")
        logger.info(f"Audience: {test['audience']}")

        orchestrator = ContentCreationOrchestrator(config)

        # Create a specific subfolder for this test run to keep things organized
        # or just use the base folder. Let's use the base folder but prefix filenames?
        # The orchestrator handles filenames based on topic.

        results = orchestrator.create_content(
            topic=test["topic"],
            style=test["style"],
            target_audience=test["audience"],
            platforms=["file"],
            output_dir=output_base,
        )

        if results["status"] == "completed":
            logger.info(f"✅ Test {i} Passed")
            article = results.get("article", {})
            logger.info(f"Title: {article.get('title')}")
            logger.info(f"Word Count: {article.get('word_count')}")
        else:
            logger.error(f"❌ Test {i} Failed")
            logger.error(results.get("error"))

    logger.info(f"\nAll tests completed. Check {output_base} for results.")


if __name__ == "__main__":
    run_acceptance_tests()
