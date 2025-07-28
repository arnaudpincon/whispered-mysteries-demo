# ai_engine/cache/cache_manager.py
#!/usr/bin/env python3
"""
AI Cache System for Detective Game
Core cache manager with LRU eviction and configurable settings
Enhanced with cache disable option
"""

import logging
import threading
import time
from typing import Any, Dict, Optional
from ai_engine.cache.cache_config import CacheConfig
from ai_engine.cache.cache_keys import CacheKeyGenerator
from ai_engine.cache.disk_cache import DiskCache
from ai_engine.cache.memory_cache import LRUCache

# Setup logging
logger = logging.getLogger(__name__)


class AICache:
    """Main AI cache manager combining memory and disk caching"""
    
    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        
        if not self.config.enable_cache:
            logger.info("AI Cache is DISABLED - all cache operations will be bypassed")
            self.cache_disabled = True
            self.key_generator = None
            self.memory_cache = None
            self.disk_cache = None
            self.stats = {
                "hits": 0,
                "misses": 0,
                "memory_hits": 0,
                "disk_hits": 0,
                "cache_stores": 0,
                "cache_disabled": True
            }
            return
        
        self.cache_disabled = False
        self.key_generator = CacheKeyGenerator(self.config)
        
        # Initialize caches
        self.memory_cache = LRUCache(self.config.max_memory_entries)
        self.disk_cache = DiskCache(
            self.config.cache_directory,
            self.config.max_disk_entries
        ) if self.config.enable_disk_cache else None
        
        # Statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "memory_hits": 0,
            "disk_hits": 0,
            "cache_stores": 0,
            "cache_disabled": False
        }
        
        # Start cleanup thread
        self._start_cleanup_thread()
        
        logger.info("AI Cache initialized", extra={
            "memory_entries": self.config.max_memory_entries,
            "disk_enabled": self.config.enable_disk_cache,
            "cache_dir": self.config.cache_directory
        })
    
    def get(
        self, 
        prompt: str, 
        model_params: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Any]:
        """
        Get cached AI response
        
        Args:
            prompt: AI prompt text
            model_params: Model parameters
            context: Additional context for cache key
            
        Returns:
            Cached response or None if not found or cache disabled
        """
        # Return None immediately if cache is disabled
        if self.cache_disabled:
            self.stats["misses"] += 1
            logger.debug("Cache bypass - cache disabled")
            return None
        
        # Skip caching for very long prompts
        if len(prompt) > self.config.max_prompt_length:
            logger.debug("Skipping cache for long prompt", extra={"prompt_length": len(prompt)})
            return None
        
        # Generate cache key
        cache_key = self.key_generator.generate_key(prompt, model_params, context)
        
        # Try memory cache first
        result = self.memory_cache.get(cache_key, self.config.memory_ttl_seconds)
        if result is not None:
            self.stats["hits"] += 1
            self.stats["memory_hits"] += 1
            logger.debug("Cache hit (memory)", extra={"key": cache_key[:16]})
            return result
        
        # Try disk cache if enabled
        if self.disk_cache:
            result = self.disk_cache.get(cache_key, self.config.disk_ttl_seconds)
            if result is not None:
                # Store in memory cache for faster future access
                self.memory_cache.put(cache_key, result)
                self.stats["hits"] += 1
                self.stats["disk_hits"] += 1
                logger.debug("Cache hit (disk)", extra={"key": cache_key[:16]})
                return result
        
        # Cache miss
        self.stats["misses"] += 1
        logger.debug("Cache miss", extra={"key": cache_key[:16]})
        return None
    
    def put(
        self, 
        prompt: str, 
        model_params: Dict[str, Any], 
        response: Any, 
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Store AI response in cache
        
        Args:
            prompt: AI prompt text
            model_params: Model parameters
            response: AI response to cache
            context: Additional context for cache key
            metadata: Additional metadata to store
        """
        # Do nothing if cache is disabled
        if self.cache_disabled:
            logger.debug("Cache store bypassed - cache disabled")
            return
        
        # Skip caching for very long prompts
        if len(prompt) > self.config.max_prompt_length:
            return
        
        # Generate cache key
        cache_key = self.key_generator.generate_key(prompt, model_params, context)
        
        # Store in memory cache
        if self.memory_cache:
            self.memory_cache.put(cache_key, response, metadata)
        
        # Store in disk cache if enabled
        if self.disk_cache:
            self.disk_cache.put(cache_key, response, metadata)
        
        self.stats["cache_stores"] += 1
        logger.debug("Stored in cache", extra={"key": cache_key[:16]})
    
    def clear(self) -> None:
        """Clear all caches"""
        if self.cache_disabled:
            logger.debug("Cache clear bypassed - cache disabled")
            return
            
        if self.memory_cache:
            self.memory_cache.clear()
        if self.disk_cache:
            # Clear disk cache would require removing all files
            pass
        logger.info("AI Cache cleared")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        stats = {
            "hit_rate_percent": round(hit_rate, 2),
            "total_requests": total_requests,
            **self.stats
        }
        
        if not self.cache_disabled:
            if self.memory_cache:
                stats["memory_cache"] = self.memory_cache.get_stats()
            
            if self.disk_cache:
                stats["disk_cache"] = self.disk_cache.get_stats()
        
        return stats
    
    def _start_cleanup_thread(self) -> None:
        """Start background cleanup thread"""
        if self.cache_disabled:
            return
            
        def cleanup_worker():
            while True:
                try:
                    time.sleep(self.config.cleanup_interval_seconds)
                    
                    # Cleanup memory cache
                    expired_memory = 0
                    if self.memory_cache:
                        expired_memory = self.memory_cache.cleanup_expired(
                            self.config.memory_ttl_seconds
                        )
                    
                    # Cleanup disk cache
                    expired_disk = 0
                    if self.disk_cache:
                        expired_disk = self.disk_cache.cleanup_expired(
                            self.config.disk_ttl_seconds
                        )
                    
                    if expired_memory > 0 or expired_disk > 0:
                        logger.debug(
                            "Cache cleanup completed",
                            extra={
                                "expired_memory": expired_memory,
                                "expired_disk": expired_disk
                            }
                        )
                        
                except Exception as e:
                    logger.error(f"Cache cleanup error: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()
    
    def is_enabled(self) -> bool:
        """Check if cache is enabled"""
        return not self.cache_disabled
    
    def get_cache_status(self) -> Dict[str, Any]:
        """Get cache status information for debugging"""
        return {
            "enabled": not self.cache_disabled,
            "memory_cache_enabled": self.memory_cache is not None,
            "disk_cache_enabled": self.disk_cache is not None,
            "config": {
                "max_memory_entries": self.config.max_memory_entries,
                "memory_ttl_seconds": self.config.memory_ttl_seconds,
                "enable_disk_cache": self.config.enable_disk_cache,
                "enable_cache": self.config.enable_cache
            }
        }