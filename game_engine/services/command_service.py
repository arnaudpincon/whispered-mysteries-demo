"""Service for processing player commands and routing to appropriate handlers"""

import json
from typing import Any, Callable, Dict

from ai_engine.core.ai_manager import AIManager
from game_engine.core.game_state import GameState
from game_engine.services.game_service import GameService
from game_engine.core.game_state import GameMode


class CommandService:
    """Processes and executes player commands with routing map"""

    def __init__(
        self, state: GameState, game_service: GameService, ai_manager: AIManager
    ):
        self.state = state
        self.game_service = game_service
        self.ai_manager = ai_manager

        self.exploration_handlers = {
            "look": self._handle_look_action,
            "move": self._handle_move_action,
            "speak": self._handle_speak_action,
            "collect": self._handle_collect_action,
            "conclude": self._handle_conclude_action,
            "nonsense": self._handle_nonsense_action
        }

    def process_command(self, command: str) -> Dict[str, Any]:
        """
        Process a player command and return response

        Args:
            command: Player's input command in any language

        Returns:
            Dictionary containing the game response
        """
        # Base response structure
        response = self._create_base_response()

        if command.lower() == "quit":
            self.state.game_running = False
            return response

        # Route to appropriate mode handler
        if self.state.current_mode == GameMode.CONVERSATION:
            return self._handle_conversation_mode(command, response)
        elif self.state.current_mode == GameMode.FINAL_CONFRONTATION:
            return self._handle_confrontation_mode(command, response)
        else:  # EXPLORATION
            return self._handle_exploration_mode(command, response)

    def _create_base_response(self) -> Dict[str, Any]:
        """Create base response structure"""
        return {
            "location": self.state.current_location,
            "room_image_url": self._get_room_image_url(),
            "message": "",
            "mode": self.state.current_mode.value,
            "character_in_conversation": self.state.character_in_conversation,
            "character_image_url": self._get_character_image_url(),
            "ending": self.state.ending_type,
        }

    def _handle_conversation_mode(
        self, command: str, response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle commands in conversation mode"""
        character_response = self.game_service.process_conversation(
            self.state.character_in_conversation, command
        )

        response["message"] = character_response

        # Check if conversation ended (GameService handles mode change)
        response["mode"] = self.state.current_mode.value
        if self.state.current_mode == GameMode.EXPLORATION:
            response["character_in_conversation"] = ""
            response["character_image_url"] = ""

        return response

    def _handle_confrontation_mode(
        self, command: str, response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle commands in final confrontation mode"""
        confrontation_response = self.game_service.process_final_confrontation(command)
        response["message"] = confrontation_response

        # Update mode if game ended
        response["mode"] = self.state.current_mode.value
        if self.state.current_mode == GameMode.GAME_OVER:
            response["ending"] = self.state.ending_type

        return response

    def _handle_exploration_mode(
        self, command: str, response: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Process command with AI
        result = self.ai_manager.process_command(command, self.state)
        action = result["action"]
        handler = self.exploration_handlers.get(action)
        
        # Fix for nonsense actions
        if (handler and result["valid"]) or (handler and action == "nonsense"):
            return handler(result, response)
        else:
            # Default case for unknown actions
            response["message"] = result["message"]
            return response

    # Individual action handlers for better organization

    def _handle_look_action(self, ai_result: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle look/examine actions"""
        target = ai_result["target"]
        target_type = ai_result["target_type"]
        
        response["message"] = self.game_service.process_look_action(target, target_type)
        return response

    def _handle_move_action(self, ai_result: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle movement actions"""
        target = ai_result["target"]
        
        if self.game_service.move_player(target):
            # Update response with new location info
            response["location"] = self.state.current_location
            response["room_image_url"] = self._get_room_image_url()
            room_description = self.ai_manager.generate_room_description(
                self.state.player.current_location, self.state, action="move"
            )
            response["message"] = room_description
        else:
            response["message"] = ai_result["message"]
        
        return response

    def _handle_speak_action(self, ai_result: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle conversation initiation - show AI message only"""
        target = ai_result["target"]
        
        if self.game_service.start_conversation(target):
            if self.state.dev_mode:
                print(f"You are now in conversation mode with {target}.")

            # Show the AI-generated message for conversation initiation
            response["message"] = ai_result["message"]
            response["mode"] = self.state.current_mode.value
            response["character_in_conversation"] = self.state.character_in_conversation
            response["character_image_url"] = self._get_character_image_url()
        else:
            response["message"] = f"I don't see {target} in this room."
        
        return response

    def _handle_collect_action(self, ai_result: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle item collection"""
        target = ai_result["target"]
        
        is_clue = self.state.player.collect_clue(target)

        if is_clue:
            clue = self.state.player.inventory[-1]
            analysis = self.ai_manager.analyze_clue(clue, self.state.player.inventory)
            response["message"] = f"\n{analysis}"
        else:
            answer = self.ai_manager.give_useless_answer(target)
            response["message"] = f"\n{answer}"
        
        return response

    def _handle_conclude_action(self, ai_result: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle final confrontation initiation"""
        if self.state.dev_mode:
            print("----- Confrontation Mode -----")

        if self.game_service.start_final_confrontation():
            confrontation_response = self.game_service.process_final_confrontation(
                ai_result["message"]
            )
            response["message"] = confrontation_response
            response["mode"] = self.state.current_mode.value

            if self.state.current_mode == GameMode.GAME_OVER:
                response["ending"] = self.state.ending_type
        else:
            response["message"] = "You have no attempts remaining."
        
        return response

    def _handle_nonsense_action(self, ai_result: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle nonsense actions"""
        nonsense_result = self.game_service.process_nonsense_action(ai_result["translated_command"])
        
        # Check if game over due to expulsion
        if nonsense_result.get("game_over", False):
            response["message"] = nonsense_result["message"]
            response["mode"] = GameMode.GAME_OVER.value
            response["ending"] = self.state.ending_type
            return response
        
        response["message"] = nonsense_result["message"]
        
        # Enhanced dev mode output for reputation system
        if self.state.dev_mode:
            self._debug_reputation_status(ai_result, nonsense_result)
        
        return response

    def _debug_reputation_status(self, ai_result: Dict[str, Any], nonsense_result: Dict[str, Any]) -> None:
        """Debug output using new reputation system"""
        print(f"REPUTATION UPDATE:")
        print(f"   Command: {ai_result['translated_command']}")
        print(f"   Severity: {nonsense_result['severity']}")
        
        # Get status from NEW system
        reputation_status = self.game_service.reputation_service.get_status(self.state.current_location)
        
        # Display room-specific counts
        room_counts = reputation_status.get('room_counts', {})
        print(f"   Room Counts ({self.state.current_location}):")
        print(f"     Impromptu: {room_counts.get('impromptu', 0)}/5 (local) /10 (global)")
        print(f"     Awkward: {room_counts.get('awkward', 0)}/3 (local) /5 (global)")
        print(f"     Dangerous: {room_counts.get('dangerous', 0)}/1 (local) /2 (global)")
        
        # Display reputation status
        local_status = reputation_status.get('local_status', {})
        global_status = reputation_status.get('global_status', {})
        print(f"   Local Status ({self.state.current_location}):")
        print(f"     Impromptu: {local_status.get('impromptu', False)}")
        print(f"     Awkward: {local_status.get('awkward', False)}")
        print(f"     Dangerous: {local_status.get('dangerous', False)}")
        print(f"   Global Status:")
        print(f"     Impromptu: {global_status.get('impromptu', False)}")
        print(f"     Awkward: {global_status.get('awkward', False)}")
        print(f"     Dangerous: {global_status.get('dangerous', False)}")
        
        # Display warnings
        warnings = nonsense_result.get('warnings', [])
        if warnings:
            print(f"   Warnings:")
            for warning in warnings:
                print(f"     • {warning}")
        
        # Show NEW reputation stats
        total_status = self.game_service.reputation_service.get_status()
        print(f"REPUTATION STATS:")
        print(f"   Total events: {sum(total_status['total_counts'].values())}")
        print(f"   Rooms with reputation: {len(total_status['rooms_with_reputation']['dangerous'])}")
    
    def _get_room_image_url(self) -> str:
        """Get current room image URL"""
        current_room = self.state.get_current_room()
        if current_room and hasattr(current_room, "image_url"):
            return current_room.image_url
        return ""

    def _get_character_image_url(self) -> str:
        """Get current character image URL"""
        if self.state.character_in_conversation:
            character = self.game_service._find_character_in_current_room(
                self.state.character_in_conversation
            )
            if character and hasattr(character, "image_url"):
                return character.image_url
        return ""