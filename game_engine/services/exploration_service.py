"""Service dedicated to exploration actions (move, look, collect)"""
from typing import List
from ai_engine.core.ai_manager import AIManager
from game_engine.core.game_state import GameState
from game_engine.models.character import Character


class ExplorationService:
    """Handles all exploration-related actions"""

    def __init__(self, state: GameState, ai_manager: AIManager):
        self.state = state
        self.ai_manager = ai_manager

    def move_player(self, room_name: str) -> bool:
        """
        Move player to a new room with synchronized state and player location
       
        Args:
            room_name: Name of room to move to
        Returns:
            True if move was successful
        """
        new_room = self.state.rooms.get(room_name)
        if not new_room or not self.state.player:
            return False

        # Add previous room to visited rooms when leaving
        self.state.rooms_visited.add(self.state.current_location)

        # Update both state and player location consistently
        self.state.current_location = room_name  # State location (string)
        self.state.player.current_location = new_room  # Player location (Room object)

        return True

    def process_look_action(self, target: str, target_type: str) -> str:
        """
        Process look/examine actions

        Args:
            target: What to look at
            target_type: Type of target (inventory, location, clue, character, etc.)

        Returns:
            Description of what was examined
        """
        if target_type == "inventory":
            return self.get_inventory_display()
        elif target_type == "location" and target == self.state.current_location:
            # Use unified room access
            room = self.state.get_current_room()
            if room:
                return self.ai_manager.generate_room_description(room, self.state, action="look")
            else:
                return f"You are in {self.state.current_location}."
        elif target_type in ["clue", "object"]:
            is_clue = self.state.player.collect_clue(target)
            if is_clue:
                clue = self.state.player.inventory[-1]
                analysis = self.ai_manager.analyze_clue(
                    clue, self.state.player.inventory
                )
                return f"\n{analysis}"
            else:
                answer = self.ai_manager.give_useless_answer(target)
                return f"\n{answer}"
        elif target_type == "character":
            characters = self._get_characters_in_current_room()
            for character in characters:
                if character.name.lower() == target.lower():
                    # Use unified room access
                    room = self.state.get_current_room()
                    return self.ai_manager.generate_character_description(
                        character, room
                    )
            return f"You don't see {target} here."
        else:
            return "You see nothing special about that."

    def get_inventory_display(self) -> str:
        """
        Get formatted inventory display text

        Returns:
            Formatted string of inventory items
        """
        if not self.state.player or not self.state.player.inventory:
            return "You have no collected clues yet."

        description = ""
        for item in self.state.player.inventory:
            description += f"\n{item.name.upper()} — Found in {item.room_name}\n {item.description}\n"

        return description

    def _get_characters_in_current_room(self) -> List[Character]:
        """Get all characters in current room using unified access"""
        current_room = self.state.get_current_room()
        if current_room:
            return current_room.characters
        return []