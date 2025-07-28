#!/usr/bin/env python3
"""
Simple Game Options Service - Session based like language service
"""

import os
from typing import Dict

from frontend.core.logging_config import game_logger


class GameOptionsService:
    """Simple service for managing game options in session - no file persistence"""
    
    def __init__(self):
        self._current_teleportation: bool = self._load_teleportation_from_env()
        game_logger.info("Game options service initialized", teleportation=self._current_teleportation)
    
    def get_teleportation_mode(self) -> bool:
        """Get current teleportation mode setting"""
        return self._current_teleportation
    
    def set_teleportation_mode(self, enabled: bool) -> bool:
        """
        Set teleportation mode
        
        Args:
            enabled: Boolean value to set
            
        Returns:
            True if option was set successfully
        """
        old_value = self._current_teleportation
        self._current_teleportation = enabled
        
        # Update environment variable for prompts
        os.environ["TELEPORTATION_MODE"] = str(enabled).lower()
        
        game_logger.info(
            "Teleportation mode changed",
            old_value=old_value,
            new_value=enabled
        )
        
        return True
    
    def get_teleportation_display(self) -> str:
        """Get teleportation mode display name"""
        return "Enabled" if self._current_teleportation else "Disabled"
    
    def _load_teleportation_from_env(self) -> bool:
        """Load teleportation setting from environment variable"""
        try:
            # Load from environment variable if present
            teleportation_env = os.getenv("TELEPORTATION_MODE", "false").lower()
            if teleportation_env in ["true", "false"]:
                result = teleportation_env == "true"
                game_logger.debug("Loaded teleportation from environment", value=result)
                return result
            
            # Default to false
            game_logger.debug("Using default teleportation", value=False)
            return False
            
        except Exception as e:
            game_logger.error("Error loading teleportation setting", error=str(e))
            return False


# Global service instance
_game_options_service = None


def get_game_options_service() -> GameOptionsService:
    """Get or create global game options service instance"""
    global _game_options_service
    if _game_options_service is None:
        _game_options_service = GameOptionsService()
    return _game_options_service


def get_current_teleportation() -> bool:
    """Convenience function to get current teleportation mode for prompts"""
    return get_game_options_service().get_teleportation_mode()


def set_teleportation_mode(enabled: bool) -> bool:
    """Convenience function to set teleportation mode"""
    return get_game_options_service().set_teleportation_mode(enabled)