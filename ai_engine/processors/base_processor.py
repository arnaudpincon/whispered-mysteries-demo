#!/usr/bin/env python3
"""
Base Processor for AI Engine
Common functionality and interface for all specialized processors
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

# Setup logging
logger = logging.getLogger(__name__)


class BaseProcessor(ABC):
    """
    Abstract base class for all AI processors
    Provides common functionality and enforces interface consistency
    """
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        """
        Initialize base processor with common dependencies
        
        Args:
            api_service: APIService instance for AI calls
            cache: Cache manager instance
            dev_mode: Enable debug logging and development features
        """
        self.api_service = api_service
        self.cache = cache
        self.dev_mode = dev_mode
        
        # Processor-specific logger
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def _log_debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log debug message if dev_mode is enabled"""
        if self.dev_mode:
            self.logger.debug(message, extra=extra or {})
    
    def _validate_ai_state_format(self, state: Dict[str, Any]) -> bool:
        """
        Validate AI state format - common across processors
        
        Args:
            state: State dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_keys = ["player", "mode"]  # Minimum required keys
        
        try:
            # Check required keys exist
            if not all(key in state for key in required_keys):
                missing_keys = [key for key in required_keys if key not in state]
                self.logger.error(f"Missing required keys in AI state: {missing_keys}")
                return False
            
            # Validate player data
            player_data = state["player"]
            if not isinstance(player_data, dict):
                self.logger.error("Player data must be a dictionary")
                return False
            
            # Validate mode
            if not isinstance(state["mode"], str):
                self.logger.error("Mode must be a string")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating AI state format: {e}")
            return False
    
    def _normalize_game_state(self, game_state: Any) -> Optional[Dict[str, Any]]:
        """
        
        Args:
            game_state: GameState object, dictionary, or any compatible format
            
        Returns:
            Normalized AI-compatible dictionary or None if invalid
        """
        try:
            ai_state = game_state.to_ai_format()
            
            if ai_state is None:
                self.logger.error("Failed to convert game state to AI format")
                return None
            
            self._log_debug("Successfully converted game state to AI format")
            return ai_state
            
        except Exception as e:
            self.logger.error(f"Error normalizing game state: {e}")
            return None
    
    def _create_cache_key(self, base_key: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a consistent cache key for this processor
        
        Args:
            base_key: Base cache key
            context: Optional context for key generation
            
        Returns:
            Full cache key with processor namespace
        """
        processor_name = self.__class__.__name__.lower().replace('processor', '')
        cache_key = f"{processor_name}:{base_key}"
        
        if context:
            # Add context hash if provided
            import hashlib
            context_str = str(sorted(context.items()))
            context_hash = hashlib.md5(context_str.encode()).hexdigest()[:8]
            cache_key += f":{context_hash}"
        
        return cache_key
    
    @abstractmethod
    def get_processor_name(self) -> str:
        """Return the name of this processor for logging and identification"""
        pass