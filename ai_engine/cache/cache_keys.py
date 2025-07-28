import hashlib
import json
import time
from typing import Any, Dict, Optional
from ai_engine.cache.cache_config import CacheConfig


class CacheKeyGenerator:
    """Generates consistent cache keys for AI requests"""
    
    def __init__(self, config: CacheConfig):
        self.config = config
    
    def generate_key(
        self, 
        prompt: str, 
        model_params: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate cache key from prompt and parameters
        
        Args:
            prompt: AI prompt text
            model_params: Model parameters (temperature, max_tokens, etc.)
            context: Additional context (character, game state, etc.)
            
        Returns:
            Hex string cache key
        """
        # Normalize parameters for consistent hashing
        normalized_params = self._normalize_params(model_params)
        
        # Create cache data structure
        cache_data = {
            "prompt": prompt,
            "params": normalized_params,
            "context": context or {}
        }
        
        # Convert to deterministic JSON
        cache_json = json.dumps(cache_data, sort_keys=True, ensure_ascii=True)
        
        # Generate hash
        hasher = hashlib.new(self.config.hash_algorithm)
        hasher.update(cache_json.encode('utf-8'))
        
        # Include timestamp if configured (for time-sensitive caching)
        if self.config.include_timestamp_in_key:
            timestamp = str(int(time.time() // 3600))  # Hour-based timestamp
            hasher.update(timestamp.encode('utf-8'))
        
        return hasher.hexdigest()
    
    def _normalize_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize parameters for consistent caching"""
        normalized = {}
        
        # Define which parameters affect caching
        cache_relevant_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty',
            'presence_penalty', 'response_format', 'tools', 'tool_choice'
        }
        
        for key, value in params.items():
            if key in cache_relevant_params:
                # Round float values to avoid precision issues
                if isinstance(value, float):
                    normalized[key] = round(value, 4)
                else:
                    normalized[key] = value
        
        return normalized


