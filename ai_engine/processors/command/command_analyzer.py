"""
Command analysis component - handles the reasoning phase
"""

import logging
from typing import Any, Dict

from ai_engine.api.service import APIConfig
from ai_engine.prompts.command.reasoning_agent import create_reasoning_prompt
from ai_engine.utils.ai_logger import log_ai_response
from ai_engine.utils.formatters import format_game_state
from ai_engine.utils.constants import ErrorMessages

from .interfaces import ICommandAnalyzer

logger = logging.getLogger(__name__)


class CommandAnalyzer(ICommandAnalyzer):
    """Analyzes and validates player commands in the reasoning phase"""
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        self.api_service = api_service
        self.cache = cache
        self.dev_mode = dev_mode
    
    def analyze_command(self, command: str, game_state: Any) -> Dict[str, Any]:
        """
        Analyze player command and extract intent, targets, and validation.
        This is the reasoning step that understands what the player wants.

        Args:
            command: Player's input command in any language
            game_state: Current game state

        Returns:
            Dictionary with analysis results including validation
        """
        try:
            if self.dev_mode:
                print(f"🔍 COMMAND ANALYSIS: Analyzing '{command}'")

            # Convert game state to text representation
            game_state_str: str = format_game_state(game_state)
            
            # Create reasoning prompt
            reasoning_prompt: str = create_reasoning_prompt(game_state_str, command)

            if self.dev_mode:
                cache_status = "ENABLED" if self.cache.is_enabled() else "DISABLED"
                print(f"🔧 Cache Status: {cache_status}")
            
            # Check cache for reasoning
            player_location = game_state.get("player", {}).get("location", "unknown")
            cache_context = {
                "type": "reasoning", 
                "location": player_location,
                "command_type": "analysis"
            }
            
            cached_reasoning = self.cache.get(
                reasoning_prompt,
                {"temperature": APIConfig.COMMAND_TEMPERATURE, "format": "json"},
                cache_context
            )
            
            if cached_reasoning:
                if self.dev_mode:
                    print("🚀 CACHE HIT: Reasoning found in cache!")
                reasoning_result = self.api_service.parse_json_response(
                    cached_reasoning,
                    self._get_fallback_reasoning()
                )
            else:
                if self.dev_mode:
                    print("💭 CACHE MISS: Computing reasoning...")
                
                reasoning_messages = [{"role": "user", "content": reasoning_prompt}]
                reasoning_system_content = "You are a detective game command analyzer that understands and validates player commands."
            
                reasoning_content = self.api_service.make_api_call(
                    messages=reasoning_messages,
                    system_content=reasoning_system_content,
                    temperature=APIConfig.COMMAND_TEMPERATURE,
                    response_format={"type": "json_object"},
                    max_tokens=APIConfig.MAX_TOKENS_XXLARGE,
                )
            
                if reasoning_content is None:
                    if self.dev_mode:
                        log_ai_response(
                            "COMMAND ANALYSIS: API call failed",
                            "CommandAnalyzer",
                            "error"
                        )
                    return self._get_fallback_reasoning()
            
                # Store in cache
                self.cache.put(
                    reasoning_prompt,
                    {"temperature": APIConfig.COMMAND_TEMPERATURE, "format": "json"},
                    reasoning_content,
                    cache_context
                )
            
                reasoning_result = self.api_service.parse_json_response(
                    reasoning_content, 
                    self._get_fallback_reasoning()
                )

            return reasoning_result

        except Exception as e:
            logger.error(f"Error in analyze_command: {e}")
            return self._get_fallback_reasoning()
    
    def _get_fallback_reasoning(self) -> Dict[str, Any]:
        """Get fallback reasoning result when analysis fails"""
        return {
            "validation_result": "invalid",
            "validation_reason": "Failed to analyze command",
            "intended_action": "help",
            "intended_target": "",
            "translated_command": "",
        }