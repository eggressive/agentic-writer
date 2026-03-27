"""Publisher agent for publishing content to various platforms."""

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class PublisherAgent:
    """Agent responsible for publishing content to platforms."""

    def __init__(
        self,
        medium_token: Optional[str] = None,
        ghost_api_url: Optional[str] = None,
        ghost_admin_api_key: Optional[str] = None,
        wordpress_url: Optional[str] = None,
        wordpress_username: Optional[str] = None,
        wordpress_app_password: Optional[str] = None,
        hashnode_api_key: Optional[str] = None,
        hashnode_publication_id: Optional[str] = None,
    ):
        """Initialize the publisher agent.

        Args:
            medium_token: Optional Medium API token
            ghost_api_url: Optional Ghost blog base URL (e.g. https://myblog.ghost.io)
            ghost_admin_api_key: Optional Ghost Admin API key (id:secret format)
            wordpress_url: Optional WordPress site URL
            wordpress_username: Optional WordPress username
            wordpress_app_password: Optional WordPress application password
            hashnode_api_key: Optional Hashnode personal API key
            hashnode_publication_id: Optional Hashnode publication/blog ID
        """
        self.medium_token = medium_token
        self.ghost_api_url = ghost_api_url
        self.ghost_admin_api_key = ghost_admin_api_key
        self.wordpress_url = wordpress_url
        self.wordpress_username = wordpress_username
        self.wordpress_app_password = wordpress_app_password
        self.hashnode_api_key = hashnode_api_key
        self.hashnode_publication_id = hashnode_publication_id
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

    def publish_to_ghost(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Publish article to Ghost.

        Uses the Ghost Admin API (POST /ghost/api/admin/posts/).
        Requires a Ghost Admin API key in ``id:secret`` format.

        Args:
            article_data: Article data including title and content

        Returns:
            Publication result
        """
        if not self.ghost_api_url or not self.ghost_admin_api_key:
            self.logger.warning(
                "Ghost credentials not provided, skipping Ghost publication"
            )
            return {
                "success": False,
                "platform": "ghost",
                "error": "Ghost API URL and Admin API key are required",
            }

        # Validate id:secret format early to avoid confusing failures later
        key_parts = self.ghost_admin_api_key.split(":")
        if len(key_parts) != 2 or not key_parts[0] or not key_parts[1]:
            return {
                "success": False,
                "platform": "ghost",
                "error": "Ghost Admin API key must be in 'id:secret' format",
            }

        try:
            # Real implementation would:
            # 1. Split ghost_admin_api_key into id:secret
            # 2. Create a JWT token signed with the secret (HS256, 5-min expiry)
            # 3. POST to {ghost_api_url}/ghost/api/admin/posts/ with
            #    Authorization: Ghost {jwt} and the post payload
            self.logger.info(f"Publishing to Ghost: {article_data.get('title')}")
            self.logger.info(
                "Ghost publication simulated (JWT + API implementation needed)"
            )

            return {
                "success": False,
                "platform": "ghost",
                "error": "Ghost publication not implemented: simulated only (no API call performed)",
            }

        except Exception as e:
            self.logger.error(f"Ghost publication failed: {str(e)}")
            return {"success": False, "platform": "ghost", "error": str(e)}

    def publish_to_wordpress(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Publish article to WordPress via the REST API.

        Uses Basic Auth with an application password
        (POST /wp-json/wp/v2/posts).

        Args:
            article_data: Article data including title and content

        Returns:
            Publication result
        """
        if (
            not self.wordpress_url
            or not self.wordpress_username
            or not self.wordpress_app_password
        ):
            self.logger.warning(
                "WordPress credentials not provided, skipping WordPress publication"
            )
            return {
                "success": False,
                "platform": "wordpress",
                "error": "WordPress URL, username, and application password are required",
            }

        try:
            # Real implementation would:
            # 1. Base64-encode "username:app_password" for Basic Auth header
            # 2. POST to {wordpress_url}/wp-json/wp/v2/posts with
            #    title, content (HTML), tags, status="publish"
            self.logger.info(f"Publishing to WordPress: {article_data.get('title')}")
            self.logger.info(
                "WordPress publication simulated (REST API implementation needed)"
            )

            return {
                "success": False,
                "platform": "wordpress",
                "error": "WordPress publication not implemented: REST API call is currently simulated only",
            }

        except Exception as e:
            self.logger.error(f"WordPress publication failed: {str(e)}")
            return {"success": False, "platform": "wordpress", "error": str(e)}

    def publish_to_hashnode(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Publish article to Hashnode via the GraphQL API.

        Uses the ``publishPost`` mutation with a personal API key.

        Args:
            article_data: Article data including title and content

        Returns:
            Publication result
        """
        if not self.hashnode_api_key or not self.hashnode_publication_id:
            self.logger.warning(
                "Hashnode credentials not provided, skipping Hashnode publication"
            )
            return {
                "success": False,
                "platform": "hashnode",
                "error": "Hashnode API key and publication ID are required",
            }

        try:
            # Real implementation would:
            # 1. Send POST to https://gql.hashnode.com with
            #    Authorization: {hashnode_api_key} header
            # 2. GraphQL mutation publishPost with title, contentMarkdown,
            #    publicationId, and tags
            self.logger.info(f"Publishing to Hashnode: {article_data.get('title')}")
            self.logger.info(
                "Hashnode publication simulated (GraphQL API implementation needed)"
            )

            return {
                "success": False,
                "platform": "hashnode",
                "error": "Hashnode publication not implemented: GraphQL API call is currently simulated only",
            }

        except Exception as e:
            self.logger.error(f"Hashnode publication failed: {str(e)}")
            return {"success": False, "platform": "hashnode", "error": str(e)}

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
    def _embed_images_in_content(content: str, images: List[Dict[str, Any]]) -> str:
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
            elif platform.lower() == "ghost":
                results["ghost"] = self.publish_to_ghost(article_data)
            elif platform.lower() == "wordpress":
                results["wordpress"] = self.publish_to_wordpress(article_data)
            elif platform.lower() == "hashnode":
                results["hashnode"] = self.publish_to_hashnode(article_data)
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
