"""
Character description generation component
"""

import logging

from ai_engine.api.service import APIConfig
from ai_engine.prompts import create_character_description_prompt
from game_engine.models.character import Character
from game_engine.models.room import Room

from .interfaces import ICharacterDescriptionGenerator

logger = logging.getLogger(__name__)


class CharacterDescriptionGenerator(ICharacterDescriptionGenerator):
    """Generates descriptions of characters in their environment"""
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        self.api_service = api_service
        self.cache = cache
        self.dev_mode = dev_mode
    
    def generate_description(self, character: Character, room: Room) -> str:
        """
        Generates a description of a character.

        Args:
            character: Character to describe
            room: Room where the character is located

        Returns:
            Description of the character
        """
        try:
            prompt: str = create_character_description_prompt(character, room)
            
            # Check cache first
            cache_context = {
                "type": "character", 
                "character": character.name, 
                "room": room.name
            }
            
            cached_result = self.cache.get(
                prompt, 
                {"temperature": 0.7}, 
                cache_context
            )
            
            if cached_result:
                if self.dev_mode:
                    print(f"🚀 CACHE HIT: Character description found in cache for {character.name}")
                return cached_result
            
            # No cache, make API call
            messages = [{"role": "user", "content": prompt}]
            system_content = "You are the narrator of a detective game set in 19th century Blackwood Manor where a murder has been committed."

            content = self.api_service.make_api_call(
                messages=messages,
                system_content=system_content,
                max_tokens=APIConfig.MAX_TOKENS_MEDIUM,
            )

            # Always define result with a fallback
            if content:
                result = content
            else:
                result = f"You inspect {character.name}. There is nothing special to note."
            
            # Store in cache
            self.cache.put(
                prompt, 
                {"temperature": 0.7}, 
                result, 
                cache_context
            )
            
            if self.dev_mode:
                print(f"💾 CACHE MISS: Generated and cached character description for {character.name}")
            
            return result

        except Exception as e:
            logger.error(f"Error in generate_character_description: {e}")
            return f"You inspect {character.name}. There is nothing special to note."