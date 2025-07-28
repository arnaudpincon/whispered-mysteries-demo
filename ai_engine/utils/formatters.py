# === ÉTAPE 1.3: Adapter formatters.py pour être défensif ===
# Fichier: ai_engine/formatters.py

import logging
from typing import Any, Dict

# Setup logging
logger = logging.getLogger(__name__)


def format_game_state(game_state: Dict[str, Any]) -> str:
    """
    Converts the game state to text format for the prompt.
    Now handles both legacy and new GameState formats defensively.

    Args:
        game_state: Game state dictionary (from GameState.to_ai_format() or legacy format)

    Returns:
        Formatted text string for AI consumption
    """
    try:
        # Extract player data safely
        player_data = game_state.get("player", {})
        current_room_data = game_state.get("current_room", {})

        # Handle player information defensively
        if isinstance(player_data, dict):
            player_data.get("name", "Detective")
            current_location = player_data.get("location", "Unknown Location")
            inventory = player_data.get("inventory", [])
        else:
            # Fallback for legacy Player object
            getattr(player_data, "name", "Detective")
            current_location = getattr(
                player_data, "current_location", "Unknown Location"
            )
            inventory = getattr(player_data, "inventory", [])

            # Handle location object vs string
            if hasattr(current_location, "name"):
                current_location = current_location.name

        # Handle current room information
        if current_room_data:
            room_name = current_room_data.get("name", current_location)
            room_description = current_room_data.get(
                "description", "No description available"
            )
            characters_in_room = current_room_data.get("characters", [])
            clues_in_room = current_room_data.get("clues", [])
            room_exits = current_room_data.get("exits", [])
        else:
            # Fallback - try to extract from legacy format
            room_name = current_location
            room_description = "No description available"
            characters_in_room = []
            clues_in_room = []
            room_exits = []

            # Try to get room data from legacy player object
            if hasattr(player_data, "current_location"):
                legacy_room = player_data.current_location
                if hasattr(legacy_room, "name"):
                    room_name = legacy_room.name
                if hasattr(legacy_room, "description"):
                    room_description = legacy_room.description
                if hasattr(legacy_room, "characters"):
                    characters_in_room = [char.name for char in legacy_room.characters]
                if hasattr(legacy_room, "clues"):
                    clues_in_room = [clue.name for clue in legacy_room.clues]
                if hasattr(legacy_room, "exits"):
                    room_exits = legacy_room.exits


        character_display = []
        for char in characters_in_room:
            if isinstance(char, dict):
                name = char.get("name", "Unknown")
                status = char.get("status", "Unknown status")
                character_display.append(f"{name} ({status})")
            else:
                # Fallback pour format legacy (juste le nom)
                character_display.append(str(char))

        # Format inventory safely
        inventory_text = []
        for item in inventory:
            if isinstance(item, dict):
                item_name = item.get("name", "Unknown item")
                inventory_text.append(item_name)
            elif hasattr(item, "name"):
                inventory_text.append(item.name)
            else:
                inventory_text.append(str(item))

        # Extract lore information safely
        lore = game_state.get("lore", {})
        rooms_lore = lore.get("rooms", {}) if isinstance(lore, dict) else {}
        characters_lore = lore.get("characters", {}) if isinstance(lore, dict) else {}

        # Build the formatted text
        text = f"""
Current room: {room_name} - {room_description}

Present characters in the current room:
{', '.join(character_display) if character_display else "No characters present"}

Visible clues / objects:
{', '.join(clues_in_room) if clues_in_room else "No visible clues"}

Possible exits:
{', '.join(room_exits) if room_exits else "No exits"}

Player's inventory:
{', '.join(inventory_text) if inventory_text else "Empty inventory"}

Manor's rooms:
{', '.join(rooms_lore.keys()) if rooms_lore else "No room information available"}

Manor's characters:
{_format_characters_info(characters_lore)}
"""

        return text.strip()

    except Exception as e:
        logger.error(f"Error formatting game state: {e}")
        logger.error(f"Game state structure: {type(game_state)}")
        if isinstance(game_state, dict):
            logger.error(f"Game state keys: {list(game_state.keys())}")

        # Return minimal fallback
        return """
Current room: Unknown Location - Unable to format game state properly

Present characters in the current room:
No characters present

Visible clues / objects:
No visible clues

Possible exits:
No exits

Player's inventory:
Empty inventory

Manor's rooms:
No room information available

Manor's characters:
No character information available
"""


def _format_characters_info(characters_lore: Dict[str, Any]) -> str:
    """
    Format character information safely

    Args:
        characters_lore: Dictionary of character information

    Returns:
        Formatted string of character info
    """
    try:
        if not characters_lore:
            return "No character information available"

        character_info = []
        for name, info in characters_lore.items():
            if isinstance(info, dict):
                role = info.get("role", "Unknown role")
                location = info.get("location", "Unknown location")
                character_info.append(f"{name}: {role} (Location: {location})")
            else:
                character_info.append(f"{name}: {str(info)}")

        return ", ".join(character_info)

    except Exception as e:
        logger.error(f"Error formatting character info: {e}")
        return "Error formatting character information"


def clue_game_state(game_state: Dict[str, Any]) -> str:
    """
    Converts the game state to text format for clue-specific prompts.
    Updated to handle new format defensively.

    Args:
        game_state: Game state dictionary

    Returns:
        Formatted clue information string
    """
    try:
        # Extract current room clues safely
        current_room_data = game_state.get("current_room", {})
        clues_in_room = current_room_data.get("clues", [])

        # Fallback to legacy format if needed
        if not clues_in_room:
            player_data = game_state.get("player", {})
            if hasattr(player_data, "current_location"):
                legacy_room = player_data.current_location
                if hasattr(legacy_room, "clues"):
                    clues_in_room = [clue.name for clue in legacy_room.clues]

        text = f"""
Clues in the game:
{', '.join(clues_in_room) if clues_in_room else "No visible clues"}
"""
        return text.strip()

    except Exception as e:
        logger.error(f"Error formatting clue game state: {e}")
        return "Clues in the game:\nNo visible clues"


def validate_game_state_format(game_state: Any) -> bool:
    """
    Validate if game state is in expected format for formatting

    Args:
        game_state: Game state to validate

    Returns:
        True if format is valid for formatting
    """
    try:
        if not isinstance(game_state, dict):
            return False

        # Check for minimum required structure
        if "player" not in game_state:
            return False

        player_data = game_state["player"]
        if not isinstance(player_data, dict) and not hasattr(player_data, "name"):
            return False

        return True

    except Exception as e:
        logger.error(f"Error validating game state format: {e}")
        return False


def debug_game_state_structure(game_state: Any) -> Dict[str, Any]:
    """
    Debug helper to understand game state structure

    Args:
        game_state: Game state to analyze

    Returns:
        Dictionary with structure information
    """
    try:
        debug_info = {
            "type": str(type(game_state)),
            "is_dict": isinstance(game_state, dict),
            "has_to_ai_format": hasattr(game_state, "to_ai_format"),
        }

        if isinstance(game_state, dict):
            debug_info["keys"] = list(game_state.keys())
            debug_info["player_type"] = str(type(game_state.get("player", "not_found")))

        return debug_info

    except Exception as e:
        return {"error": str(e)}
