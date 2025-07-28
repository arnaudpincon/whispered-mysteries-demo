"""
Abstract interfaces for character conversation components
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from game_engine.models.character import Character
from game_engine.models.player import Player

class IConversationHandler(ABC):
    """Interface for handling character conversations"""
    
    @abstractmethod
    def handle_conversation(
        self, character: Character, player: Player, topic: str, game_state: Any
    ) -> str:
        """Handle a conversation interaction"""
        pass


class IPersonalityEngine(ABC):
    """Interface for applying personality to responses"""
    
    @abstractmethod
    def apply_personality(
        self, base_response: Dict[str, Any], character: Character, topic: str
    ) -> Dict[str, Any]:
        """Apply character personality to a base response"""
        pass


class IMemoryManager(ABC):
    """Interface for managing character memory and context"""
    
    @abstractmethod
    def get_conversation_context(
        self, character: Character, topic: str, game_state: Any, player: Player = None
    ) -> List[Dict[str, str]]:
        """Get conversation context including memory and lore"""
        pass

    @abstractmethod
    def store_conversation(
        self, character: Character, topic: str, response: str
    ) -> None:
        """Store conversation in character memory"""
        pass


class ILoreRetriever(ABC):
    """Interface for retrieving game lore and context"""
    
    @abstractmethod
    def get_relevant_lore(
        self, game_state: Any, topic: str, player: Player, character: Character
    ) -> Optional[str]:
        """Get relevant lore information for a conversation"""
        pass
