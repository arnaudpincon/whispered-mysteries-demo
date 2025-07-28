"""
Theory Processing Module - Refactored for Clean Architecture

Main exports for backward compatibility and new features.
"""

# Main processor (backward compatibility)
from .processor import TheoryProcessor

# Advanced components (for extensions)
from .factory import TheoryComponentFactory
from .interfaces import (
    IFinalSceneHandler,
    ITheoryVerifier,
    IEndingWriter
)

# Individual components (for custom setups)
from .final_scene import FinalSceneHandler
from .theory_verifier import TheoryVerifier
from .ending_writer import EndingWriter

__all__ = [
    # Main interface (same as before)
    'TheoryProcessor',
    
    # Factory for custom setups
    'TheoryComponentFactory',
    
    # Interfaces for custom implementations
    'IFinalSceneHandler',
    'ITheoryVerifier',
    'IEndingWriter',
    
    # Individual components
    'FinalSceneHandler',
    'TheoryVerifier',
    'EndingWriter',
]