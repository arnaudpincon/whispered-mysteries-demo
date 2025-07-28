#!/usr/bin/env python3
"""Factory for creating control buttons - UI components only"""

from typing import Tuple
import gradio as gr
from frontend.core.constants import ButtonStates, CSSClasses, GameText



def create_control_buttons() -> Tuple[gr.Button, gr.Button, gr.Button]:
    """
    Create the three main control buttons for the detective game

    Returns:
        Tuple of (inventory_button, conclude_button, settings_button)
    """

    inventory_button: gr.Button = gr.Button(
        GameText.BRIEFCASE_BUTTON,
        elem_id=CSSClasses.INVENTORY_BUTTON_ID,
        variant="secondary",
        scale=1,
        interactive=ButtonStates.DISABLED,
    )

    conclude_button: gr.Button = gr.Button(
        GameText.SOLVE_CASE_BUTTON,
        elem_id=CSSClasses.CONCLUDE_BUTTON_ID,
        variant="secondary",
        scale=1,
        interactive=ButtonStates.DISABLED,
    )

    settings_button: gr.Button = gr.Button(
        GameText.SETTINGS_BUTTON,
        elem_id=CSSClasses.SETTINGS_BUTTON_ID,
        variant="secondary",
        scale=1,
        interactive=ButtonStates.ENABLED,
    )

    return inventory_button, conclude_button, settings_button
