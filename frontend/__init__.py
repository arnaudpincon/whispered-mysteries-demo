#!/usr/bin/env python3
"""UI package initialization for the detective game frontend - PHASE 5 VERSION"""

from .core.frontend_config import config, image_assets, text_assets
from .ui import InventoryHandler, create_game_facade
from .services.image_preloader import get_cache_stats, initialize_image_system
from .ui.css_styles import CSS_STYLES
from .ui.main_frontend import create_gradio_app
from .ui.response_handler import ResponseHandler

__all__ = [
    "create_gradio_app",
    "config",
    "image_assets",
    "text_assets",
    "InventoryHandler",
    "create_game_facade",
    "ResponseHandler",
    "CSS_STYLES",
    "initialize_image_system",
    "get_cache_stats",
]
