"""Refactored GameService - Main orchestrator with simplified dependencies"""

from typing import Any, Dict

from ai_engine.core.ai_manager import AIManager
from game_engine.core.game_state import GameState
from game_engine.services.confrontation_service import ConfrontationService
from game_engine.services.conversation_service import ConversationService
from game_engine.services.exploration_service import ExplorationService
from game_engine.services.memory_service import MemoryService
from game_engine.services.reputation_service import ReputationService
from game_engine.setup.game_setup import setup_game
from utils.markdown_utils import read_markdown_file


class GameService:
    """Main game orchestrator with simplified dependencies"""

    def __init__(self, state: GameState, ai_config: Dict[str, Any]):
        self.state = state

        # Initialize AIManager with configuration
        ai_manager_params = {
            "api_key": ai_config.get("api_key"),
            "endpoint": ai_config.get("endpoint"),
            "deployment_name": ai_config.get("deployment_name"),
            "api_version": ai_config.get("api_version"),
            "session_id": state.session_id,
        }
        self.ai_manager = AIManager(**ai_manager_params)

        # Store dev_mode for game logic
        self.dev_mode = ai_config.get("dev_mode", False)
        self.state.dev_mode = self.dev_mode

        # Initialize services - order is important
        self.reputation_service = ReputationService(state.reputation)
        self.memory_service = MemoryService(state, self.ai_manager, self.reputation_service)
        self.conversation_service = ConversationService(state, self.ai_manager)
        self.exploration_service = ExplorationService(state, self.ai_manager)
        self.confrontation_service = ConfrontationService(state, self.ai_manager)

    def initialize_game(self, player_name: str) -> str:
        """Initialize a new game session"""
        # Setup game world
        rooms, player = setup_game(player_name)

        # Update game state
        self.state.rooms = rooms
        self.state.player = player
        self.state.player_name = player_name
        self.state.game_running = True

        if player and player.current_location:
            self.state.current_location = player.current_location.name
            self.state.rooms_visited.add(self.state.current_location)

        # Populate lore information
        self._populate_lore_data(rooms)

        # Load and return intro text
        intro = read_markdown_file("data/narratives/documents/intro.md")
        return intro

    # Delegation methods

    def start_conversation(self, character_name: str) -> bool:
        """Start conversation without complex reputation logic"""
        success = self.conversation_service.start_conversation(character_name)
        if success:
            # Simple reputation update - no complex cross-service calls
            character = self.conversation_service._find_character_in_current_room(character_name)
            if character:
                self._add_reputation_to_character_memory(character)
        return success
    
    def _add_reputation_to_character_memory(self, character) -> None:
        """Add reputation context to character memory"""
        memory_context = self.reputation_service.get_character_memory_context(self.state.current_location)
        
        # Add global reputation context
        for global_memory in memory_context["global_memories"]:
            character.remember(global_memory, "assistant")

    def end_conversation(self) -> bool:
        """Delegate to conversation service"""
        return self.conversation_service.end_conversation()

    def process_conversation(self, character_name: str, topic: str) -> str:
        """Delegate to conversation service"""
        return self.conversation_service.process_conversation(character_name, topic)

    def move_player(self, room_name: str) -> bool:
        """Delegate to exploration service"""
        return self.exploration_service.move_player(room_name)

    def process_look_action(self, target: str, target_type: str) -> str:
        """Delegate to exploration service"""
        return self.exploration_service.process_look_action(target, target_type)

    def get_inventory_display(self) -> str:
        """Delegate to exploration service"""
        return self.exploration_service.get_inventory_display()

    def start_final_confrontation(self) -> bool:
        """Delegate to confrontation service"""
        return self.confrontation_service.start_final_confrontation()

    def process_final_confrontation(self, user_input: str) -> str:
        """Delegate to confrontation service"""
        return self.confrontation_service.process_final_confrontation(user_input)

    def use_attempt(self) -> bool:
        """Delegate to confrontation service"""
        return self.confrontation_service.use_attempt()

    def trigger_game_over(self, ending_type: int = 0) -> None:
        """Delegate to confrontation service"""
        self.confrontation_service.trigger_game_over(ending_type)

    def process_nonsense_action(self, command: str) -> Dict[str, Any]:
        """Pure delegation to memory service"""
        return self.memory_service.process_nonsense_action(command)
    
    def refresh_all_character_memories(self) -> None:
        """Refresh global memories for all characters"""
        self.memory_service.refresh_all_character_global_memories()

    # Private helper methods

    def _populate_lore_data(self, rooms: Dict[str, Any]) -> None:
        """Populate lore data from rooms and characters for AI context"""
        for room_id, room in rooms.items():
            self.state.lore["rooms"][room.name] = room.description

            for character in room.characters:
                self.state.lore["characters"][character.name] = {
                    "role": character.role,
                    "description": character.description,
                    "traits": character.traits,
                    "location": room.name,
                }

    def _find_character_in_current_room(self, character_name: str):
        """Helper method for backwards compatibility"""
        return self.conversation_service._find_character_in_current_room(character_name)

    def _get_characters_in_current_room(self):
        """Helper method for backwards compatibility"""
        return self.exploration_service._get_characters_in_current_room()