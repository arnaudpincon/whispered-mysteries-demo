"""
Main conversation handler that orchestrates the conversation flow
"""

import json
import logging
from typing import Any

from ai_engine.api.service import APIConfig
from ai_engine.prompts.character import create_neutral_character_prompt
from ai_engine.utils.ai_logger import log_ai_response
from game_engine.models.character import Character
from game_engine.models.player import Player


from .errors import (
    ConversationErrorHandler, 
    ConversationResponseFormatter, 
    ConversationValidator
)
from .interfaces import IConversationHandler, IMemoryManager, IPersonalityEngine

logger = logging.getLogger(__name__)


class StandardConversationHandler(IConversationHandler):
    """Handles standard character conversations"""
    
    def __init__(
        self, 
        api_service, 
        memory_manager: IMemoryManager,
        personality_engine: IPersonalityEngine
    ):
        self.api_service = api_service
        self.memory_manager = memory_manager
        self.personality_engine = personality_engine
    
    def handle_conversation(
        self, character: Character, player: Player, topic: str, game_state: Any
    ) -> str:
        """Handle a complete conversation interaction"""
        try:
            # Validate inputs
            is_valid, error_msg = ConversationValidator.validate_conversation_inputs(
                character, player, topic, game_state
            )
            
            if not is_valid:
                return ConversationResponseFormatter.format_error_response(error_msg)
            
            # Get conversation context with memory and lore
            messages = self.memory_manager.get_conversation_context(
                character, topic, game_state, player
            )
            
            # Create base character prompt
            character_prompt = create_neutral_character_prompt(character, player)
            
            # Get base AI response
            base_content = self.api_service.make_api_call(
                messages=messages,
                system_content=character_prompt,
                max_tokens=APIConfig.MAX_TOKENS_LARGE,
                response_format={"type": "json_object"},
            )
            
            if base_content is None:
                return ConversationErrorHandler.handle_ai_timeout("base_conversation")
            

            log_ai_response(base_content, "Neutral Character Agent", "json")
            
            # Parse base response
            try:
                base_response_dict = json.loads(base_content)
            except json.JSONDecodeError:
                logger.error("Failed to parse base AI response")
                return ConversationErrorHandler.handle_conversation_error(
                    Exception("JSON decode error"), "response_parsing"
                )
            
            # Apply personality enhancement
            enhanced_response = self.personality_engine.apply_personality(
                base_response_dict, character, topic
            )
            
            # Store conversation in memory
            self.memory_manager.store_conversation(
                character, topic, enhanced_response.get("answer", "")
            )

            log_ai_response(
                enhanced_response.get("answer", "No answer found"), 
                "Personalized Character Agent", 
                "text"
            )
            
            return json.dumps(enhanced_response)
            
        except Exception as e:
            return ConversationErrorHandler.handle_conversation_error(
                e, "conversation_handling"
            )