#!/usr/bin/env python3
"""Example script demonstrating the content creation agent."""

import os
from src.orchestrator import ContentCreationOrchestrator
from src.utils import Config, setup_logger


def main():
    """Run an example content creation workflow."""
    # Setup logging
    logger = setup_logger(level="INFO")

    print("=" * 60)
    print("Content Creation Agent - Example")
    print("=" * 60)

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not found in environment")
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("\nOr create a .env file based on .env.example")
        return

    try:
        # Load configuration
        print("\n📋 Loading configuration...")
        config = Config.from_env()
        config.validate_required()
        print("✅ Configuration loaded successfully")

        # Initialize orchestrator
        print("\n🤖 Initializing AI agents...")
        orchestrator = ContentCreationOrchestrator(config)
        print("✅ Agents ready")

        # Define topic
        topic = "The Impact of Artificial Intelligence on Modern Education"
        print(f"\n📝 Topic: {topic}")

        # Run content creation pipeline
        print("\n🚀 Starting content creation pipeline...")
        print("   This may take a few minutes...\n")

        results = orchestrator.create_content(
            topic=topic,
            style="professional",
            target_audience="educators and administrators",
            platforms=["file"],
            output_dir="output",
        )

        # Display results
        if results.get("status") == "completed":
            print("\n" + "=" * 60)
            print("✅ Content Creation Completed Successfully!")
            print("=" * 60)

            summary = orchestrator.get_summary(results)
            print(summary)

            # Publication details
            pub = results.get("publication", {})

            if "file" in pub and pub["file"].get("success"):
                md_file = pub["file"].get("markdown_file")
                print(f"\n📄 Article saved to: {md_file}")
                print(f"💾 Metadata saved to: {pub['file'].get('metadata_file')}")

            print("\n✨ You can now review and publish the article!")

        else:
            print(f"\n❌ Content creation failed: {results.get('error')}")

    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("Please check your .env file and ensure all required variables are set.")
    except Exception as e:
        logger.exception("An error occurred")
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
