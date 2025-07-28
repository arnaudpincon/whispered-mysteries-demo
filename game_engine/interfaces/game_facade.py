"""Unified interface between frontend and game engine"""

from typing import Any, Dict, List, Optional, Tuple

from game_engine.core.game_state import GameState
from game_engine.services.command_service import CommandService
from game_engine.services.game_service import GameService
from game_engine.services.save_service import SaveService
from game_engine.utils.error_handler import GameErrorHandler


class GameFacade:
    """Unified and simple interface for the frontend"""

    def __init__(self, ai_config: Dict[str, Any]):
        self.state = GameState()
        self.game_service = GameService(self.state, ai_config)

        # Create AI manager through game service
        ai_manager = self.game_service.ai_manager
        self.command_service = CommandService(self.state, self.game_service, ai_manager)

        # UI state (moved from GameState)
        self.show_inventory = False

        self.save_service = SaveService(self)

    def cleanup(self):
        """Clean up session resources"""
        try:
            if hasattr(self.state, 'cleanup_session'):
                self.state.cleanup_session()
            print(f"GameFacade cleaned up for session: {self.state.session_id}")
        except Exception as e:
            GameErrorHandler.handle_state_error(e, "session cleanup")

    def get_session_id(self) -> str:
        """Get the session ID for this game"""
        return self.state.session_id

    def start_game(self, player_name: str) -> str:
        """Start a new game with error handling"""
        try:
            return self.game_service.initialize_game(player_name)
        except Exception as e:
            error_response = GameErrorHandler.handle_command_error(e, f"start game: {player_name}", "game initialization")
            return error_response.get("message", "Failed to start game. Please try again.")

    def process_command(self, command: str) -> Dict[str, Any]:
        """Process a player command with error handling"""
        try:
            return self.command_service.process_command(command)
        except Exception as e:
            return GameErrorHandler.handle_command_error(e, command, "command processing")

    def get_current_state(self) -> Dict[str, Any]:
        """Get current state for UI with error handling"""
        try:
            state_dict = self.state.to_dict()
            state_dict["show_inventory"] = self.show_inventory
            return state_dict
        except Exception as e:
            GameErrorHandler.handle_state_error(e, "get current state")
            # Return minimal safe state
            return {
                "mode": "exploration",
                "location": "Main Hall",
                "game_running": True,
                "show_inventory": self.show_inventory,
                "error": True
            }

    def get_inventory(self) -> str:
        """Get inventory display with error handling"""
        try:
            return self.game_service.get_inventory_display()
        except Exception as e:
            error_msg = GameErrorHandler.handle_ai_error(e, "inventory display")
            return error_msg

    def toggle_inventory_view(self) -> bool:
        """Toggle inventory display"""
        self.show_inventory = not self.show_inventory
        return self.show_inventory

    def get_show_inventory(self) -> bool:
        """Check if inventory is shown"""
        return self.show_inventory

    # Accessors with error handling

    def get_current_mode(self):
        """Get current game mode"""
        return self.state.current_mode

    def get_current_location(self) -> str:
        """Get current location"""
        return self.state.current_location

    def get_attempts_remaining(self) -> int:
        """Get remaining attempts"""
        return self.state.attempts_remaining

    def is_game_running(self) -> bool:
        """Check if game is running"""
        return self.state.game_running

    def is_in_conversation(self) -> bool:
        """Check if in conversation"""
        return self.state.current_mode == self.state.current_mode.CONVERSATION

    def is_game_over(self) -> bool:
        """Check if game is over"""
        return self.state.current_mode == self.state.current_mode.GAME_OVER
    
    def export_save_data(self, chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Export complete game save data
        
        Args:
            chat_history: Chat interface history from Gradio
            
        Returns:
            Complete save data dictionary
        """
        try:
            return self.save_service.export_save(chat_history)
        except Exception as e:
            GameErrorHandler.handle_state_error(e, "save export")
            return {}
    
    def create_save_file(self, chat_history: List[Dict[str, str]], filename: Optional[str] = None) -> Optional[str]:
        """
        Create save file and return file path (legacy method for local saves)
        
        Args:
            chat_history: Chat interface history
            filename: Optional custom filename
            
        Returns:
            Path to created save file, or None if failed
        """
        try:
            return self.save_service.create_save_file(chat_history, filename)
        except Exception as e:
            GameErrorHandler.handle_state_error(e, "save file creation")
            return None
    
    def create_download_save(self, chat_history: List[Dict[str, str]], filename: Optional[str] = None) -> Optional[Tuple[str, str]]:
        """
        Create save file for download
        
        Args:
            chat_history: Chat interface history from Gradio
            filename: Optional custom filename
            
        Returns:
            Tuple[file_path: str, filename: str] or None if failed
        """
        try:
            return self.save_service.create_download_save(chat_history)
        except Exception as e:
            GameErrorHandler.handle_state_error(e, "download save creation")
            return None
    
    def get_save_info(self, save_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get displayable information about a save
        
        Args:
            save_data: Save data dictionary
            
        Returns:
            Save information for display
        """
        try:
            return self.save_service.get_save_info(save_data)
        except Exception as e:
            GameErrorHandler.handle_state_error(e, "save info extraction")
            return {"error": "Could not read save information"}
    
    def validate_save_data(self, save_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate save data format and integrity
        
        Args:
            save_data: Save data to validate
            
        Returns:
            Tuple[success: bool, message: str]
        """
        try:
            return self.save_service.import_save(save_data)
        except Exception as e:
            error_msg = f"Save validation failed: {e}"
            GameErrorHandler.handle_state_error(e, "save validation")
            return False, error_msg
    
    # Static save utilities
    
    @staticmethod
    def load_save_from_file(file_path: str) -> Tuple[bool, Dict[str, Any], str]:
        """
        Load save data from file (static method)
        
        Args:
            file_path: Path to save file
            
        Returns:
            Tuple[success: bool, save_data: dict, message: str]
        """
        return SaveService.load_save_from_file(file_path)
    
    @staticmethod
    def load_save_from_content(file_content: str) -> Tuple[bool, Dict[str, Any], str]:
        """
        Load save data from file content (static method for uploaded files)
        
        Args:
            file_content: JSON content as string
            
        Returns:
            Tuple[success: bool, save_data: dict, message: str]
        """
        return SaveService.load_save_from_content(file_content)
    
    @staticmethod
    def create_game_from_save(save_data: Dict[str, Any], ai_config: Dict[str, Any]) -> Tuple[Optional['GameFacade'], List[Dict[str, str]], str]:
        """
        Create a new GameFacade instance from save data
        
        Args:
            save_data: Complete save data
            ai_config: AI configuration for the new game
            
        Returns:
            Tuple[game_facade: GameFacade|None, chat_history: list, message: str]
        """
        try:
            # Validate save data first
            temp_service = SaveService()
            is_valid, validation_msg = temp_service.import_save(save_data)
            
            if not is_valid:
                return None, [], f"Invalid save data: {validation_msg}"
            
            # Create new GameFacade
            new_facade = GameFacade(ai_config)
            
            # Restore game state
            success, restore_msg = new_facade._restore_from_save_data(save_data)
            
            if not success:
                return None, [], f"Failed to restore game: {restore_msg}"
            
            # Extract chat history
            chat_history = save_data.get("display", {}).get("chat_history", [])
            
            return new_facade, chat_history, "Game restored successfully"
            
        except Exception as e:
            error_msg = f"Error creating game from save: {e}"
            GameErrorHandler.handle_state_error(e, "game restoration")
            return None, [], error_msg
    
    def _restore_from_save_data(self, save_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Internal method to restore game state from save data
        
        Args:
            save_data: Complete save data
            
        Returns:
            Tuple[success: bool, message: str]
        """
        try:
            # Restore basic game state
            self._restore_game_state(save_data["game_state"])

            # Restore rooms
            self._restore_rooms(save_data["rooms"])

            # Restore characters
            self._restore_characters(save_data["characters"])
            
            # Restore reputation
            self._restore_reputation(save_data["reputation"])
            
            # Restore UI state
            self._restore_ui_state(save_data["display"])
            
            return True, "Game state restored successfully"
            
        except Exception as e:
            return False, f"Restoration failed: {e}"
    
    def _restore_game_state(self, game_state_data: Dict[str, Any]) -> None:
        """Restore core game state"""
        from game_engine.core.game_state import GameMode
        
        # Restore basic state
        self.state.current_mode = GameMode(game_state_data["current_mode"])
        self.state.current_location = game_state_data["current_location"]
        self.state.player_name = game_state_data["player_name"]
        self.state.game_running = game_state_data["game_running"]
        self.state.attempts_remaining = game_state_data["attempts_remaining"]
        self.state.attempts_used = game_state_data["attempts_used"]
        self.state.ending_type = game_state_data["ending_type"]
        self.state.investigation_stage = game_state_data["investigation_stage"]
        self.state.character_in_conversation = game_state_data["character_in_conversation"]
        self.state.rooms_visited = set(game_state_data["rooms_visited"])
        self.state.characters_met = set(game_state_data["characters_met"])
        self.state.conclude_conversation = game_state_data["conclude_conversation"]
        self.state.lore = game_state_data["lore"]
        self.state.dev_mode = game_state_data["dev_mode"]
        
        # Restore player inventory
        self._restore_player_inventory(game_state_data["player_inventory"])
    
    def _restore_player_inventory(self, inventory_data: List[Dict[str, Any]]) -> None:
        """Restore player inventory"""
        from game_engine.models.clue import Clue
        from game_engine.models.player import Player
        
        # Create player if not exists
        if not self.state.player:
            self.state.player = Player(self.state.player_name)
        
        # Restore inventory items
        self.state.player.inventory = []
        for item_data in inventory_data:
            clue = Clue(
                name=item_data["name"],
                description=item_data["description"],
                room_name=item_data["room_name"]
            )
            clue.is_collected = item_data["is_collected"]
            self.state.player.inventory.append(clue)
    
    def _restore_characters(self, characters_data: Dict[str, Any]) -> None:
        """Restore all characters with their memories and states"""
        from game_engine.models.character import Character
        from game_engine.models.secret_list import Secret
        
        # Clear existing characters from rooms
        for room in self.state.rooms.values():
            room.characters = []
        
        # Restore each character
        for char_name, char_data in characters_data.items():
            basic_info = char_data["basic_info"]
            memory = char_data["memory"]
            secrets_data = char_data["secrets"]
            game_data = char_data["game_data"]
            
            # Create secrets
            secrets = []
            for secret_data in secrets_data:
                secret = Secret(secret_data["condition"], secret_data["secret"])
                secret.shown = secret_data["shown"]
                secrets.append(secret)
            
            # Create character
            character = Character(
                name=basic_info["name"],
                role=basic_info["role"],
                description=basic_info["description"],
                information_to_disclose=game_data["information_to_disclose"],
                traits=basic_info["traits"],
                secrets=secrets,
                possible_locations=game_data["possible_locations"],
                prompt=game_data["prompt"],
                image_url=basic_info["image_url"],
                status=basic_info["status"]
            )
            
            # Restore memories
            character.memory_global = memory["global_memory"]
            character.memory_current = memory["current_memory"]
            character.dialogues = char_data["dialogues"]
            
            # Place character in room
            current_location = basic_info["current_location"]
            if current_location in self.state.rooms:
                self.state.rooms[current_location].add_character(character)
    
    def _restore_reputation(self, reputation_data: Dict[str, Any]) -> None:
        """Restore reputation system"""
        from game_engine.models.reputation import GlobalReputation, ReputationSeverity, ReputationEvent
        
        # Create new reputation system
        self.state.reputation = GlobalReputation()
        
        # Restore room events
        for room_name, room_data in reputation_data["rooms"].items():
            for event_data in room_data["events"]:
                severity = ReputationSeverity(event_data["severity"])
                event = ReputationEvent(
                    command=event_data["command"],
                    severity=severity,
                    timestamp=event_data["timestamp"],
                    room_name=event_data["room_name"],
                    summary=event_data["summary"]
                )
                self.state.reputation.get_room(room_name).add_event(event)
    
    def _restore_rooms(self, rooms_data: Dict[str, Any]) -> None:
        """Restore rooms and their states"""
        from game_engine.models.room import Room
        from game_engine.models.clue import Clue
        
        self.state.rooms = {}
        
        for room_name, room_data in rooms_data.items():
            # Create room
            room = Room(
                name=room_data["name"],
                description=room_data["description"],
                exits=room_data["exits"],
                image_url=room_data["image_url"]
            )
            
            # Add remaining clues
            for clue_data in room_data["clues_present"]:
                if not clue_data["is_collected"]:  # Only non-collected clues
                    clue = Clue(
                        name=clue_data["name"],
                        description=clue_data["description"],
                        room_name=clue_data["room_name"]
                    )
                    room.add_clue(clue)
            
            self.state.rooms[room_name] = room
        
        # Set player location
        if self.state.player and self.state.current_location in self.state.rooms:
            self.state.player.current_location = self.state.rooms[self.state.current_location]
    
    def _restore_ui_state(self, display_data: Dict[str, Any]) -> None:
        """Restore UI state"""
        ui_state = display_data.get("ui_state", {})
        self.show_inventory = ui_state.get("show_inventory", False)