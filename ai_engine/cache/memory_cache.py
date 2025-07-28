from collections import OrderedDict
import json
import threading
import time
from typing import Any, Dict, Optional
from ai_engine.cache.cache_config import CacheEntry

class LRUCache:
    """LRU (Least Recently Used) cache implementation"""
    
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.RLock()
    
    def get(self, key: str, ttl_seconds: int) -> Optional[Any]:
        """Get value from cache"""
        with self._lock:
            entry = self.cache.get(key)
            if entry is None:
                return None
            
            # Check if expired
            if entry.is_expired(ttl_seconds):
                del self.cache[key]
                return None
            
            # Update access and move to end (most recently used)
            entry.touch()
            self.cache.move_to_end(key)
            
            return entry.value
    
    def put(self, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Put value in cache"""
        with self._lock:
            # Calculate size
            size_bytes = self._calculate_size(value)
            
            # Create entry
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=time.time(),
                last_accessed=time.time(),
                size_bytes=size_bytes,
                metadata=metadata or {}
            )
            
            # Remove existing entry if present
            if key in self.cache:
                del self.cache[key]
            
            # Add new entry
            self.cache[key] = entry
            
            # Evict if necessary
            while len(self.cache) > self.max_size:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
    
    def remove(self, key: str) -> bool:
        """Remove specific key"""
        with self._lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all entries"""
        with self._lock:
            self.cache.clear()
    
    def cleanup_expired(self, ttl_seconds: int) -> int:
        """Remove expired entries"""
        with self._lock:
            expired_keys = []
            for key, entry in self.cache.items():
                if entry.is_expired(ttl_seconds):
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.cache[key]
            
            return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            total_size = sum(entry.size_bytes for entry in self.cache.values())
            return {
                "entries": len(self.cache),
                "max_size": self.max_size,
                "total_size_bytes": total_size,
                "oldest_entry": min(entry.created_at for entry in self.cache.values()) if self.cache else None,
                "newest_entry": max(entry.created_at for entry in self.cache.values()) if self.cache else None
            }
    
    def _calculate_size(self, value: Any) -> int:
        """Estimate size of cached value"""
        try:
            if isinstance(value, str):
                return len(value.encode('utf-8'))
            elif isinstance(value, (dict, list)):
                return len(json.dumps(value).encode('utf-8'))
            else:
                return len(str(value).encode('utf-8'))
        except:
            return 1000  # Default size estimate


