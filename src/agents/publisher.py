"""Publisher agent for publishing content to various platforms."""

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


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

    @staticmethod
    def _format_image_markdown(img: Dict[str, Any]) -> str:
        """Format a single image as markdown with attribution."""
        alt = img.get("description", "Image")
        url = img.get("url", "")
        author = img.get("author", "Unknown")
        author_url = img.get("author_url", "")
        source = img.get("source", "Unsplash")

        lines = [f"![{alt}]({url})"]
        if author_url:
            lines.append(f"*Photo by [{author}]({author_url}) on {source}*")
        else:
            lines.append(f"*Photo by {author} on {source}*")
        return "\n".join(lines)

    @staticmethod
    def _embed_images_in_content(
        content: str, images: List[Dict[str, Any]]
    ) -> str:
        """Embed images after the first paragraph of their assigned sections.

        Each image must have a 'section' key matching a ## heading in the
        content.  Images without a matching section are appended at the end.

        Args:
            content: Article markdown text
            images: Image dicts, each with a 'section' key

        Returns:
            Content string with images embedded inline
        """
        if not images:
            return content

        # Group images by their assigned section heading
        section_images: Dict[str, List[Dict[str, Any]]] = {}
        unplaced: List[Dict[str, Any]] = []
        for img in images:
            section = img.get("section")
            if section:
                section_images.setdefault(section, []).append(img)
            else:
                unplaced.append(img)

        if not section_images and not unplaced:
            return content

        # Split content into lines and rebuild with images inserted
        lines = content.split("\n")
        result_lines: List[str] = []
        current_heading: Optional[str] = None
        found_first_paragraph = False

        for line in lines:
            result_lines.append(line)

            # Detect ## headings
            heading_match = re.match(r"^##\s+(.+)$", line)
            if heading_match:
                current_heading = heading_match.group(1).strip()
                found_first_paragraph = False
                continue

            # After a heading, look for the end of the first paragraph
            # (a non-empty line followed by an empty line or another heading)
            if (
                current_heading
                and current_heading in section_images
                and not found_first_paragraph
            ):
                stripped = line.strip()
                # A blank line after we've seen content marks end of first paragraph
                if stripped == "" and len(result_lines) >= 2:
                    prev = result_lines[-2].strip() if len(result_lines) >= 2 else ""
                    if prev and not prev.startswith("#"):
                        found_first_paragraph = True
                        for img in section_images[current_heading]:
                            result_lines.append("")
                            result_lines.append(
                                PublisherAgent._format_image_markdown(img)
                            )
                        del section_images[current_heading]

        # Any images whose sections weren't found in the text, plus unplaced
        remaining = unplaced[:]
        for imgs in section_images.values():
            remaining.extend(imgs)

        if remaining:
            result_lines.append("")
            for img in remaining:
                result_lines.append("")
                result_lines.append(PublisherAgent._format_image_markdown(img))

        return "\n".join(result_lines)

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

                # Embed images within article sections instead of appending
                content = article_data.get("content", "")
                images = article_data.get("images", [])
                content = self._embed_images_in_content(content, images)
                f.write(content)

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
