"""
Factory for creating conversation components
"""

from typing import Tuple
from .conversation import StandardConversationHandler
from .memory import CharacterMemoryManager, GameStateLoreRetriever
from .personality import CharacterPersonalityEngine
from .summary import ConversationSummaryService


class ConversationComponentFactory:
    """Factory for creating conversation components"""
    
    @staticmethod
    def create_standard_setup(api_service) -> Tuple[
        StandardConversationHandler, 
        ConversationSummaryService
    ]:
        """Create a standard conversation setup"""
        
        # Create components
        lore_retriever = GameStateLoreRetriever(api_service)
        memory_manager = CharacterMemoryManager(lore_retriever)
        personality_engine = CharacterPersonalityEngine(api_service)
        
        # Create main handler
        conversation_handler = StandardConversationHandler(
            api_service, memory_manager, personality_engine
        )
        
        # Create summary service
        summary_service = ConversationSummaryService(api_service)
        
        return conversation_handler, summary_service