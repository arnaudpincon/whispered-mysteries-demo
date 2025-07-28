"""
Conversation summary service
"""

import logging

from ai_engine.prompts.character import create_conversation_summary_prompt
from game_engine.models.character import Character
from game_engine.models.player import Player

logger = logging.getLogger(__name__)


class ConversationSummaryService:
    """Handles conversation summarization"""
    
    def __init__(self, api_service):
        self.api_service = api_service
    
    def create_summary(self, character: Character, player: Player) -> str:
        """Generate a summary of conversation between character and player"""
        try:
            prompt = create_conversation_summary_prompt(character, player)
            messages = [{"role": "user", "content": prompt}]
            system_content = (
                "You are summarizing a conversation between a character and a player."
            )
            
            content = self.api_service.make_api_call(
                messages=messages, 
                system_content=system_content, 
                max_tokens=200
            )
            
            return content or "Unable to generate conversation summary."
            
        except Exception as e:
            logger.error(f"Error in conversation_summary: {e}")
            return "Unable to generate conversation summary."