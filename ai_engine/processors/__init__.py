"""
AI Processors
Specialized processors for different AI operations in the detective game
"""

# Base processor
from .base_processor import BaseProcessor

# Specialized processors
from .command import CommandProcessor
from .character import CharacterProcessor
from .story import StoryProcessor
from .theory import TheoryProcessor

__all__ = [
    # Base
    'BaseProcessor',
    
    # Processors
    'CommandProcessor',
    'CharacterProcessor', 
    'StoryProcessor',
    'TheoryProcessor',
]