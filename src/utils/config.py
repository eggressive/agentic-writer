"""Configuration management for the content creation agent."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv


class Config(BaseModel):
    """Configuration settings for the content creation agent."""

    openai_api_key: str = Field(default="")
    medium_access_token: Optional[str] = Field(default=None)
    unsplash_access_key: Optional[str] = Field(default=None)
    openai_model: str = Field(default="gpt-4-turbo-preview")
    temperature: float = Field(default=0.7)
    log_level: str = Field(default="INFO")
    max_research_sources: int = Field(default=5)
    max_retries: int = Field(default=3)
    unsplash_per_page: int = Field(default=10)
    unsplash_order_by: str = Field(default="relevant")
    unsplash_content_filter: str = Field(default="high")
    unsplash_orientation: str = Field(default="landscape")

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        load_dotenv()

        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            medium_access_token=os.getenv("MEDIUM_ACCESS_TOKEN"),
            unsplash_access_key=os.getenv("UNSPLASH_ACCESS_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            max_research_sources=int(os.getenv("MAX_RESEARCH_SOURCES", "5")),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            unsplash_per_page=int(os.getenv("UNSPLASH_PER_PAGE", "10")),
            unsplash_order_by=os.getenv("UNSPLASH_ORDER_BY", "relevant"),
            unsplash_content_filter=os.getenv("UNSPLASH_CONTENT_FILTER", "high"),
            unsplash_orientation=os.getenv("UNSPLASH_ORIENTATION", "landscape"),
        )

    def validate_required(self) -> None:
        """Validate that required API keys are present."""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required but not set")
