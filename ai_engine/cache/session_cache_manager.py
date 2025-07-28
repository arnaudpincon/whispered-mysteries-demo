"""
Session-based cache manager to isolate cache between different players
"""

import threading
import uuid
from typing import Any, Dict, Optional
from dataclasses import dataclass, field

from .cache_config import CacheConfig
from .cache_manager import AICache


@dataclass
class SessionCacheManager:
    """Manages separate cache instances for each game session"""
    
    # Dictionary mapping session_id -> AICache instance
    _session_caches: Dict[str, AICache] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    def get_cache_for_session(self, session_id: str) -> AICache:
        """
        Get or create a cache instance for a specific session
        
        Args:
            session_id: Unique identifier for the game session
            
        Returns:
            AICache instance for this session
        """
        with self._lock:
            if session_id not in self._session_caches:
                # Create new cache instance for this session
                config = CacheConfig()
                self._session_caches[session_id] = AICache(config)
                print(f"🔧 Created new cache instance for session: {session_id}")
            
            return self._session_caches[session_id]
    
    def clear_session_cache(self, session_id: str) -> None:
        """
        Clear cache for a specific session
        
        Args:
            session_id: Session to clear
        """
        with self._lock:
            if session_id in self._session_caches:
                self._session_caches[session_id].clear()
                print(f"🧹 Cleared cache for session: {session_id}")
    
    def remove_session(self, session_id: str) -> None:
        """
        Remove a session cache entirely (when game ends)
        
        Args:
            session_id: Session to remove
        """
        with self._lock:
            if session_id in self._session_caches:
                self._session_caches[session_id].clear()
                del self._session_caches[session_id]
                print(f"🗑️ Removed cache for session: {session_id}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get statistics for all session caches"""
        with self._lock:
            stats = {
                "total_sessions": len(self._session_caches),
                "sessions": {}
            }
            
            for session_id, cache in self._session_caches.items():
                stats["sessions"][session_id] = cache.get_statistics()
            
            return stats
    
    def cleanup_inactive_sessions(self, max_sessions: int = 10) -> None:
        """
        Remove oldest sessions if we have too many
        
        Args:
            max_sessions: Maximum number of sessions to keep
        """
        with self._lock:
            if len(self._session_caches) > max_sessions:
                # Remove oldest sessions (simple FIFO)
                sessions_to_remove = list(self._session_caches.keys())[:-max_sessions]
                
                for session_id in sessions_to_remove:
                    self.remove_session(session_id)
                
                print(f"🧹 Cleaned up {len(sessions_to_remove)} inactive sessions")

# Global session cache manager
_session_cache_manager = SessionCacheManager()

def get_session_cache_manager() -> SessionCacheManager:
    """Get the global session cache manager"""
    return _session_cache_manager


def get_cache_for_session(session_id: str) -> AICache:
    """
    Convenience function to get cache for a session
    
    Args:
        session_id: Session identifier
        
    Returns:
        AICache instance for this session
    """
    return _session_cache_manager.get_cache_for_session(session_id)


def generate_session_id() -> str:
    """Generate a unique session ID"""
    return str(uuid.uuid4())