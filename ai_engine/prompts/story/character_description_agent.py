"""
Character Description Agent
Generates descriptions of characters in their environment
"""

from ai_engine.prompts.prompt_config import get_rules_prompt
from game_engine.models.character import Character
from game_engine.models.room import Room


def create_character_description_prompt(character: Character, room: Room) -> str:
    """
    Create a simple, direct prompt for character description.
    
    Args:
        character: Character to describe
        room: Room where the character is located
        
    Returns:
        Formatted prompt for character description
    """
    rules_prompt = get_rules_prompt()
    
    character_info = _extract_character_info(character)
    room_info = _extract_room_info(room)
    description_guidelines = _get_description_guidelines()
    
    return f"""
        Describe {character.name} to the player (detective) who is observing them.
        
        In one short sentence, describe what {character.name} looks like.
       
        In a second sentence, describe what {character.name} is currently doing or their demeanor.
       
        Address the player directly using "you" when relevant (e.g., "You see that...", "You notice...").
        
        {character_info}
        {room_info}
       
        {description_guidelines}
        {rules_prompt}
    """


def _extract_character_info(character: Character) -> str:
    """Extract and format character information"""
    return f"""This is the role of the character: {character.role}
        This is the status of the character: {character.status}
        This is the physical description of the character: {character.description}
        This is the personnality of the character: {character.traits}"""


def _extract_room_info(room: Room) -> str:
    """Extract and format room information"""
    return f"""The player and {room.name} are in this current room of the manor: {room.name}
        This is the description of the room: {room.description}"""


def _get_description_guidelines() -> str:
    """Get the description writing guidelines"""
    return """Rules:
        - Be simple and direct
        - No flowery language or unnecessary adjectives
        - Describe only what would be immediately noticeable
        - Maximum two or three sentences total
        - Avoid being verbose or pompous
        - Focus on clarity over style
        - Show their personality through actions, not exposition
        - Address the player as "you" when describing what they perceive"""