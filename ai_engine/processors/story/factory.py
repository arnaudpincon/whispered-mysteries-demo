"""
Factory for creating story processing components
"""

from typing import Tuple

from .room_description import RoomDescriptionGenerator
from .character_description import CharacterDescriptionGenerator
from .clue_analyzer import ClueAnalyzer
from .object_inspector import ObjectInspector


class StoryComponentFactory:
    """Factory for creating story processing components"""
    
    @staticmethod
    def create_standard_setup(
        api_service, 
        cache, 
        dev_mode: bool = False
    ) -> Tuple[
        RoomDescriptionGenerator,
        CharacterDescriptionGenerator, 
        ClueAnalyzer,
        ObjectInspector
    ]:
        """
        Create a standard story processing setup
        
        Args:
            api_service: API service instance
            cache: Cache manager instance
            dev_mode: Enable development mode features
            
        Returns:
            Tuple of all story processing components
        """
        
        # Create all components
        room_generator = RoomDescriptionGenerator(api_service, cache, dev_mode)
        character_generator = CharacterDescriptionGenerator(api_service, cache, dev_mode)
        clue_analyzer = ClueAnalyzer(api_service, cache, dev_mode)
        object_inspector = ObjectInspector(api_service, cache, dev_mode)
        
        return room_generator, character_generator, clue_analyzer, object_inspector