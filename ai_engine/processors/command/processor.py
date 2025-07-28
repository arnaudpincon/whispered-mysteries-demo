"""
Main CommandProcessor - Clean interface with refactored components
"""

import logging
from typing import Any, Dict

from ai_engine.processors.base_processor import BaseProcessor
from ai_engine.utils.ai_logger import log_ai_response
from ai_engine.utils.constants import DefaultAlternatives, ErrorMessages, GameStateInput

from .factory import CommandComponentFactory

logger = logging.getLogger(__name__)


class CommandProcessor(BaseProcessor):
    """
    Refactored Command Processor - Now acts as a lightweight coordinator
    
    Responsibilities:
    1. Coordinate command processing components (analysis + execution)
    2. Provide backward-compatible interface
    3. Handle high-level command flow
    4. Manage nonsense action handling
    """
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        super().__init__(api_service, cache, dev_mode)
        
        # Create command components using factory
        (self.command_analyzer,
         self.command_executor,
         self.nonsense_handler) = CommandComponentFactory.create_standard_setup(
            api_service, cache, dev_mode
        )
        
        self._log_debug("CommandProcessor initialized with refactored components")
    
    def get_processor_name(self) -> str:
        return "command"
        
    def process_command(self, command: str, game_state: Any) -> Dict[str, Any]:
        """
        Process a natural language command using the two-phase approach.
        Now coordinated through specialized components.
        
        Args:
            command: Player's input command
            game_state: Current game state
            
        Returns:
            Dictionary with command processing results
        """
        self._log_debug(f"Processing command: '{command}'")
        
        if not command or not command.strip():
            return self._create_error_response(ErrorMessages.COMMAND_NOT_UNDERSTOOD)

        # Normalize game state using adapter
        ai_state = self._normalize_game_state(game_state)
        if ai_state is None:
            return self._create_error_response("Invalid game state format")

        try:
            # Step 1: Analysis - Analyze and understand the command
            reasoning_result = self.command_analyzer.analyze_command(command, ai_state)

            if self.dev_mode:
                # Reasoning complet en JSON coloré
                log_ai_response(reasoning_result, "CommandAnalyzer Agent", "json")
            
            # Step 2: Execution - ALWAYS execute, let executor handle invalid commands intelligently
            execution_result = self.command_executor.execute_command(reasoning_result, ai_state)
            
            if self.dev_mode:
                log_ai_response(execution_result, "CommandExecutor Agent", "json")
            
            return execution_result

        except Exception as e:
            logger.error(f"Error in process_command: {e}")
            return self._create_error_response(ErrorMessages.COMMAND_NOT_UNDERSTOOD)
    
    def nonsense_reaction(self, command: str, game_state: GameStateInput) -> Dict[str, Any]:
        """
        Generate reaction to nonsense actions with reputation awareness.
        Now delegated to specialized component.
        
        Args:
            command: The nonsensical command/action attempted by the player
            game_state: Current game state (GameState object or dictionary)
            
        Returns:
            Dict with message, severity classification and action details
        """
        self._log_debug(f"Handling nonsense action: '{command}'")
        
        try:
            # Normalize game state
            ai_state = self._normalize_game_state(game_state)
            if ai_state is None:
                return {
                    "message": "You attempt something ridiculous, but even describing it seems impossible right now.",
                    "severity": "awkward",
                    "action_category": "unknown"
                }
            
            return self.nonsense_handler.handle_nonsense(command, ai_state)
            
        except Exception as e:
            logger.error(f"Error in nonsense_reaction: {e}")
            return {
                "message": "Your bizarre behavior causes an awkward silence.",
                "severity": "awkward",
                "action_category": "unknown",
                "command_attempted": command,
            }
   
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            "valid": False,
            "message": error_message,
            "alternatives": DefaultAlternatives.BASIC_COMMANDS,
            "action": "help",
            "target": "",
            "target_type": "unknown",
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check the health of command processor components"""
        return {
            "processor_name": self.get_processor_name(),
            "command_analyzer": self.command_analyzer is not None,
            "command_executor": self.command_executor is not None,
            "nonsense_handler": self.nonsense_handler is not None,
            "api_service": self.api_service is not None,
            "cache": self.cache is not None,
            "dev_mode": self.dev_mode
        }