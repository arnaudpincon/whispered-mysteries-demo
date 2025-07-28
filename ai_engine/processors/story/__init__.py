"""
Story Processing Module - Refactored for Clean Architecture

Main exports for backward compatibility and new features.
"""

# Main processor (backward compatibility)
from .processor import StoryProcessor

# Advanced components (for extensions)
from .factory import StoryComponentFactory
from .interfaces import (
    IRoomDescriptionGenerator,
    ICharacterDescriptionGenerator,
    IClueAnalyzer,
    IObjectInspector
)

# Individual components (for custom setups)
from .room_description import RoomDescriptionGenerator
from .character_description import CharacterDescriptionGenerator
from .clue_analyzer import ClueAnalyzer
from .object_inspector import ObjectInspector

__all__ = [
    # Main interface (same as before)
    'StoryProcessor',
    
    # Factory for custom setups
    'StoryComponentFactory',
    
    # Interfaces for custom implementations
    'IRoomDescriptionGenerator',
    'ICharacterDescriptionGenerator',
    'IClueAnalyzer',
    'IObjectInspector',
    
    # Individual components
    'RoomDescriptionGenerator',
    'CharacterDescriptionGenerator',
    'ClueAnalyzer',
    'ObjectInspector',
]