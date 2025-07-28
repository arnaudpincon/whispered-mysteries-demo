"""
Command execution component - handles the execution phase
"""

import logging
from typing import Any, Dict

from ai_engine.api.service import APIConfig
from ai_engine.prompts.command.executor_agent import create_command_prompt
from ai_engine.utils.formatters import format_game_state
from ai_engine.utils.constants import DefaultAlternatives, ErrorMessages

from .interfaces import ICommandExecutor

logger = logging.getLogger(__name__)


class CommandExecutor(ICommandExecutor):
    """Executes commands based on analysis results"""
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        self.api_service = api_service
        self.cache = cache
        self.dev_mode = dev_mode
    
    def execute_command(self, reasoning_result: Dict[str, Any], game_state: Any) -> Dict[str, Any]:
        """
        Execute command based on analysis results.
        This is the execution step that determines final actions.

        Args:
            reasoning_result: Results from command analysis
            game_state: Current game state

        Returns:
            Dictionary with execution results and player response
        """
        try:
            # Convert game state to text representation
            game_state_str: str = format_game_state(game_state)
            
            # Create execution prompt
            execution_prompt: str = create_command_prompt(reasoning_result, game_state_str)

            # Check cache for execution (less likely to cache due to variability)
            player_location = game_state.get("player", {}).get("location", "unknown")
            cache_context = {
                "type": "execution",
                "location": player_location,
                "action": reasoning_result.get('intended_action', 'unknown')
            }
            
            cached_execution = self.cache.get(
                execution_prompt,
                {"temperature": APIConfig.COMMAND_TEMPERATURE, "format": "json"},
                cache_context
            )
            
            if cached_execution:
                if self.dev_mode:
                    print("🚀 CACHE HIT: Execution found in cache!")
                execution_result = self.api_service.parse_json_response(
                    cached_execution,
                    self._get_fallback_execution()
                )
            else:
                if self.dev_mode:
                    print("💭 CACHE MISS: Computing execution...")

                execution_messages = [{"role": "user", "content": execution_prompt}]
                execution_system_content = "You are a detective game command executor that determines final actions based on analysis results."

                # Get execution decision
                execution_content = self.api_service.make_api_call(
                    messages=execution_messages,
                    system_content=execution_system_content,
                    temperature=APIConfig.COMMAND_TEMPERATURE,
                    response_format={"type": "json_object"},
                    max_tokens=APIConfig.MAX_TOKENS_LARGE,
                )

                if execution_content is None:
                    if self.dev_mode:
                        print("❌ COMMAND EXECUTION: API call failed")
                    return self._get_fallback_execution()

                # Store in cache
                self.cache.put(
                    execution_prompt,
                    {"temperature": APIConfig.COMMAND_TEMPERATURE, "format": "json"},
                    execution_content,
                    cache_context
                )

                # Parse execution result
                execution_result = self.api_service.parse_json_response(
                    execution_content, 
                    self._get_fallback_execution()
                )

            # Add translated command from reasoning
            execution_result["translated_command"] = reasoning_result.get("translated_command")

            return execution_result

        except Exception as e:
            logger.error(f"Error in execute_command: {e}")
            return self._get_fallback_execution()
    
    def _get_fallback_execution(self) -> Dict[str, Any]:
        """Get fallback execution result when execution fails"""
        return {
            "valid": False,
            "message": ErrorMessages.COMMAND_NOT_UNDERSTOOD,
            "alternatives": DefaultAlternatives.BASIC_COMMANDS,
            "action": "help",
            "target": "",
            "target_type": "unknown",
        }