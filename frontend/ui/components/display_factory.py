#!/usr/bin/env python3
"""Factory for creating display components - UI components only"""

import gradio as gr
from PIL import Image
from frontend.core.constants import CSSClasses, GameText, UIConstants

def create_room_view(intro_image: Image.Image) -> gr.Image:
    """Create the room view component"""
    return gr.Image(
        value=intro_image,
        label=GameText.INTRO_VIEW_LABEL,
        elem_id=CSSClasses.SCENE_IMG,
        visible=True,
        show_download_button=False
    )


def create_room_map(initial_map_image: Image.Image) -> gr.Image:
    """Create the room map component"""
    return gr.Image(
        value=initial_map_image,
        label=GameText.MANOR_MAP_LABEL,
        elem_id=CSSClasses.MAP_IMG,
        visible=True,
        show_download_button=False
    )


def create_inventory_display() -> gr.Textbox:
    """Create the inventory display component"""
    return gr.Textbox(
        label=GameText.INVENTORY_LABEL,
        elem_id=CSSClasses.INVENTORY_TEXT,
        visible=False,
        interactive=False,
        lines=UIConstants.INVENTORY_TEXT_LINES,
        max_lines=UIConstants.INVENTORY_TEXT_LINES,
    )
