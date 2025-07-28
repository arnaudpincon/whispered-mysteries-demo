"""
Abstract interfaces for story processing components
"""

from abc import ABC, abstractmethod
from typing import Any, Optional, List
from game_engine.models.room import Room
from game_engine.models.character import Character


class IRoomDescriptionGenerator(ABC):
    """Interface for generating room descriptions"""
    
    @abstractmethod
    def generate_description(self, room: Room, game_state: Any, action: str) -> str:
        """Generate an atmospheric description of a room"""
        pass


class ICharacterDescriptionGenerator(ABC):
    """Interface for generating character descriptions"""
    
    @abstractmethod
    def generate_description(self, character: Character, room: Room) -> str:
        """Generate a description of a character"""
        pass


class IClueAnalyzer(ABC):
    """Interface for analyzing clues"""
    
    @abstractmethod
    def analyze_clue(self, clue: Any, collected_clues: Optional[List] = None) -> str:
        """Analyze a clue and provide insights"""
        pass


class IObjectInspector(ABC):
    """Interface for inspecting non-clue objects"""
    
    @abstractmethod
    def inspect_object(self, object_name: str) -> str:
        """Inspect a useless object and provide a response"""
        pass