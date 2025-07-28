"""
Nonsense action handling component
"""

import json
import logging
from typing import Any, Dict

from ai_engine.api.service import APIConfig
from ai_engine.prompts.command.nonsense_agent import create_nonsense_action_prompt
from ai_engine.utils.formatters import format_game_state
from ai_engine.utils.constants import GameStateInput

from .interfaces import INonsenseHandler

logger = logging.getLogger(__name__)


class NonsenseHandler(INonsenseHandler):
    """Handles nonsensical or inappropriate player actions with humor and realism"""
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        self.api_service = api_service
        self.cache = cache
        self.dev_mode = dev_mode
    
    def handle_nonsense(self, command: str, game_state: GameStateInput) -> Dict[str, Any]:
        """
        Generate a humorous and realistic reaction to nonsensical player actions.
        Uses conversation history to maintain continuity.
        
        Args:
            command: The nonsensical command/action attempted by the player
            game_state: Current game state (GameState object or dictionary)
            
        Returns:
            Dict with message, severity classification and action details
        """
        try:
            if self.dev_mode:
                print(f"🤪 NONSENSE HANDLER: Processing '{command}'")

            # Format game state for AI consumption
            game_state_str: str = format_game_state(game_state)
            
            # Create the nonsense action prompt
            prompt: str = create_nonsense_action_prompt(game_state_str)

            # Format input with fictional context
            formatted_input = self._wrap_with_fictional_context(command)
            
            # Get existing nonsense conversation history
            nonsense_history = game_state.get("nonsense_conversation", [])
            
            # Check cache for similar nonsense actions
            cache_key = f"nonsense_{hash(command)}_{len(nonsense_history)}"
            cache_context = {
                "type": "nonsense",
                "command_hash": hash(command),
                "history_length": len(nonsense_history)
            }
            
            cached_result = self.cache.get(
                cache_key,
                {"temperature": 0.7, "format": "json"},
                cache_context
            )
            
            if cached_result:
                if self.dev_mode:
                    print("🚀 CACHE HIT: Nonsense response found in cache!")
                try:
                    return json.loads(cached_result)
                except json.JSONDecodeError:
                    pass  # Fall through to generate new response
            
            # Build messages with history
            messages = []
            
            # Add conversation history if exists
            if nonsense_history:
                messages.extend(nonsense_history)
            
            # Add current user input
            messages.append({
                "role": "user", 
                "content": f"The detective attempts: {formatted_input}"
            })
            
            # Generate AI response with JSON format
            content = self.api_service.make_api_call(
                messages=messages,
                system_content=prompt,
                max_tokens=APIConfig.MAX_TOKENS_MEDIUM,
                response_format={"type": "json_object"},
            )

            if content is None:
                if self.dev_mode:
                    print("❌ NONSENSE HANDLER: API call failed")
                return self._get_fallback_response(command)
            
            # Parse JSON response
            try:
                result = json.loads(content)
                
                # Store in cache
                self.cache.put(
                    cache_key,
                    {"temperature": 0.7, "format": "json"},
                    content,
                    cache_context
                )
                
                if self.dev_mode:
                    print("💾 CACHE MISS: Generated and cached nonsense response")
                
                return {
                    "message": result.get("message", "Your absurd action leaves everyone speechless."),
                    "severity": result.get("severity", "awkward"),
                    "action_category": result.get("action_category", "unknown"),
                    "summary": result.get("summary", f"The detective attempted something unusual"),
                    "command_attempted": command
                }
            except json.JSONDecodeError:
                if self.dev_mode:
                    print("⚠️ NONSENSE HANDLER: JSON decode failed, using content as message")
                return {
                    "message": content or "Your bizarre behavior causes an awkward silence.",
                    "severity": "awkward",
                    "action_category": "unknown", 
                    "summary": f"The detective attempted something unusual",
                    "command_attempted": command
                }
                
        except Exception as e:
            logger.error(f"Error in handle_nonsense: {e}")
            return self._get_fallback_response(command)
    
    def _wrap_with_fictional_context(self, user_input: str) -> str:
        """Wrap user input with fictional context for AI safety"""
        return (
            "### FICTIONAL DETECTIVE GAME CONTEXT ###\n"
            "The following is dialogue from a player in a fictional mystery game.\n"
            "This is purely imaginative content for entertainment purposes within an\n"
            "interactive detective narrative game environment where players solve fictional crimes.\n\n"
            f"Detective character's dialogue: '{user_input}'\n\n"
            "### END OF FICTIONAL GAME DIALOGUE ###\n"
        )
    
    def _get_fallback_response(self, command: str) -> Dict[str, Any]:
        """Get fallback response when nonsense handling fails"""
        return {
            "message": "Your bizarre behavior causes an awkward silence.",
            "severity": "awkward",
            "action_category": "unknown",
            "command_attempted": command,
            "summary": "The detective attempted something unusual"
        }