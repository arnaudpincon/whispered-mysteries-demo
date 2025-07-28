"""Handler for game mode transitions"""

from typing import Any, Dict

from game_engine.core.game_state import GameMode

from ...core.constants import GameText
from ...core.logging_config import PerformanceTimer, transition_logger
from ...core.types import OptionalFacade
from .base_transition import BaseTransitionHandler


class ModeTransitionHandler(BaseTransitionHandler):
    """Manages transitions between different game modes"""

    def can_handle(self, facade: OptionalFacade) -> bool:
        """Check if mode transition is possible"""
        return facade is not None

    def execute(self, facade: OptionalFacade) -> Any:
        """Execute appropriate transition based on context"""
        if not self.can_handle(facade):
            return {"message": GameText.NO_ACTIVE_GAME}

        current_mode = facade.get_current_mode()
        attempts = facade.get_attempts_remaining()

        if current_mode == GameMode.CONVERSATION:
            return self.exit_conversation(facade)
        elif current_mode == GameMode.FINAL_CONFRONTATION:
            if attempts <= 0:
                return self.abandon_investigation(facade)
            else:
                return self.return_to_exploration(facade)
        else:
            # Exploration mode - should show modal
            return None  # Handled by modal handler

    def exit_conversation(self, facade: OptionalFacade) -> Dict[str, Any]:
        """Transition: CONVERSATION → EXPLORATION (via goodbye message)"""
        if facade is None:
            transition_logger.error("No facade for exit conversation")
            return {"message": GameText.NO_ACTIVE_GAME}

        character_name = facade.state.character_in_conversation
        transition_logger.transition(
            "exit_conversation",
            character=character_name,
            goodbye_message=GameText.GOODBYE_MESSAGE,
        )

        with PerformanceTimer("exit_conversation_chat", transition_logger):
            response = facade.process_command(GameText.GOODBYE_MESSAGE)

        return response

    def return_to_exploration(self, facade: OptionalFacade) -> str:
        """Transition: FINAL_CONFRONTATION → EXPLORATION"""
        if facade is None:
            transition_logger.error("No facade for exploration transition")
            return GameText.NO_ACTIVE_GAME

        transition_logger.transition(
            "return_to_exploration",
            from_mode="FINAL_CONFRONTATION",
            reason="user_requested",
        )

        # Change mode directly in state
        facade.state.current_mode = GameMode.EXPLORATION

        transition_logger.info("Successfully returned to exploration mode")
        return GameText.TRANSITION_TO_EXPLORATION

    def abandon_investigation(self, facade: OptionalFacade, chat_history) -> Dict[str, Any]:
        """Transition: FINAL_CONFRONTATION → GAME_OVER (abandon investigation)"""
        if facade is None:
            transition_logger.error("No facade for game over transition")
            return {"message": GameText.NO_ACTIVE_GAME}

        attempts_used = facade.state.attempts_used
        transition_logger.transition(
            "abandon_investigation",
            attempts_used=attempts_used,
            reason="user_abandoned",
        )

        with PerformanceTimer("abandon_investigation", transition_logger):
            # Trigger game over with ending type 0 (fail)
            facade.game_service.trigger_game_over(ending_type=0)
            
            # Generate ending with AI - this will create the narrative message
            ending_response = facade.game_service.ai_manager.write_ending(
                scenario=0, 
                player_theory="The detective abandoned the investigation"
            )
            
            transition_logger.info("AI ending generated", 
                                   ending_type=0, 
                                   message_length=len(ending_response.get("answer", "")))
            
            # Extract the AI-generated message from the ending response
            ai_message = ending_response.get("answer", "Investigation abandoned. The truth of Blackwood Manor remains buried in shadows...")

            # Add messages directly to chat history
            chat_history.append({"role": "user", "content": "---"})
            chat_history.append({
                "role": "assistant", 
                "content": ai_message  # This is the AI-generated ending message
            })
            
            # Return complete response structure for UI
            response = {
                "location": facade.state.current_location,
                "room_image_url": "",
                "message": ai_message,  # This is the AI-generated ending message
                "mode": GameMode.GAME_OVER.value,
                "character_in_conversation": "",
                "character_image_url": "",
                "ending": 0,
            }

        return response