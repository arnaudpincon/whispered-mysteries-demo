#!/usr/bin/env python3
"""
Static Map Generator
Uses a fixed image with hardcoded player positions
"""

# Fix Tkinter issues with PIL
import os
os.environ["PIL_DISABLE_TKINTER"] = "1"

from .static_map_service import (
    StaticMapService,
    get_static_map_service,
    generate_initial_map,
    update_map,
    validate_room_positions,
    debug_room_positions
)

# Export all functions for compatibility
__all__ = [
    "StaticMapService",
    "get_static_map_service", 
    "generate_initial_map",
    "update_map",
    "validate_room_positions",
    "debug_room_positions"
]