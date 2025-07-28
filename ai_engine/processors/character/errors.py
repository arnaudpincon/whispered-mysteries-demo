"""
Error handling, validation, and response formatting for character conversations
"""

import json
import logging
from typing import Any, Optional, Tuple

from game_engine.core.game_state import GameMode
from game_engine.models.character import Character
from game_engine.models.player import Player



logger = logging.getLogger(__name__)


class ConversationError(Exception):
    """Base exception for conversation-related errors"""
    pass


class ConversationErrorHandler:
    """Centralized error handling for conversation operations"""
    
    @staticmethod
    def handle_conversation_error(error: Exception, context: str) -> str:
        """Handle conversation errors gracefully"""
        logger.error(f"Conversation error in {context}: {error}")
        
        error_response = {
            "action": GameMode.CONVERSATION.value,
            "answer": "I'm having trouble understanding right now. Could you repeat that?",
            "think": f"Error in conversation: {str(error)}",
        }
        
        return json.dumps(error_response)

    @staticmethod
    def handle_ai_timeout(context: str) -> str:
        """Handle AI timeout specifically"""
        logger.warning(f"AI timeout in {context}")
        
        error_response = {
            "action": GameMode.CONVERSATION.value,
            "answer": "I need a moment to think. Could you ask again?",
            "think": "AI service timeout occurred",
        }
        
        return json.dumps(error_response)


class ConversationResponseFormatter:
    """Formats conversation responses consistently"""
    
    @staticmethod
    def format_json_response(
        think: str, answer: str, action: str = GameMode.CONVERSATION.value
    ) -> str:
        """Format a standard conversation response"""
        response = {
            "think": think,
            "answer": answer,
            "action": action
        }
        return json.dumps(response)
    
    @staticmethod
    def format_error_response(error_message: str) -> str:
        """Format an error response"""
        return ConversationResponseFormatter.format_json_response(
            think=f"Error occurred: {error_message}",
            answer="I'm afraid I didn't catch what you said. Could you repeat that?",
            action=GameMode.CONVERSATION.value
        )
    
    @staticmethod
    def format_empty_topic_response() -> str:
        """Format response for empty or invalid topic"""
        return ConversationResponseFormatter.format_json_response(
            think="Empty or invalid topic provided",
            answer="I'm afraid I didn't catch what you said. Could you repeat that?",
            action=GameMode.CONVERSATION.value
        )


class ConversationValidator:
    """Validates conversation inputs and states"""
    
    @staticmethod
    def validate_topic(topic: str) -> bool:
        """Validate that topic is not empty or invalid"""
        return topic and topic.strip()
    
    @staticmethod
    def validate_character(character: Character) -> bool:
        """Validate character object"""
        return character and hasattr(character, 'name')
    
    @staticmethod
    def validate_game_state(game_state: Any) -> bool:
        """Validate game state object"""
        return game_state is not None
    
    @staticmethod
    def validate_conversation_inputs(
        character: Character, player: Player, topic: str, game_state: Any
    ) -> Tuple[bool, Optional[str]]:
        """Validate all conversation inputs"""
        if not ConversationValidator.validate_topic(topic):
            return False, "Invalid topic"
        
        if not ConversationValidator.validate_character(character):
            return False, "Invalid character"
        
        if not player:
            return False, "Invalid player"
        
        if not ConversationValidator.validate_game_state(game_state):
            return False, "Invalid game state"
        
        return True, None
