"""
Character personality engine for applying personality traits to responses
"""

import logging
from typing import Any, Dict

from ai_engine.api.service import APIConfig
from ai_engine.prompts.character import create_personality_character_prompt
from game_engine.models.character import Character

from .interfaces import IPersonalityEngine

logger = logging.getLogger(__name__)


class CharacterPersonalityEngine(IPersonalityEngine):
    """Applies character personality to responses"""
    
    def __init__(self, api_service):
        self.api_service = api_service
    
    def apply_personality(
        self, base_response: Dict[str, Any], character: Character, topic: str
    ) -> Dict[str, Any]:
        """Apply character personality to a base response"""
        try:
            base_answer = base_response.get("answer", "")
            
            if not base_answer:
                return base_response
            
            # Create personality transformation prompt
            personality_prompt = create_personality_character_prompt(
                base_answer=base_answer, 
                character=character, 
                conversation_topic=topic
            )
            
            messages = [
                *character.memory_current,
                {"role": "user", "content": personality_prompt},
            ]
            
            # Call API to transform the answer
            enhanced_answer = self.api_service.make_api_call(
                messages=messages,
                max_tokens=APIConfig.MAX_TOKENS_LARGE,
            )
            
            # Return enhanced response or fallback to original
            result = base_response.copy()
            result["answer"] = (
                enhanced_answer if enhanced_answer is not None else base_answer
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error applying personality: {e}")
            return base_response