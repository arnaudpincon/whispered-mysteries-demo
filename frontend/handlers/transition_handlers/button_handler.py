"""Handler pour la gestion des états des boutons"""

from typing import Any

import gradio as gr

from ...core.constants import ButtonStates, GameModes, GameText
from ...core.logging_config import transition_logger
from ...core.types import OptionalFacade
from .base_transition import BaseTransitionHandler


class ButtonHandler(BaseTransitionHandler):
    """Gère les états et mises à jour des boutons"""

    def can_handle(self, facade: OptionalFacade) -> bool:
        """Always can handle button operations"""
        return True

    def execute(self, facade: OptionalFacade) -> Any:
        """Not used for button handler - use specific methods"""

    @staticmethod
    def update_main_action_button(current_mode: str, attempts: int) -> Any:
        """
        Update main action button text and state based on game mode and attempts

        Args:
            current_mode: Current game mode string
            attempts: Number of attempts remaining

        Returns:
            Gradio update for the main action button
        """
        transition_logger.debug(
            "Updating main action button", mode=current_mode, attempts=attempts
        )

        if current_mode == GameModes.CONVERSATION:
            return gr.update(
                value=GameText.QUIT_CONVERSATION_BUTTON,
                variant="secondary",
                interactive=ButtonStates.ENABLED,
            )
        elif current_mode == GameModes.FINAL_CONFRONTATION:
            if attempts <= 0:
                transition_logger.warning(
                    "No attempts remaining - showing abandon option"
                )
                return gr.update(
                    value=GameText.ABANDON_INVESTIGATION_BUTTON,
                    variant="secondary",
                    interactive=ButtonStates.ENABLED,
                )
            else:
                return gr.update(
                    value=GameText.RETURN_TO_INVESTIGATION_BUTTON,
                    variant="secondary",
                    interactive=ButtonStates.ENABLED,
                )
        elif current_mode == GameModes.GAME_OVER:
            transition_logger.info("Game over - disabling solve button")
            return gr.update(
                value=GameText.SOLVE_CASE_BUTTON,
                variant="secondary",
                interactive=ButtonStates.DISABLED,
            )
        else:  # EXPLORATION
            return gr.update(
                value=GameText.SOLVE_CASE_BUTTON,
                variant="secondary",
                interactive=ButtonStates.ENABLED,
            )
