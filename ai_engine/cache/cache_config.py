from dataclasses import dataclass, field
import os
import time
from typing import Any, Dict


@dataclass
class CacheConfig:
    """Configuration for AI cache system"""
    
    # Memory cache settings
    max_memory_entries: int = 1000
    memory_ttl_seconds: int = 3600  # 1 hour
    
    # Disk cache settings
    enable_disk_cache: bool = False
    max_disk_entries: int = 10000
    disk_ttl_seconds: int = 86400  # 24 hours
    cache_directory: str = "cache/ai_responses"
    
    # Performance settings
    cleanup_interval_seconds: int = 300  # 5 minutes
    max_prompt_length: int = 10000  # Cache only prompts shorter than this
    
    # Hash settings
    hash_algorithm: str = "sha256"
    include_timestamp_in_key: bool = False

    enable_cache: bool = field(default_factory=lambda: _get_cache_enabled_from_env())

    def __post_init__(self):
        """Post-initialization to handle cache disabling"""
        if not self.enable_cache:
            # Disable both memory and disk cache if cache is disabled
            self.max_memory_entries = 0
            self.enable_disk_cache = False
            print("🚫 AI Cache is DISABLED via environment variable")

def _get_cache_enabled_from_env() -> bool:
    """Get cache enabled status from environment variable"""
    cache_enabled = os.getenv("AI_CACHE_ENABLED", "false").lower()
    return cache_enabled in ["true", "1", "yes", "on"]

@dataclass
class CacheEntry:
    """Single cache entry with metadata"""
    
    key: str
    value: Any
    created_at: float
    last_accessed: float
    access_count: int = 0
    size_bytes: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self, ttl_seconds: int) -> bool:
        """Check if entry has expired"""
        return time.time() - self.created_at > ttl_seconds
    
    def touch(self) -> None:
        """Update access time and count"""
        self.last_accessed = time.time()
        self.access_count += 1



