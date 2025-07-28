"""
Character memory management and lore retrieval
"""

import logging
from typing import Any, Dict, List, Optional

from ai_engine.api.service import APIConfig
from ai_engine.prompts.character import create_get_lore_information
from ai_engine.utils.ai_logger import log_ai_response
from ai_engine.utils.formatters import format_game_state
from game_engine.models.character import Character
from game_engine.models.player import Player
from .interfaces import IMemoryManager, ILoreRetriever

logger = logging.getLogger(__name__)


class GameStateLoreRetriever(ILoreRetriever):
    """Retrieves lore information from game state"""
    
    def __init__(self, api_service):
        self.api_service = api_service
    
    def get_relevant_lore(
        self, game_state: Any, topic: str, player: Player, character: Character
    ) -> Optional[str]:
        """Get relevant lore information for a conversation topic"""
        try:
            # Normalize game state using existing adapter
            ai_state = self._normalize_game_state(game_state)
            if ai_state is None:
                return None
            
            # Create lore retrieval prompt
            prompt_get_info = create_get_lore_information(
                format_game_state(ai_state), player, character, topic
            )
            
            messages = [*character.memory_current, {"role": "user", "content": topic}]
            
            return self.api_service.make_api_call(
                messages=messages,
                system_content=prompt_get_info,
                max_tokens=APIConfig.MAX_TOKENS_MEDIUM,
            )
            
        except Exception as e:
            logger.error(f"Error getting lore information: {e}")
            return None
    
    def _normalize_game_state(self, game_state: Any) -> Optional[Dict[str, Any]]:
        """Normalize game state to AI-compatible format"""
        
        try:
            ai_state = game_state.to_ai_format()
            if ai_state is None:
                logger.error("Failed to convert game state to AI format")
                return None
            
            return ai_state
            
        except Exception as e:
            logger.error(f"Error normalizing game state: {e}")
            return None


class CharacterMemoryManager(IMemoryManager):
    """Manages character memory and conversation context"""
    
    def __init__(self, lore_retriever: ILoreRetriever):
        self.lore_retriever = lore_retriever
    
    def get_conversation_context(
        self, character: Character, topic: str, game_state: Any, player: Player = None
    ) -> List[Dict[str, str]]:
        """Build complete conversation context"""
        try:
            # Start with character's current memory
            messages = list(character.memory_current)
            
            # Add user topic
            messages.append({"role": "user", "content": topic})
            
            relevant_info = self.lore_retriever.get_relevant_lore(
                game_state, topic, player, character
            )

            log_ai_response(
                f"Relevant informations: {relevant_info}",
                "Lore Retrieved Agent",
                "text"
            )
            
            if relevant_info:
                messages.append({
                    "role": "assistant",
                    "content": f"FACTUAL GAME INFORMATION: The following information is verified and accurate from the game state. Use this factual data to inform your response. Info: {relevant_info}",
                })
            
            return messages
            
        except Exception as e:
            logger.error(f"Error building conversation context: {e}")
            # Return minimal context
            return [{"role": "user", "content": topic}]
    
    def store_conversation(
        self, character: Character, topic: str, response: str
    ) -> None:
        """Store conversation in character memory"""
        try:
            character.remember(topic, "user")
            character.remember(response, "assistant")
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")

