# game_engine/game_data.py
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from utils.markdown_utils import read_markdown_file

# Add parent directory to path to access models
sys.path.append(str(Path(__file__).parent.parent))

from game_engine.models.character import Character
from game_engine.models.clue import Clue
from game_engine.models.room import Room
from game_engine.models.secret_list import Secret


class GameDataLoader:
    """Loader for modular game data structure"""

    def __init__(self, data_dir: str = "data"):
        # Adjust path relative to game_engine directory
        self.data_dir = Path(__file__).parent.parent.parent / data_dir

    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON data from file"""
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _folder_name_to_snake_case(self, folder_name: str) -> str:
        """Convert folder name to snake_case for consistency"""
        return folder_name.lower().replace(" ", "_").replace("'", "")

    def load_room(self, room_folder_name: str) -> Room:
        """Load a single room from its folder structure"""
        room_dir = self.data_dir / "rooms" / room_folder_name

        # Load room info
        info = self._load_json(room_dir / "info.json")

        # Create room object
        room = Room(
            info["name"],
            info["description"],
            info["exits"],
            info["image"],
        )

        return room

    def load_clue(self, clue_folder_name: str) -> Clue:
        """Load a single clue from its folder structure"""
        clue_dir = self.data_dir / "clues" / clue_folder_name

        # Load clue info
        info = self._load_json(clue_dir / "info.json")

        # Create clue object
        clue = Clue(
            name=info["name"],
            description=info["description"],
            room_name=info["room_name"],
        )
        clue.is_collected = info.get("is_collected", False)

        return clue

    def load_character(self, character_folder_name: str) -> Character:
        """Load a single character from its folder structure"""
        char_dir = self.data_dir / "characters" / character_folder_name

        # Load basic info
        info = self._load_json(char_dir / "info.json")

        # Load secrets
        secrets_data = self._load_json(char_dir / "secrets.json")

        # Convert secrets to Secret objects
        secrets = []
        for secret_data in secrets_data["secrets"]:
            secret = Secret(
                condition=secret_data["condition"], secret=secret_data["secret"]
            )
            secrets.append(secret)

        # Load prompt from markdown file
        prompt = ""
        prompt_file = info.get("prompt_file", "prompt_memory.md")
        prompt_path = char_dir / prompt_file

        if prompt_path.exists():
            prompt = read_markdown_file(prompt_path)

        # Create character object
        character = Character(
            name=info["name"],
            role=info["role"],
            description=info["description"],
            information_to_disclose=info["information_to_disclose"],
            traits=info["traits"],
            secrets=secrets,
            possible_locations=info["possible_locations"],
            image_url=info["image_url"],
            prompt=prompt,
            status=info.get("status", "alive")
        )

        return character

    def load_all_rooms(self) -> List[Room]:
        """Load all rooms from their folder structure"""
        rooms_dir = self.data_dir / "rooms"
        rooms = []

        if not rooms_dir.exists():
            raise FileNotFoundError(f"Rooms directory not found: {rooms_dir}")

        # Get all room folders
        for room_folder in sorted(rooms_dir.iterdir()):
            if room_folder.is_dir() and (room_folder / "info.json").exists():
                try:
                    room = self.load_room(room_folder.name)
                    rooms.append(room)
                except Exception as e:
                    print(f"Error loading room {room_folder.name}: {e}")

        return rooms

    def load_all_clues(self) -> List[Clue]:
        """Load all clues from their folder structure"""
        clues_dir = self.data_dir / "clues"
        clues = []

        if not clues_dir.exists():
            raise FileNotFoundError(f"Clues directory not found: {clues_dir}")

        # Get all clue folders
        for clue_folder in sorted(clues_dir.iterdir()):
            if clue_folder.is_dir() and (clue_folder / "info.json").exists():
                try:
                    clue = self.load_clue(clue_folder.name)
                    clues.append(clue)
                except Exception as e:
                    print(f"Error loading clue {clue_folder.name}: {e}")

        return clues

    def load_all_characters(self) -> List[Character]:
        """Load all characters from their folder structure"""
        characters_dir = self.data_dir / "characters"
        characters = []

        if not characters_dir.exists():
            raise FileNotFoundError(f"Characters directory not found: {characters_dir}")

        # Get all character folders
        for char_folder in sorted(characters_dir.iterdir()):
            if char_folder.is_dir() and (char_folder / "info.json").exists():
                try:
                    character = self.load_character(char_folder.name)
                    characters.append(character)
                except Exception as e:
                    print(f"Error loading character {char_folder.name}: {e}")

        return characters


# Global loader instance
_loader = GameDataLoader()


def create_rooms() -> List[Room]:
    """Generate a list of rooms"""
    return _loader.load_all_rooms()


def create_clues() -> List[Clue]:
    """Generate a list of clues for the Blackwood Manor mystery"""
    return _loader.load_all_clues()


def create_characters() -> List[Character]:
    """Generate a list of characters"""
    return _loader.load_all_characters()


# Helper functions for loading specific items
def load_room_by_name(room_name: str) -> Room:
    """Load a specific room by its name"""
    folder_name = _loader._folder_name_to_snake_case(room_name)
    return _loader.load_room(folder_name)


def load_character_by_name(character_name: str) -> Character:
    """Load a specific character by their name"""
    folder_name = _loader._folder_name_to_snake_case(character_name)
    return _loader.load_character(folder_name)


def load_clue_by_name(clue_name: str) -> Clue:
    """Load a specific clue by its name"""
    folder_name = _loader._folder_name_to_snake_case(clue_name)
    return _loader.load_clue(folder_name)


# Configuration functions for different game scenarios
def load_tutorial_scenario() -> tuple[List[Room], List[Clue], List[Character]]:
    """Load a simplified tutorial scenario with fewer elements"""
    rooms = create_rooms()[:5]  # Only first 5 rooms
    clues = create_clues()[:10]  # Only first 10 clues
    characters = create_characters()[:3]  # Only first 3 characters
    return rooms, clues, characters


def load_full_scenario() -> tuple[List[Room], List[Clue], List[Character]]:
    """Load the complete game scenario"""
    return create_rooms(), create_clues(), create_characters()


def validate_data_integrity() -> bool:
    """Validate that all data loads correctly and references are valid"""
    try:
        rooms = create_rooms()
        clues = create_clues()
        characters = create_characters()

        room_names = {room.name for room in rooms}

        # Check that all clue locations exist
        for clue in clues:
            if clue.room_name not in room_names:
                print(
                    f"Warning: Clue '{clue.name}' references non-existent room '{clue.room_name}'"
                )
                return False

        # Check that all character locations exist
        for character in characters:
            for location in character.possible_locations:
                if location not in room_names:
                    print(
                        f"Warning: Character '{character.name}' references non-existent room '{location}'"
                    )
                    return False

        print(
            f"Data validation successful: {len(rooms)} rooms, {len(clues)} clues, {len(characters)} characters"
        )
        return True

    except Exception as e:
        print(f"Data validation failed: {e}")
        return False


if __name__ == "__main__":
    # Test the loader
    validate_data_integrity()