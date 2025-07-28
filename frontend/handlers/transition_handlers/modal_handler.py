"""Handler for modal management"""
""" Display or Hide the modal for Solve Case button """

from typing import Any, Tuple

import gradio as gr

from ...core.logging_config import transition_logger
from ...core.types import OptionalFacade
from .base_transition import BaseTransitionHandler


class ModalHandler(BaseTransitionHandler):
    """Manages modal display and hiding"""

    def can_handle(self, facade: OptionalFacade) -> bool:
        """Always can handle modal operations"""
        return True

    def execute(self, facade: OptionalFacade) -> Any:
        """Not used for modal handler - use specific methods"""

    @staticmethod
    def show_solve_case_modal(attempts: int) -> Tuple[Any, Any]:
        """Show the solve case confirmation modal"""
        transition_logger.info("Showing solve case modal", attempts_remaining=attempts)

        if attempts == 1:
            transition_logger.warning("Last attempt warning displayed")
            attempts_text = f"""**Attempts remaining: {attempts}**

<div class="last-attempt-warning">
⚠️ **This is your last chance!** ⚠️<br/>
Choose carefully - this is your final attempt to solve the case.
</div>"""
        else:
            attempts_text = f"**Attempts remaining: {attempts}**"

        return (
            gr.update(visible=True, elem_classes=["modal-visible"]),
            gr.update(value=attempts_text),
        )

    @staticmethod
    def hide_solve_case_modal() -> Any:
        """Hide the solve case confirmation modal"""
        transition_logger.debug("Hiding solve case modal")
        return gr.update(visible=False, elem_classes=[])
