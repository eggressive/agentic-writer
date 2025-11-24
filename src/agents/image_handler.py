"""Image handler agent for finding and managing images."""

import logging
from typing import Any, Dict, List, Optional

import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Unsplash API constants
UNSPLASH_MAX_PER_PAGE = 30


class ImageAgent:
    """Agent responsible for finding and selecting relevant images."""

    def __init__(
        self,
        llm: ChatOpenAI,
        unsplash_key: Optional[str] = None,
        per_page: int = 10,
        order_by: str = "relevant",
        content_filter: str = "high",
        orientation: str = "landscape",
    ):
        """Initialize the image agent.

        Args:
            llm: Language model for image selection
            unsplash_key: Optional Unsplash API key
            per_page: Number of images per search query (default: 10, max: 30)
            order_by: Sort order - "relevant" or "latest" (default: "relevant")
            content_filter: Content filtering level - "low" or "high" (default: "high")
            orientation: Image orientation - "landscape", "portrait", or "squarish" (default: "landscape")
        """
        # Validate parameters
        if not 1 <= per_page <= UNSPLASH_MAX_PER_PAGE:
            raise ValueError(
                f"per_page must be between 1 and {UNSPLASH_MAX_PER_PAGE}, got {per_page}"
            )
        if order_by not in ["relevant", "latest"]:
            raise ValueError(
                f"order_by must be 'relevant' or 'latest', got '{order_by}'"
            )
        if content_filter not in ["low", "high"]:
            raise ValueError(
                f"content_filter must be 'low' or 'high', got '{content_filter}'"
            )
        if orientation not in ["landscape", "portrait", "squarish"]:
            raise ValueError(
                f"orientation must be 'landscape', 'portrait', or 'squarish', got '{orientation}'"
            )

        self.llm = llm
        self.unsplash_key = unsplash_key
        self.per_page = per_page
        self.order_by = order_by
        self.content_filter = content_filter
        self.orientation = orientation
        self.logger = logging.getLogger(__name__)

    def generate_image_queries(self, topic: str, article_content: str) -> List[str]:
        """Generate search queries for finding relevant images.

        Args:
            topic: Article topic
            article_content: Full article content

        Returns:
            List of image search queries
        """
        self.logger.info(f"Generating image queries for: {topic}")

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are an image curator. Generate 3-5 specific image search queries that would find relevant, high-quality images for this article.
The queries should be:
- Specific and descriptive
- Relevant to the main topic
- Suitable for professional content
- Diverse (different aspects of the topic)

Return only the queries, one per line."""
                ),
                HumanMessage(
                    content=f"Topic: {topic}\n\nArticle preview:\n{article_content[:1000]}"
                ),
            ]
        )

        response = self.llm.invoke(prompt.format_messages())
        queries = [q.strip() for q in response.content.split("\n") if q.strip()]

        return queries[:5]

    def search_unsplash(
        self,
        query: str,
        per_page: int = 5,
        order_by: str = "relevant",
        content_filter: str = "high",
        color: Optional[str] = None,
        orientation: str = "landscape",
    ) -> List[Dict[str, Any]]:
        """Search Unsplash for images.

        Args:
            query: Search query
            per_page: Number of results per page (max 30)
            order_by: Sort order - "relevant" (default) or "latest"
            content_filter: Content filtering level - "low" or "high" (default)
            color: Optional color filter. Valid values: "black_and_white", "black", "white", "yellow", "orange", "red", "purple", "magenta", "green", "teal", "blue"
            orientation: Image orientation - "landscape" (default), "portrait", or "squarish"

        Returns:
            List of image metadata
        """
        if not self.unsplash_key:
            self.logger.warning("Unsplash API key not provided, skipping image search")
            return []

        try:
            url = "https://api.unsplash.com/search/photos"
            headers = {"Authorization": f"Client-ID {self.unsplash_key}"}
            params = {
                "query": query,
                "per_page": min(per_page, UNSPLASH_MAX_PER_PAGE),
                "order_by": order_by,
                "content_filter": content_filter,
                "orientation": orientation,
            }

            # Add optional color filter
            if color:
                params["color"] = color

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            results = response.json().get("results", [])

            images = []
            for result in results:
                images.append(
                    {
                        "id": result["id"],
                        "url": result["urls"]["regular"],
                        "thumb_url": result["urls"]["thumb"],
                        "full_url": result["urls"]["full"],
                        "description": result.get("description")
                        or result.get("alt_description", ""),
                        "author": result["user"]["name"],
                        "author_url": result["user"]["links"]["html"],
                        "download_url": result["links"]["download"],
                        "download_location": result["links"]["download_location"],
                        "photo_link": result["links"]["html"],
                        "width": result["width"],
                        "height": result["height"],
                        "color": result.get("color", ""),
                        "likes": result.get("likes", 0),
                        "tags": [
                            tag.get("title", "") for tag in result.get("tags", [])
                        ],
                    }
                )

            self.logger.info(f"Found {len(images)} images for query: {query}")
            return images

        except requests.exceptions.HTTPError as e:
            self.logger.error(f"Unsplash API HTTP error: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Unsplash search failed: {str(e)}")
            return []

    def track_download(self, download_location: str) -> bool:
        """Track image download with Unsplash API as required by guidelines.

        Args:
            download_location: The download_location URL from the photo object

        Returns:
            True if tracking was successful, False otherwise
        """
        if not self.unsplash_key:
            self.logger.info(
                "Unsplash API key not configured, download tracking skipped (optional feature)"
            )
            return False

        try:
            headers = {"Authorization": f"Client-ID {self.unsplash_key}"}
            response = requests.get(download_location, headers=headers, timeout=10)
            response.raise_for_status()
            self.logger.debug(f"Download tracked successfully for: {download_location}")
            return True
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error tracking download: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to track download: {str(e)}")
            return False

    def find_images(
        self, topic: str, article_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Find relevant images for an article.

        Args:
            topic: Article topic
            article_data: Article data including content

        Returns:
            List of recommended images
        """
        self.logger.info(f"Finding images for: {topic}")

        # Generate search queries
        queries = self.generate_image_queries(topic, article_data.get("content", ""))

        # Search for images
        all_images = []
        for query in queries:
            images = self.search_unsplash(
                query,
                per_page=self.per_page,
                order_by=self.order_by,
                content_filter=self.content_filter,
                orientation=self.orientation,
            )
            all_images.extend(images)

        # Select best images
        selected_images = self.select_best_images(topic, article_data, all_images)

        # Track downloads for selected images (required by Unsplash API guidelines)
        for image in selected_images:
            if "download_location" in image:
                self.track_download(image["download_location"])

        return selected_images

    def select_best_images(
        self,
        topic: str,
        article_data: Dict[str, Any],
        available_images: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Select the best images from available options.

        Args:
            topic: Article topic
            article_data: Article data
            available_images: List of available images

        Returns:
            List of selected images
        """
        if not available_images:
            self.logger.warning("No images available to select from")
            return []

        # If we have API access, just return top 3 diverse images
        if self.unsplash_key:
            # Take up to 3 images, ensuring diversity
            selected = []
            seen_authors = set()

            for img in available_images:
                if len(selected) >= 3:
                    break
                if img["author"] not in seen_authors:
                    selected.append(img)
                    seen_authors.add(img["author"])

            # Fill remaining slots if needed
            for img in available_images:
                if len(selected) >= 3:
                    break
                if img not in selected:
                    selected.append(img)

            return selected

        return []

    def generate_image_suggestions(self, topic: str, article_content: str) -> List[str]:
        """Generate suggestions for images when API is not available.

        Args:
            topic: Article topic
            article_content: Article content

        Returns:
            List of image suggestions
        """
        self.logger.info(f"Generating image suggestions for: {topic}")

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are an image curator. Suggest 3 specific images that would be ideal for this article.
For each image, describe:
- What the image should show
- Why it's relevant
- Suggested placement in the article

Format each suggestion as:
Image N: [Description]
Why: [Relevance]
Placement: [Where in article]"""
                ),
                HumanMessage(
                    content=f"Topic: {topic}\n\nArticle:\n{article_content[:1500]}"
                ),
            ]
        )

        response = self.llm.invoke(prompt.format_messages())

        return response.content.split("\n\n")
