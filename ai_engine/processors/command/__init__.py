"""
Command Processing Module - Refactored for Clean Architecture

Main exports for backward compatibility and new features.
"""

# Main processor (backward compatibility)
from .processor import CommandProcessor

# Advanced components (for extensions)
from .factory import CommandComponentFactory
from .interfaces import (
    ICommandAnalyzer,
    ICommandExecutor,
    INonsenseHandler
)

# Individual components (for custom setups)
from .command_analyzer import CommandAnalyzer
from .command_executor import CommandExecutor
from .nonsense_handler import NonsenseHandler

__all__ = [
    # Main interface (same as before)
    'CommandProcessor',
    
    # Factory for custom setups
    'CommandComponentFactory',
    
    # Interfaces for custom implementations
    'ICommandAnalyzer',
    'ICommandExecutor',
    'INonsenseHandler',
    
    # Individual components
    'CommandAnalyzer',
    'CommandExecutor',
    'NonsenseHandler',
]