"""
Main StoryProcessor - Clean interface with refactored components
"""

import logging
from typing import Any, Dict, List, Optional

from ai_engine.processors.base_processor import BaseProcessor
from game_engine.core.game_state import GameState
from game_engine.models.character import Character
from game_engine.models.room import Room

from .factory import StoryComponentFactory

logger = logging.getLogger(__name__)


class StoryProcessor(BaseProcessor):
    """
    Refactored Story Processor - Now acts as a lightweight coordinator
    
    Responsibilities:
    1. Coordinate story generation components
    2. Provide backward-compatible interface
    3. Handle high-level story flow
    """
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        super().__init__(api_service, cache, dev_mode)
        
        # Create story components using factory
        (self.room_generator, 
         self.character_generator,
         self.clue_analyzer,
         self.object_inspector) = StoryComponentFactory.create_standard_setup(
            api_service, cache, dev_mode
        )
        
        self._log_debug("StoryProcessor initialized with refactored components")
    
    def get_processor_name(self) -> str:
        return "story"

    def generate_room_description(self, room: Room, game_state: GameState, action: str) -> str:
        """
        Generates an atmospheric description of a room.
        Now delegated to specialized component.

        Args:
            room: Room to describe (contains its own nonsense history)
            game_state: Current game state
            action: Action being performed

        Returns:
            Atmospheric description of the room
        """
        self._log_debug(f"Generating room description for: {room.name if room else 'Unknown'}")
        
        try:
            return self.room_generator.generate_description(room, game_state, action)
        except Exception as e:
            self.logger.error(f"Error in generate_room_description: {e}")
            room_name = getattr(room, 'name', 'an unknown location')
            return f"You find yourself in {room_name}."

    def generate_character_description(self, character: Character, room: Room) -> str:
        """
        Generates a description of a character.
        Now delegated to specialized component.

        Args:
            character: Character to describe
            room: Room where the character is located

        Returns:
            Description of the character
        """
        self._log_debug(f"Generating character description for: {character.name if character else 'Unknown'}")
        
        try:
            return self.character_generator.generate_description(character, room)
        except Exception as e:
            self.logger.error(f"Error in generate_character_description: {e}")
            character_name = getattr(character, 'name', 'someone')
            return f"You inspect {character_name}. There is nothing special to note."

    def analyze_clue(self, clue: Any, collected_clues: Optional[List] = None) -> str:
        """
        Analyzes a clue and gives insights to the player.
        Now delegated to specialized component.

        Args:
            clue: Clue to analyze
            collected_clues: Optional list of previously collected clues

        Returns:
            Analysis of the clue
        """
        self._log_debug(f"Analyzing clue: {getattr(clue, 'name', 'Unknown clue')}")
        
        try:
            return self.clue_analyzer.analyze_clue(clue, collected_clues)
        except Exception as e:
            self.logger.error(f"Error in analyze_clue: {e}")
            return "This clue seems significant, but its meaning eludes me for now."

    def give_useless_answer(self, object_name: str) -> str:
        """
        Give a simple answer for a useless object.
        Now delegated to specialized component.
        
        Args:
            object_name: Name of the object to inspect
            
        Returns:
            Simple response about the object
        """
        self._log_debug(f"Inspecting useless object: {object_name}")
        
        try:
            return self.object_inspector.inspect_object(object_name)
        except Exception as e:
            self.logger.error(f"Error in give_useless_answer: {e}")
            return "There is nothing special."
    
    def health_check(self) -> Dict[str, Any]:
        """Check the health of story processor components"""
        return {
            "processor_name": self.get_processor_name(),
            "room_generator": self.room_generator is not None,
            "character_generator": self.character_generator is not None,
            "clue_analyzer": self.clue_analyzer is not None,
            "object_inspector": self.object_inspector is not None,
            "api_service": self.api_service is not None,
            "cache": self.cache is not None,
            "dev_mode": self.dev_mode
        }