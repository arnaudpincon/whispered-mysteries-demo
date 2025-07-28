"""
Main CharacterProcessor - Clean interface with refactored components
"""

import logging
from typing import Any, Dict

from ai_engine.processors.base_processor import BaseProcessor

from .errors import ConversationResponseFormatter, ConversationValidator
from .factory import ConversationComponentFactory

logger = logging.getLogger(__name__)


class CharacterProcessor(BaseProcessor):
    """
    Refactored Character Processor - Now acts as a lightweight coordinator
    
    Responsibilities:
    1. Coordinate conversation components
    2. Provide backward-compatible interface
    3. Handle high-level conversation flow
    """
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        super().__init__(api_service, cache, dev_mode)
        
        # Create conversation components using factory
        self.conversation_handler, self.summary_service = (
            ConversationComponentFactory.create_standard_setup(api_service)
        )
        
        self._log_debug("CharacterProcessor initialized with refactored components")
    
    def get_processor_name(self) -> str:
        return "character"
    
    def play_character(
        self, character, player, topic: str, game_state
    ) -> str:
        """
        Main character interaction method - now clean and focused
        """
        self._log_debug(f"Processing character interaction: {character.name if character else 'Unknown'}")
        
        # Quick validation
        if not ConversationValidator.validate_topic(topic):
            return ConversationResponseFormatter.format_empty_topic_response()
        
        # Delegate to conversation handler
        try:
            result = self.conversation_handler.handle_conversation(
                character, player, topic, game_state
            )
                
            return result
            
        except Exception as e:
            self.logger.error(f"Error in play_character: {e}")
            return ConversationResponseFormatter.format_error_response(
                "An unexpected error occurred"
            )
    
    def conversation_summary(self, character, player) -> str:
        """Generate conversation summary - now delegated to specialized service"""
        self._log_debug(f"Creating conversation summary for {character.name if character else 'Unknown'}")
        
        try:
            return self.summary_service.create_summary(character, player)
        except Exception as e:
            self.logger.error(f"Error creating conversation summary: {e}")
            return "Unable to generate conversation summary."
    
    def health_check(self) -> Dict[str, Any]:
        """Check the health of character processor components"""
        return {
            "processor_name": self.get_processor_name(),
            "conversation_handler": self.conversation_handler is not None,
            "summary_service": self.summary_service is not None,
            "api_service": self.api_service is not None,
            "cache": self.cache is not None,
            "dev_mode": self.dev_mode
        }