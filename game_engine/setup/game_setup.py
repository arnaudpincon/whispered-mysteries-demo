import random
from typing import Dict, List, Tuple

from game_engine.setup.game_data import create_characters, create_clues, create_rooms
from game_engine.models.character import Character
from game_engine.models.clue import Clue
from game_engine.models.player import Player
from game_engine.models.room import Room


def setup_game(name: str) -> Tuple[Dict[str, Room], Player]:
    """Set up the game world dynamically, placing characters in specific rooms from their possible locations."""

    # Create game elements
    rooms: List[Room] = create_rooms()
    clues: List[Clue] = create_clues()
    characters: List[Character] = create_characters()

    room_dict: Dict[str, Room] = {room.name: room for room in rooms}

    # Place characters in their designated possible locations
    for character in characters:
        # Filter to valid locations that exist in the room dictionary
        valid_locations: List[str] = [
            loc for loc in character.possible_locations if loc in room_dict
        ]

        # If no valid locations, default to "Main Hall"
        if not valid_locations:
            valid_locations = ["Main Hall"]

        # Pick a random room from the valid locations
        room_name: str = random.choice(valid_locations)
        room: Room = room_dict[room_name]

        # Place the character in the room
        room.add_character(character)

    # Place clues in their specific rooms
    for clue in clues:
        room_name: str = clue.room_name
        room: Room = room_dict.get(room_name)
        if room:
            room.add_clue(clue)
        else:
            print(f"Warning: Room {room_name} not found for clue {clue}")

    # Ask for player's detective name
    detective_name = name

    # Create player and set initial position
    player: Player = Player("Detective " + detective_name)
    player.current_location = room_dict["Main Hall"]

    return room_dict, player
