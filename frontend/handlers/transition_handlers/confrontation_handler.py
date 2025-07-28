"""Handler pour les transitions vers la confrontation finale"""

from typing import Any, Tuple

import gradio as gr

from ...core.constants import ButtonStates, GameText, UIConstants
from ...core.logging_config import PerformanceTimer, transition_logger
from ...core.types import OptionalFacade
from .base_transition import BaseTransitionHandler
from ...services.image_preloader import get_special_image
from .button_handler import ButtonHandler

class ConfrontationHandler(BaseTransitionHandler):
    """Gère la transition vers la confrontation finale"""

    def can_handle(self, facade: OptionalFacade) -> bool:
        """Vérifie si la confrontation peut être démarrée"""
        return facade is not None and facade.get_attempts_remaining() > 0

    def execute(self, facade: OptionalFacade, chat_history) -> Tuple[Any, ...]:
        """
        Transition: Modal confirmation → FINAL_CONFRONTATION

        Args:
            facade: GameFacade instance

        Returns:
            Tuple of UI updates (8 elements)
        """
        if not self.can_handle(facade):
            transition_logger.error("Cannot start confrontation")
            return tuple(gr.update() for _ in range(UIConstants.MODAL_OUTPUTS))

        transition_logger.transition(
            "start_confrontation",
            current_location=facade.get_current_location(),
            attempts_before=facade.get_attempts_remaining(),
        )

        # Use attempt when entering confrontation
        attempt_used = facade.game_service.use_attempt()
        if attempt_used:
            remaining = facade.state.attempts_remaining
            transition_logger.info(
                "Attempt consumed for confrontation",
                attempts_remaining=remaining,
                attempts_used=facade.state.attempts_used,
            )
        else:
            transition_logger.warning("Could not use attempt - no attempts remaining")

        # Start the solve case process
        with PerformanceTimer("start_confrontation_dialogue", transition_logger):
            facade.game_service.start_final_confrontation()

            response = self._get_confrontation_intro_message(facade)

            chat_history.append({"role": "user", "content": "---------"})
            chat_history.append({
                "role": "assistant", 
                "content": response
            })

        # Get current state after action
        new_mode = facade.get_current_mode().value
        new_location = facade.get_current_location()
        attempts = facade.get_attempts_remaining()

        confrontation_img = get_special_image("confrontation")

        transition_logger.info(
            "Confrontation transition complete",
            new_mode=new_mode,
            location=new_location,
            attempts_remaining=attempts,
        )

        updated_inventory = facade.get_inventory()
        facade.toggle_inventory_view()

        # Return with type safety
        return (
            gr.update(
                visible=True,
                value=confrontation_img,
                label=GameText.CONFRONTATION_LABEL,
            ),
            gr.update(visible=False),  # room_map
            gr.update(visible=True, value=updated_inventory),
            facade,  # game_facade
            gr.update(visible=True, value=GameText.MAP_BUTTON),  # inventory_button
            ButtonHandler.update_main_action_button(new_mode, attempts),
            gr.update(
                interactive=ButtonStates.ENABLED
            ),  # inventory_button (reactivate)
            gr.update(interactive=ButtonStates.ENABLED), # settings_button (reactivate)
            chat_history
        )
    
    def _get_confrontation_intro_message(self, facade: OptionalFacade) -> str:
        """
        Generate the introduction message for the confrontation phase
    
        Args:
            facade: GameFacade instance
        
        Returns:
            Formatted message string for the chat
        """
        attempts_remaining = facade.get_attempts_remaining()
        player_name = facade.state.player_name if facade.state.player else "Detective"
    
        if attempts_remaining == 2:  # First try
            message = (
                f"🎭 **In the main salon of Blackwood Manor...**\n\n"
                f"You have gathered all the manor's inhabitants. "
                f"Inspector Ferdinand turns to you:\n\n"
                f"*\"So {player_name}, who is the culprit according to you?\"*"
            )
        elif attempts_remaining == 1:  # Second try
            message = (
                f"😤 **Second gathering...**\n\n"
                f"Inspector Ferdinand sighs:\n"
                f"*\"You already made us waste time once, {player_name}.\"*\n\n"
                f"The suspects seem annoyed to be summoned again.\n\n"
                f"*\"Well, who is the culprit according to you?\"*"
            )
        else:  # Last try
            message = (
                f"🚨 **Third gathering...**\n\n"
                f"Ferdinand sighs deeply:\n"
                f"*\"Listen {player_name}, this is your last chance.\"*\n\n"
                f"Everyone is visibly irritated.\n\n"
                f"*\"So, who is the culprit according to you?\"*"
            )
    
        return message
