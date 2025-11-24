"""Configuration management for the content creation agent."""

import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator


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

    @field_validator("unsplash_per_page")
    @classmethod
    def validate_per_page(cls, v: int) -> int:
        """Validate unsplash_per_page is within valid range."""
        if not 1 <= v <= 30:
            raise ValueError("unsplash_per_page must be between 1 and 30")
        return v

    @field_validator("unsplash_order_by")
    @classmethod
    def validate_order_by(cls, v: str) -> str:
        """Validate unsplash_order_by has valid value."""
        if v not in ["relevant", "latest"]:
            raise ValueError("unsplash_order_by must be 'relevant' or 'latest'")
        return v

    @field_validator("unsplash_content_filter")
    @classmethod
    def validate_content_filter(cls, v: str) -> str:
        """Validate unsplash_content_filter has valid value."""
        if v not in ["low", "high"]:
            raise ValueError("unsplash_content_filter must be 'low' or 'high'")
        return v

    @field_validator("unsplash_orientation")
    @classmethod
    def validate_orientation(cls, v: str) -> str:
        """Validate unsplash_orientation has valid value."""
        if v not in ["landscape", "portrait", "squarish"]:
            raise ValueError(
                "unsplash_orientation must be 'landscape', 'portrait', or 'squarish'"
            )
        return v

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        load_dotenv()

        # Parse integer values with better error handling
        try:
            max_research_sources = int(os.getenv("MAX_RESEARCH_SOURCES", "5"))
        except ValueError as e:
            raise ValueError(
                "Invalid value for MAX_RESEARCH_SOURCES: must be an integer"
            ) from e

        try:
            max_retries = int(os.getenv("MAX_RETRIES", "3"))
        except ValueError as e:
            raise ValueError("Invalid value for MAX_RETRIES: must be an integer") from e

        try:
            unsplash_per_page = int(os.getenv("UNSPLASH_PER_PAGE", "10"))
        except ValueError as e:
            raise ValueError(
                "Invalid value for UNSPLASH_PER_PAGE: must be an integer"
            ) from e

        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            medium_access_token=os.getenv("MEDIUM_ACCESS_TOKEN"),
            unsplash_access_key=os.getenv("UNSPLASH_ACCESS_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            max_research_sources=max_research_sources,
            max_retries=max_retries,
            unsplash_per_page=unsplash_per_page,
            unsplash_order_by=os.getenv("UNSPLASH_ORDER_BY", "relevant"),
            unsplash_content_filter=os.getenv("UNSPLASH_CONTENT_FILTER", "high"),
            unsplash_orientation=os.getenv("UNSPLASH_ORIENTATION", "landscape"),
        )

    def validate_required(self) -> None:
        """Validate that required API keys are present."""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required but not set")
