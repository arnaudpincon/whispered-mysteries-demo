"""
Abstract interfaces for theory processing components
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class IFinalSceneHandler(ABC):
    """Interface for handling final scene interactions"""
    
    @abstractmethod
    def handle_final_scene(
        self, player: Any, conversation: List[Dict[str, str]], game_state: Any
    ) -> Dict[str, Any]:
        """Assist the player in completing their murder theory"""
        pass


class ITheoryVerifier(ABC):
    """Interface for verifying detective theories"""
    
    @abstractmethod
    def verify_theory(self, conversation: List[Dict[str, str]]) -> Dict[str, Any]:
        """Verify the detective's theory against possible scenarios"""
        pass


class IEndingWriter(ABC):
    """Interface for writing game endings"""
    
    @abstractmethod
    def write_ending(self, scenario: int, player_theory: str) -> Dict[str, Any]:
        """Generate the ending based on the player's theory and scenario"""
        pass