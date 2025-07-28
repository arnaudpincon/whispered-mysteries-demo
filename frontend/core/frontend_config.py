#!/usr/bin/env python3
"""Configuration management for the frontend - Updated with image preloader"""
import os
from typing import Any, Dict

from dotenv import load_dotenv
from PIL import Image

from utils.markdown_utils import read_markdown_file

from ..services.image_preloader import image_cache, initialize_image_system

load_dotenv()


class Config:
    """Centralized configuration class"""

    def __init__(self):
        # Environment variables
        self.azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.azure_openai_deployment_name: str = os.getenv(
            "AZURE_OPENAI_DEPLOYMENT_NAME", ""
        )
        self.api_version: str = os.getenv("API_VERSION", "")
        self.dev_mode: str = os.getenv("DEV_MODE", "")

    def get_openai_config(self) -> Dict[str, Any]:
        """Get OpenAI configuration dictionary"""
        return {
            "api_key": self.azure_openai_api_key,
            "endpoint": self.azure_openai_endpoint,
            "deployment_name": self.azure_openai_deployment_name,
            "api_version": self.api_version,
            "dev_mode": self.dev_mode,
        }


class ImageAssets:
    """Manage all image assets using the preloader system"""

    def __init__(self):
        # Initialize the preloader system
        initialize_image_system()

        # Properties for easy access to common images
        self.character_image: Image.Image = image_cache.get_special_image("character")
        self.room_image: Image.Image = image_cache.get_special_image("room")
        self.intro_image: Image.Image = image_cache.get_special_image("intro")
        self.confrontation_image: Image.Image = image_cache.get_special_image(
            "confrontation"
        )

    def get_ending_image(self, ending_type: int) -> Image.Image:
        """Get appropriate ending image based on ending type"""
        return image_cache.get_ending_image(ending_type)

    def load_character_image(self, image_url: str) -> Image.Image:
        """Load character image with fallback - now uses preloader"""
        return image_cache.get_character_image(image_url)

    def load_room_image(self, image_url: str) -> Image.Image:
        """Load room image with fallback - now uses preloader"""
        return image_cache.get_room_image(image_url)

    def get_cache_stats(self) -> Dict[str, int]:
        """Get image cache statistics for debugging"""
        return image_cache.get_cache_stats()


class TextAssets:
    """Manage all text assets"""

    def __init__(self):
        self.rules_text: str = read_markdown_file("data/narratives/documents/rules_short.md")


# Global instances
config = Config()
image_assets = ImageAssets()
text_assets = TextAssets()
