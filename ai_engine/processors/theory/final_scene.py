"""
Final scene handling component
"""

import logging
from typing import Any, Dict, List

from ai_engine.utils.constants import ErrorMessages

from .interfaces import IFinalSceneHandler

logger = logging.getLogger(__name__)


class FinalSceneHandler(IFinalSceneHandler):
    """Handles final scene interactions where player completes their theory"""
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        self.api_service = api_service
        self.cache = cache
        self.dev_mode = dev_mode
    
    def handle_final_scene(
        self, player: Any, conversation: List[Dict[str, str]], game_state: Any
    ) -> Dict[str, Any]:
        """
        Assist the player in completing their murder theory.
        
        Args:
            player: Player object
            conversation: Conversation history
            game_state: Current game state
            
        Returns:
            Dictionary containing scene completion status and response
        """
        try:
            if self.dev_mode:
                print(f"🎭 FINAL SCENE: Processing theory completion")
            
            # Check cache first
            conversation_key = str(hash(str(conversation)))
            cache_context = {
                "type": "final_scene",
                "conversation_hash": conversation_key
            }
            
            cached_result = self.cache.get(
                conversation_key,
                {"temperature": 0.7, "format": "json"},
                cache_context
            )
            
            if cached_result:
                if self.dev_mode:
                    print("🚀 CACHE HIT: Final scene response found in cache")
                return self.api_service.parse_json_response(
                    cached_result,
                    self._get_fallback_response()
                )
            
            # Make API call
            content = self.api_service.make_api_call(
                messages=conversation,
                max_tokens=500,
                response_format={"type": "json_object"},
            )

            if content is None:
                if self.dev_mode:
                    print("❌ FINAL SCENE: API call failed")
                return self._get_fallback_response()
            
            # Parse response
            result = self.api_service.parse_json_response(content, self._get_fallback_response())
            
            # Store in cache
            self.cache.put(
                conversation_key,
                {"temperature": 0.7, "format": "json"},
                content,
                cache_context
            )
            
            if self.dev_mode:
                print("💾 CACHE MISS: Generated and cached final scene response")
            
            return result

        except Exception as e:
            logger.error(f"Error in handle_final_scene: {e}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Get fallback response for final scene"""
        return {
            "completed": False,
            "answer": ErrorMessages.THEORY_ERROR,
        }