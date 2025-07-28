"""
Updated cache decorators to support session-based caching
"""

import os
from typing import Optional

from ai_engine.cache.ai_cache import AICache
from ai_engine.cache.cache_config import CacheConfig
from .session_cache_manager import get_cache_for_session, generate_session_id, get_session_cache_manager


def get_ai_cache(session_id: Optional[str] = None) -> 'AICache':
    """
    Get AI cache for a specific session
    
    Args:
        session_id: Optional session identifier. If None, creates a new session.
        
    Returns:
        AICache instance for the session
    """
    if session_id is None:
        session_id = generate_session_id()
        print(f"🆕 Generated new session ID: {session_id}")
    
    cache = get_cache_for_session(session_id)
    
    # Log cache status on first access
    if cache.config.enable_cache:
        print(f"✅ AI Cache is ENABLED for session: {session_id}")
    else:
        print(f"🚫 AI Cache is DISABLED for session: {session_id}")
        
    return cache


def initialize_ai_cache(session_id: str, config: Optional['CacheConfig'] = None) -> None:
    """
    Initialize AI cache for a specific session with custom configuration
    
    Args:
        session_id: Session identifier
        config: Optional cache configuration
    """
    from .cache_config import CacheConfig
    from .cache_manager import AICache
    
    if config is None:
        config = CacheConfig()
    
    # Manually create cache for this session
    manager = get_session_cache_manager()
    with manager._lock:
        manager._session_caches[session_id] = AICache(config)
    
    status = "ENABLED" if config.enable_cache else "DISABLED"
    print(f"🔧 AI Cache initialized for session {session_id}: {status}")


def cache_ai_response(session_id: str, context_key: Optional[str] = None):
    """
    Decorator to automatically cache AI responses for a specific session
    
    Args:
        session_id: Session identifier
        context_key: Optional context identifier for cache key
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache = get_cache_for_session(session_id)
            
            # Skip cache logic entirely if disabled
            if hasattr(cache, 'cache_disabled') and cache.cache_disabled:
                return func(*args, **kwargs)
            
            # Extract cache parameters from function arguments
            prompt = None
            model_params = {}
            
            if args:
                prompt = str(args[0])  # Assume first arg is prompt
            
            # Check if we have cached result
            if prompt:
                cached_result = cache.get(prompt, model_params, {"context": context_key})
                if cached_result is not None:
                    return cached_result
            
            # Call original function
            result = func(*args, **kwargs)
            
            # Cache the result
            if prompt and result:
                cache.put(prompt, model_params, result, {"context": context_key})
            
            return result
        return wrapper
    return decorator