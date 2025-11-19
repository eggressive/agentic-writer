"""Image handler agent for finding and managing images."""

import logging
from typing import List, Dict, Any, Optional
import requests
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage


class ImageAgent:
    """Agent responsible for finding and selecting relevant images."""

    def __init__(self, llm: ChatOpenAI, unsplash_key: Optional[str] = None):
        """Initialize the image agent.
        
        Args:
            llm: Language model for image selection
            unsplash_key: Optional Unsplash API key
        """
        self.llm = llm
        self.unsplash_key = unsplash_key
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
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an image curator. Generate 3-5 specific image search queries that would find relevant, high-quality images for this article.
The queries should be:
- Specific and descriptive
- Relevant to the main topic
- Suitable for professional content
- Diverse (different aspects of the topic)

Return only the queries, one per line."""),
            HumanMessage(content=f"Topic: {topic}\n\nArticle preview:\n{article_content[:1000]}")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        queries = [q.strip() for q in response.content.split("\n") if q.strip()]
        
        return queries[:5]

    def search_unsplash(self, query: str, per_page: int = 5) -> List[Dict[str, Any]]:
        """Search Unsplash for images.
        
        Args:
            query: Search query
            per_page: Number of results per page
            
        Returns:
            List of image metadata
        """
        if not self.unsplash_key:
            self.logger.warning("Unsplash API key not provided, skipping image search")
            return []
        
        try:
            url = "https://api.unsplash.com/search/photos"
            headers = {"Authorization": f"Client-ID {self.unsplash_key}"}
            params = {"query": query, "per_page": per_page, "orientation": "landscape"}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            results = response.json().get("results", [])
            
            images = []
            for result in results:
                images.append({
                    "id": result["id"],
                    "url": result["urls"]["regular"],
                    "thumb_url": result["urls"]["thumb"],
                    "description": result.get("description") or result.get("alt_description", ""),
                    "author": result["user"]["name"],
                    "author_url": result["user"]["links"]["html"],
                    "download_url": result["links"]["download"],
                    "width": result["width"],
                    "height": result["height"]
                })
            
            self.logger.info(f"Found {len(images)} images for query: {query}")
            return images
            
        except Exception as e:
            self.logger.error(f"Unsplash search failed: {str(e)}")
            return []

    def find_images(self, topic: str, article_data: Dict[str, Any]) -> List[Dict[str, Any]]:
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
            images = self.search_unsplash(query)
            all_images.extend(images)
        
        # Select best images
        selected_images = self.select_best_images(topic, article_data, all_images)
        
        return selected_images

    def select_best_images(
        self,
        topic: str,
        article_data: Dict[str, Any],
        available_images: List[Dict[str, Any]]
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
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an image curator. Suggest 3 specific images that would be ideal for this article.
For each image, describe:
- What the image should show
- Why it's relevant
- Suggested placement in the article

Format each suggestion as:
Image N: [Description]
Why: [Relevance]
Placement: [Where in article]"""),
            HumanMessage(content=f"Topic: {topic}\n\nArticle:\n{article_content[:1500]}")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        
        return response.content.split("\n\n")
