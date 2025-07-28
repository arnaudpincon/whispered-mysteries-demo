#!/usr/bin/env python3
"""Factory for creating modal components - UI components only"""

from typing import Tuple
import gradio as gr
from frontend.core.constants import GameText, CSSClasses, UIConstants



def create_confirmation_modal() -> Tuple[gr.Row, gr.Markdown, gr.Button, gr.Button]:
    """
    Create the solve case confirmation modal

    Returns:
        Tuple of (confirmation_modal, attempts_display, confirm_solve_btn, cancel_solve_btn)
    """

    # Confirmation modal for solve case
    with gr.Row(
        visible=False, elem_id=CSSClasses.CONFIRMATION_MODAL
    ) as confirmation_modal:
        with gr.Column(elem_id=CSSClasses.MODAL_CONTENT):
            gr.Markdown(GameText.SOLVE_CASE_MODAL_TITLE)
            gr.Markdown(GameText.SOLVE_CASE_MODAL_QUESTION)
            gr.Markdown(GameText.SOLVE_CASE_MODAL_REQUIREMENTS)
            attempts_display = gr.Markdown(
                f"**Attempts remaining: {UIConstants.MAX_ATTEMPTS}**",
                elem_id=CSSClasses.ATTEMPTS_DISPLAY,
            )

            with gr.Row(elem_id=CSSClasses.MODAL_BUTTONS):
                confirm_solve_btn = gr.Button(
                    GameText.CONFIRM_SOLVE_BUTTON,
                    variant="primary",
                    elem_id=CSSClasses.CONFIRM_SOLVE_BTN,
                )
                cancel_solve_btn = gr.Button(
                    GameText.CANCEL_SOLVE_BUTTON,
                    variant="secondary",
                    elem_id=CSSClasses.CANCEL_SOLVE_BTN,
                )

    return confirmation_modal, attempts_display, confirm_solve_btn, cancel_solve_btn
