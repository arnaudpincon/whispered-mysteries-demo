"""Common utility functions for game operations"""

from typing import Any, Dict, List, Optional
from game_engine.models.character import Character
from game_engine.models.room import Room


class GameUtils:
    """Utility functions for common game operations"""

    @staticmethod
    def find_character_by_name(characters: List[Character], name: str) -> Optional[Character]:
        """
        Find character by name (case insensitive)
        
        Args:
            characters: List of characters to search
            name: Name to search for
            
        Returns:
            Character if found, None otherwise
        """
        name_lower = name.lower()
        for character in characters:
            if character.name.lower() == name_lower:
                return character
        return None

    @staticmethod
    def get_characters_in_room(room: Room) -> List[Character]:
        """
        Get all characters in a room safely
        
        Args:
            room: Room to check
            
        Returns:
            List of characters (empty if room has no characters)
        """
        if not room or not hasattr(room, 'characters'):
            return []
        return room.characters

    @staticmethod
    def format_character_list(characters: List[Character]) -> str:
        """
        Format a list of characters for display
        
        Args:
            characters: List of characters
            
        Returns:
            Formatted string of character names
        """
        if not characters:
            return "No one is here."
        
        names = [char.name for char in characters]
        if len(names) == 1:
            return f"{names[0]} is here."
        elif len(names) == 2:
            return f"{names[0]} and {names[1]} are here."
        else:
            return f"{', '.join(names[:-1])}, and {names[-1]} are here."

    @staticmethod
    def validate_room_transition(current_room: Room, target_room_name: str) -> bool:
        """
        Validate if player can move to target room
        
        Args:
            current_room: Current room object
            target_room_name: Name of target room
            
        Returns:
            True if transition is valid
        """
        if not current_room or not hasattr(current_room, 'exits'):
            return False
        
        return target_room_name in current_room.exits

    @staticmethod
    def safe_get_attribute(obj: Any, attribute: str, default: Any = None) -> Any:
        """
        Safely get an attribute from an object
        
        Args:
            obj: Object to get attribute from
            attribute: Attribute name
            default: Default value if attribute doesn't exist
            
        Returns:
            Attribute value or default
        """
        return getattr(obj, attribute, default)

    @staticmethod
    def format_inventory_item(item, index: int) -> str:
        """
        Format an inventory item for display
        
        Args:
            item: Inventory item
            index: Item index
            
        Returns:
            Formatted item string
        """
        return f"{index + 1}. {item.name.upper()} — Found in {item.room_name}\n   {item.description}"