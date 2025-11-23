"""Publisher agent for publishing content to various platforms."""

import logging
from typing import Dict, Any, Optional
import json
from pathlib import Path


class PublisherAgent:
    """Agent responsible for publishing content to platforms."""

    def __init__(self, medium_token: Optional[str] = None):
        """Initialize the publisher agent.

        Args:
            medium_token: Optional Medium API token
        """
        self.medium_token = medium_token
        self.logger = logging.getLogger(__name__)

    def publish_to_medium(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Publish article to Medium.

        Args:
            article_data: Article data including title and content

        Returns:
            Publication result
        """
        if not self.medium_token:
            self.logger.warning(
                "Medium token not provided, skipping Medium publication"
            )
            return {
                "success": False,
                "platform": "medium",
                "error": "Medium API token not configured",
            }

        try:
            # Note: Actual Medium API implementation would go here
            # For now, we'll simulate the publication
            self.logger.info(f"Publishing to Medium: {article_data.get('title')}")

            # In a real implementation, you would:
            # 1. Use the Medium API to create a post
            # 2. Upload images
            # 3. Add tags
            # 4. Set publication status

            self.logger.info("Medium publication simulated (API implementation needed)")

            return {
                "success": True,
                "platform": "medium",
                "message": "Article ready for Medium publication (API token required for actual publishing)",
                "url": "https://medium.com/@your-username/your-article",
            }

        except Exception as e:
            self.logger.error(f"Medium publication failed: {str(e)}")
            return {"success": False, "platform": "medium", "error": str(e)}

    def save_to_file(
        self, article_data: Dict[str, Any], output_dir: str = "output"
    ) -> Dict[str, Any]:
        """Save article to file system.

        Args:
            article_data: Article data
            output_dir: Output directory path

        Returns:
            Save result
        """
        try:
            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # Generate filename from title
            title = article_data.get("title", "untitled")
            filename = "".join(
                c if c.isalnum() or c in (" ", "-") else "_" for c in title
            )
            filename = filename.replace(" ", "_").lower()[:50]

            # Save markdown file
            md_file = output_path / f"{filename}.md"
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(f"# {article_data.get('title', 'Untitled')}\n\n")
                f.write(f"**Topic:** {article_data.get('topic', 'N/A')}\n\n")
                f.write(f"**Word Count:** {article_data.get('word_count', 0)}\n\n")
                f.write(f"**Tags:** {', '.join(article_data.get('tags', []))}\n\n")
                f.write(
                    f"**Meta Description:** {article_data.get('meta_description', '')}\n\n"
                )
                f.write("---\n\n")
                f.write(article_data.get("content", ""))

                # Add images if available
                images = article_data.get("images", [])
                if images:
                    f.write("\n\n## Visuals\n\n")
                    for img in images:
                        alt = img.get("description", "Image")
                        url = img.get("url", "")
                        author = img.get("author", "Unknown")
                        author_url = img.get("author_url", "")
                        source = img.get("source", "Unsplash")

                        f.write(f"![{alt}]({url})\n")
                        if author_url:
                            f.write(
                                f"*Photo by [{author}]({author_url}) on {source}*\n\n"
                            )
                        else:
                            f.write(f"*Photo by {author} on {source}*\n\n")

            # Save metadata JSON
            json_file = output_path / f"{filename}_metadata.json"
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "title": article_data.get("title"),
                        "topic": article_data.get("topic"),
                        "word_count": article_data.get("word_count"),
                        "tags": article_data.get("tags"),
                        "meta_description": article_data.get("meta_description"),
                        "images": article_data.get("images", []),
                        "sources_count": article_data.get("sources_count", 0),
                    },
                    f,
                    indent=2,
                )

            self.logger.info(f"Article saved to: {md_file}")

            return {
                "success": True,
                "platform": "file",
                "markdown_file": str(md_file),
                "metadata_file": str(json_file),
            }

        except Exception as e:
            self.logger.error(f"File save failed: {str(e)}")
            return {"success": False, "platform": "file", "error": str(e)}

    def publish(
        self,
        article_data: Dict[str, Any],
        platforms: list = None,
        output_dir: str = "output",
    ) -> Dict[str, Any]:
        """Publish article to specified platforms.

        Args:
            article_data: Article data
            platforms: List of platforms to publish to (default: ["file"])
            output_dir: Output directory for file-based publishing

        Returns:
            Dictionary with publication results for each platform
        """
        if platforms is None:
            platforms = ["file"]

        results = {}

        for platform in platforms:
            if platform.lower() == "medium":
                results["medium"] = self.publish_to_medium(article_data)
            elif platform.lower() == "file":
                results["file"] = self.save_to_file(article_data, output_dir)
            else:
                self.logger.warning(f"Unknown platform: {platform}")
                results[platform] = {
                    "success": False,
                    "platform": platform,
                    "error": f"Platform '{platform}' not supported",
                }

        return results
