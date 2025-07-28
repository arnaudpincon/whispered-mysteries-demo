"""
Save Service for Detective Game - Enhanced with download functionality
Handles export and import of game state with automatic download support
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import tempfile
import os

from game_engine.core.game_state import GameState, GameMode
from game_engine.models.character import Character
from game_engine.models.player import Player
from game_engine.models.reputation import GlobalReputation, ReputationSeverity


class SaveService:
    """Service for handling complete game save/load operations with download support"""
    
    SAVE_VERSION = "1.0"
    SUPPORTED_VERSIONS = ["1.0"]
    
    def __init__(self, game_facade=None):
        """
        Initialize SaveService
        
        Args:
            game_facade: GameFacade instance (None for loading saves)
        """
        self.game_facade = game_facade
    
    # Main public methods
    
    def export_save(self, chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Export complete game save
        
        Args:
            chat_history: Chat interface history from Gradio
            
        Returns:
            Complete save data dictionary
            
        Raises:
            Exception: If game_facade is None or export fails
        """
        if not self.game_facade:
            raise Exception("Cannot export save: no active game")
        
        try:
            save_data = {
                "metadata": self._create_metadata(),
                "display": self._export_display_data(chat_history),
                "game_state": self._export_game_state(),
                "characters": self._export_characters(),
                "reputation": self._export_reputation(),
                "rooms": self._export_rooms_state()
            }
            
            # Validate export before returning
            if self._validate_save_data(save_data):
                return save_data
            else:
                raise Exception("Save validation failed")
                
        except Exception as e:
            print(f"Export failed: {e}")
            raise
    
    def import_save(self, save_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Import and validate save data
        
        Args:
            save_data: Save data dictionary
            
        Returns:
            Tuple[success: bool, message: str]
        """
        try:
            # Validate save format and version
            is_valid, error_msg = self._validate_save_format(save_data)
            if not is_valid:
                return False, f"Invalid save format: {error_msg}"
            
            # Version compatibility check
            save_version = save_data["metadata"]["version"]
            if save_version not in self.SUPPORTED_VERSIONS:
                return False, f"Unsupported save version: {save_version}"
            
            print(f"Save validation successful (version {save_version})")
            return True, "Save loaded successfully"
            
        except Exception as e:
            error_msg = f"Import failed: {e}"
            print(error_msg)
            return False, error_msg
    
    def create_download_save(self, chat_history: List[Dict[str, str]], filename: Optional[str] = None) -> Tuple[str, str]:
        save_data = self.export_save(chat_history)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            player_name = self.game_facade.state.player_name.replace(" ", "_")
            current_room = self.game_facade.get_current_location().replace(" ", "_")
            filename = f"BlackwoodManorSave-{player_name}-{current_room}-{timestamp}.json"
        
        # Create temp name
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            print(f"Save prepared for download: {filename}")
            return temp_path, filename
            
        except Exception as e:
            # Clean up if writing fails
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            except:
                pass
            raise e
    
    def create_save_file(self, chat_history: List[Dict[str, str]], filename: Optional[str] = None) -> str:
        """
        Create save file in local directory (legacy method for backward compatibility)
        
        Args:
            chat_history: Chat interface history
            filename: Optional custom filename
            
        Returns:
            Path to created save file
        """
        save_data = self.export_save(chat_history)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            player_name = self.game_facade.state.player_name.replace(" ", "_")
            current_room = self.game_facade.get_current_location().replace(" ", "_")
            filename = f"BlackwoodManorSave-{player_name}-{current_room}-{timestamp}.json"
        
        # Ensure saves directory exists
        saves_dir = Path("saves")
        saves_dir.mkdir(exist_ok=True)
        
        save_path = saves_dir / filename
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"Save created: {save_path}")
        return str(save_path)
    
    # Export methods
    
    def _create_metadata(self) -> Dict[str, Any]:
        """Create save metadata"""
        return {
            "version": self.SAVE_VERSION,
            "timestamp": datetime.now().isoformat(),
            "game_version": "1.0",  # Could be from config
            "player_name": self.game_facade.state.player_name,
            "session_id": self.game_facade.state.session_id,
            "creation_info": {
                "current_location": self.game_facade.state.current_location,
                "current_mode": self.game_facade.state.current_mode.value,
                "attempts_remaining": self.game_facade.state.attempts_remaining,
                "game_running": self.game_facade.state.game_running
            }
        }
    
    def _export_display_data(self, chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Export display and UI related data"""
        return {
            "chat_history": chat_history,
            "ui_state": {
                "show_inventory": self.game_facade.show_inventory,
                "current_view": "inventory" if self.game_facade.show_inventory else "map"
            },
            "chat_metadata": {
                "message_count": len(chat_history),
                "last_message_timestamp": time.time()
            }
        }
    
    def _export_game_state(self) -> Dict[str, Any]:
        """Export core game state"""
        state = self.game_facade.state
        
        return {
            "current_mode": state.current_mode.value,
            "current_location": state.current_location,
            "player_name": state.player_name,
            "game_running": state.game_running,
            "attempts_remaining": state.attempts_remaining,
            "attempts_used": state.attempts_used,
            "ending_type": state.ending_type,
            "investigation_stage": state.investigation_stage,
            "character_in_conversation": state.character_in_conversation,
            "rooms_visited": list(state.rooms_visited),
            "characters_met": list(state.characters_met),
            "conclude_conversation": state.conclude_conversation,
            "lore": state.lore,
            "dev_mode": state.dev_mode,
            "player_inventory": self._export_player_inventory()
        }
    
    def _export_player_inventory(self) -> List[Dict[str, Any]]:
        """Export player inventory"""
        if not self.game_facade.state.player or not self.game_facade.state.player.inventory:
            return []
        
        inventory = []
        for item in self.game_facade.state.player.inventory:
            inventory.append({
                "name": item.name,
                "description": item.description,
                "room_name": item.room_name,
                "is_collected": item.is_collected
            })
        
        return inventory
    
    def _export_characters(self) -> Dict[str, Any]:
        """Export all characters with their memories and states"""
        characters_data = {}
        
        for room_name, room in self.game_facade.state.rooms.items():
            for character in room.characters:
                characters_data[character.name] = {
                    "basic_info": {
                        "name": character.name,
                        "role": character.role,
                        "description": character.description,
                        "traits": character.traits,
                        "status": character.status,
                        "current_location": room_name,
                        "image_url": character.image_url
                    },
                    "memory": {
                        "global_memory": character.memory_global,
                        "current_memory": character.memory_current
                    },
                    "secrets": [
                        {
                            "condition": secret.condition,
                            "secret": secret.secret,
                            "shown": secret.shown
                        }
                        for secret in character.secrets
                    ],
                    "dialogues": character.dialogues,
                    "game_data": {
                        "information_to_disclose": character.information_to_disclose,
                        "possible_locations": character.possible_locations,
                        "prompt": character.prompt
                    }
                }
        
        return characters_data
    
    def _export_reputation(self) -> Dict[str, Any]:
        """Export reputation system state"""
        reputation = self.game_facade.state.reputation
        
        reputation_data = {
            "rooms": {},
            "global_status": {
                "impromptu_global": reputation.is_global_reputation(ReputationSeverity.IMPROMPTU),
                "awkward_global": reputation.is_global_reputation(ReputationSeverity.AWKWARD),
                "dangerous_global": reputation.is_global_reputation(ReputationSeverity.DANGEROUS)
            }
        }
        
        # Export room-specific reputation
        for room_name, room_rep in reputation.rooms.items():
            reputation_data["rooms"][room_name] = {
                "events": [
                    {
                        "command": event.command,
                        "severity": event.severity.value,
                        "timestamp": event.timestamp,
                        "room_name": event.room_name,
                        "summary": event.summary
                    }
                    for event in room_rep.events
                ]
            }
        
        return reputation_data
    
    def _export_rooms_state(self) -> Dict[str, Any]:
        """Export rooms and their current state"""
        rooms_data = {}
        
        for room_name, room in self.game_facade.state.rooms.items():
            rooms_data[room_name] = {
                "name": room.name,
                "description": room.description,
                "exits": room.exits,
                "image_url": room.image_url,
                "characters_present": [char.name for char in room.characters],
                "clues_present": [
                    {
                        "name": clue.name,
                        "description": clue.description,
                        "room_name": clue.room_name,
                        "is_collected": clue.is_collected
                    }
                    for clue in room.clues
                ]
            }
        
        return rooms_data
    
    # Validation methods
    
    def _validate_save_format(self, save_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate save data format and required fields"""
        required_top_level = ["metadata", "display", "game_state", "characters", "reputation"]
        
        # Check top-level structure
        for field in required_top_level:
            if field not in save_data:
                return False, f"Missing required field: {field}"
        
        # Check metadata
        metadata = save_data["metadata"]
        required_metadata = ["version", "timestamp", "player_name"]
        for field in required_metadata:
            if field not in metadata:
                return False, f"Missing metadata field: {field}"
        
        # Check game_state essential fields
        game_state = save_data["game_state"]
        required_game_state = ["current_mode", "current_location", "player_name"]
        for field in required_game_state:
            if field not in game_state:
                return False, f"Missing game_state field: {field}"
        
        return True, "Valid format"
    
    def _validate_save_data(self, save_data: Dict[str, Any]) -> bool:
        """Validate exported save data integrity"""
        try:
            # Check that all characters have valid data
            characters = save_data["characters"]
            for char_name, char_data in characters.items():
                if not all(key in char_data for key in ["basic_info", "memory", "secrets"]):
                    print(f"Character {char_name} missing required data")
                    return False
            
            # Check that current location exists in rooms
            current_location = save_data["game_state"]["current_location"]
            if current_location not in save_data["rooms"]:
                print(f"Current location {current_location} not found in rooms")
                return False
            
            # Check chat history format
            chat_history = save_data["display"]["chat_history"]
            if not isinstance(chat_history, list):
                print("Chat history is not a list")
                return False
            
            print("Save data validation successful")
            return True
            
        except Exception as e:
            print(f"Save validation error: {e}")
            return False
    
    # Utility methods
    
    def get_save_info(self, save_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract save information for display purposes"""
        try:
            metadata = save_data["metadata"]
            creation_info = metadata.get("creation_info", {})
            
            return {
                "player_name": metadata.get("player_name", "Unknown"),
                "timestamp": metadata.get("timestamp", "Unknown"),
                "version": metadata.get("version", "Unknown"),
                "current_location": creation_info.get("current_location", "Unknown"),
                "attempts_remaining": creation_info.get("attempts_remaining", 0),
                "game_running": creation_info.get("game_running", False),
                "message_count": save_data["display"].get("chat_metadata", {}).get("message_count", 0)
            }
        except Exception as e:
            print(f"Error extracting save info: {e}")
            return {"error": "Could not read save information"}
    
    @staticmethod
    def load_save_from_file(file_path: str) -> Tuple[bool, Dict[str, Any], str]:
        """
        Load save data from file
        
        Args:
            file_path: Path to save file
            
        Returns:
            Tuple[success: bool, save_data: dict, message: str]
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            print(f"Loaded save from: {file_path}")
            return True, save_data, "File loaded successfully"
            
        except FileNotFoundError:
            return False, {}, f"Save file not found: {file_path}"
        except json.JSONDecodeError as e:
            return False, {}, f"Invalid JSON format: {e}"
        except Exception as e:
            return False, {}, f"Error loading file: {e}"
    
    @staticmethod
    def load_save_from_content(file_content: str) -> Tuple[bool, Dict[str, Any], str]:
        """
        Load save data from file content (for uploaded files)
        
        Args:
            file_content: JSON content as string
            
        Returns:
            Tuple[success: bool, save_data: dict, message: str]
        """
        try:
            save_data = json.loads(file_content)
            
            print("Loaded save from uploaded content")
            return True, save_data, "Save loaded successfully"
            
        except json.JSONDecodeError as e:
            return False, {}, f"Invalid JSON format: {e}"
        except Exception as e:
            return False, {}, f"Error parsing save content: {e}"


# Convenience functions

def create_save_service(game_facade=None) -> SaveService:
    """Factory function to create SaveService instance"""
    return SaveService(game_facade)


def quick_download_save(game_facade, chat_history: List[Dict[str, str]], filename: Optional[str] = None) -> Tuple[str, str]:
    """
    Quick save function for download
    
    Args:
        game_facade: GameFacade instance
        chat_history: Chat history from Gradio
        filename: Optional custom filename
        
    Returns:
        Tuple[file_path: str, filename: str] - Temporary file path and suggested filename
    """
    save_service = SaveService(game_facade)
    return save_service.create_download_save(chat_history)


def quick_load_from_content(file_content: str) -> Tuple[bool, Dict[str, Any], str]:
    """
    Quick load function from file content
    
    Args:
        file_content: JSON content as string
        
    Returns:
        Tuple[success: bool, save_data: dict, message: str]
    """
    return SaveService.load_save_from_content(file_content)