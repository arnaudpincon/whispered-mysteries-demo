"""
AI Cache System
Memory and disk caching for AI responses
"""

# Configuration and data structures
from .cache_config import (
    CacheConfig,
    CacheEntry,
)

# Key generation
from .cache_keys import (
    CacheKeyGenerator,
)

# Cache implementations
from .memory_cache import (
    LRUCache,
)

from .disk_cache import (
    DiskCache,
)

# Main cache manager
from .cache_manager import (
    AICache,
)

# Decorators and utilities
from .cache_decorators import (
    get_ai_cache,
    initialize_ai_cache,
    cache_ai_response,
)

__all__ = [
    # Configuration
    'CacheConfig',
    'CacheEntry',
    
    # Key generation
    'CacheKeyGenerator',
    
    # Cache implementations
    'LRUCache',
    'DiskCache',
    
    # Main manager
    'AICache',
    
    # Utilities
    'get_ai_cache',
    'initialize_ai_cache',
    'cache_ai_response',
]