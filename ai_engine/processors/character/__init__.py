"""
Character Processing Module - Refactored for Clean Architecture

Main exports for backward compatibility and new features.
"""

# Main processor (backward compatibility)
from .processor import CharacterProcessor

# Advanced components (for extensions)
from .factory import ConversationComponentFactory
from .interfaces import (
    IConversationHandler,
    IPersonalityEngine, 
    IMemoryManager,
    ILoreRetriever
)

# Error handling
from .errors import (
    ConversationError,
    ConversationErrorHandler,
    ConversationResponseFormatter,
    ConversationValidator
)

__all__ = [
    # Main interface (same as before)
    'CharacterProcessor',
    
    # Factory for custom setups
    'ConversationComponentFactory',
    
    # Interfaces for custom implementations
    'IConversationHandler',
    'IPersonalityEngine', 
    'IMemoryManager',
    'ILoreRetriever',
    
    # Error handling utilities
    'ConversationError',
    'ConversationErrorHandler',
    'ConversationResponseFormatter',
    'ConversationValidator',
]
