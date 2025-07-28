import json
from pathlib import Path
import pickle
import threading
import time
from typing import Any, Dict, Optional
from venv import logger


class DiskCache:
    """Persistent disk cache for AI responses"""
    
    def __init__(self, cache_dir: str, max_entries: int):
        self.cache_dir = Path(cache_dir)
        self.max_entries = max_entries
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        
        # Index file for metadata
        self.index_file = self.cache_dir / "cache_index.json"
        self._load_index()
    
    def _load_index(self) -> None:
        """Load cache index from disk"""
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r') as f:
                    self.index = json.load(f)
            else:
                self.index = {}
        except Exception as e:
            logger.warning(f"Failed to load cache index: {e}")
            self.index = {}
    
    def _save_index(self) -> None:
        """Save cache index to disk"""
        try:
            with open(self.index_file, 'w') as f:
                json.dump(self.index, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save cache index: {e}")
    
    def get(self, key: str, ttl_seconds: int) -> Optional[Any]:
        """Get value from disk cache"""
        with self._lock:
            if key not in self.index:
                return None
            
            entry_info = self.index[key]
            
            # Check if expired
            if time.time() - entry_info['created_at'] > ttl_seconds:
                self._remove_entry(key)
                return None
            
            # Load from disk
            cache_file = self.cache_dir / f"{key}.pkl"
            if not cache_file.exists():
                del self.index[key]
                return None
            
            try:
                with open(cache_file, 'rb') as f:
                    value = pickle.load(f)
                
                # Update access time
                entry_info['last_accessed'] = time.time()
                entry_info['access_count'] = entry_info.get('access_count', 0) + 1
                self._save_index()
                
                return value
                
            except Exception as e:
                logger.error(f"Failed to load cache entry {key}: {e}")
                self._remove_entry(key)
                return None
    
    def put(self, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Put value in disk cache"""
        with self._lock:
            cache_file = self.cache_dir / f"{key}.pkl"
            
            try:
                # Save to disk
                with open(cache_file, 'wb') as f:
                    pickle.dump(value, f)
                
                # Update index
                self.index[key] = {
                    'created_at': time.time(),
                    'last_accessed': time.time(),
                    'access_count': 1,
                    'size_bytes': cache_file.stat().st_size,
                    'metadata': metadata or {}
                }
                
                # Cleanup if necessary
                self._cleanup_if_needed()
                self._save_index()
                
            except Exception as e:
                logger.error(f"Failed to save cache entry {key}: {e}")
                if cache_file.exists():
                    cache_file.unlink()
    
    def _remove_entry(self, key: str) -> None:
        """Remove entry from disk and index"""
        cache_file = self.cache_dir / f"{key}.pkl"
        if cache_file.exists():
            cache_file.unlink()
        if key in self.index:
            del self.index[key]
    
    def _cleanup_if_needed(self) -> None:
        """Remove oldest entries if over limit"""
        if len(self.index) <= self.max_entries:
            return
        
        # Sort by last access time
        sorted_entries = sorted(
            self.index.items(),
            key=lambda x: x[1]['last_accessed']
        )
        
        # Remove oldest entries
        entries_to_remove = len(self.index) - self.max_entries
        for key, _ in sorted_entries[:entries_to_remove]:
            self._remove_entry(key)
    
    def cleanup_expired(self, ttl_seconds: int) -> int:
        """Remove expired entries"""
        with self._lock:
            current_time = time.time()
            expired_keys = []
            
            for key, entry_info in self.index.items():
                if current_time - entry_info['created_at'] > ttl_seconds:
                    expired_keys.append(key)
            
            for key in expired_keys:
                self._remove_entry(key)
            
            if expired_keys:
                self._save_index()
            
            return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get disk cache statistics"""
        with self._lock:
            total_size = sum(entry['size_bytes'] for entry in self.index.values())
            return {
                "entries": len(self.index),
                "max_entries": self.max_entries,
                "total_size_bytes": total_size,
                "cache_directory": str(self.cache_dir),
                "index_file_exists": self.index_file.exists()
            }


