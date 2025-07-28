#!/usr/bin/env python3
"""
Factory for creating enhanced settings modal with tab navigation and download
"""
from typing import Tuple
import gradio as gr

def create_settings_modal(handler_instance) -> Tuple[
    gr.Row,           # settings_modal
    gr.Button,        # save_load_tab_btn
    gr.Button,        # settings_tab_btn
    gr.Button,        # close_tab_btn
    gr.Column,        # save_load_content
    gr.Column,        # settings_content
    gr.Dropdown,      # language_dropdown
    gr.Checkbox,      # teleportation_checkbox
    gr.Markdown,      # status_display
    gr.Button,        # apply_button
    gr.File,          # load_file
    gr.Button,        # save_button
    gr.Button,        # load_button
    gr.Markdown,      # save_load_status
    gr.File           # download_file
]:
    """
    Create the enhanced settings modal with tab navigation and download support
    Returns:
        Tuple of all modal components including download_file
    """
    with gr.Row(visible=False, elem_id="settings-modal") as settings_modal:
        with gr.Column(elem_id="settings-modal-content"):
            gr.Markdown("## ☰ Menu")
            
            # === TAB NAVIGATION BUTTONS ===
            with gr.Row():
                settings_tab_btn = gr.Button(
                    "⚙️ Settings",
                    variant="primary",  # Active by default
                    scale=1
                )
                save_load_tab_btn = gr.Button(
                    "💾 Save/Load",
                    variant="secondary",
                    scale=1
                )
                close_tab_btn = gr.Button(
                    "❌ Close",
                    variant="secondary",
                    scale=1
                )
            
            # === SAVE/LOAD CONTENT (Hidden by default) ===
            with gr.Column(visible=False) as save_load_content:
                gr.Markdown("### 💾 Save & Load Game")
                
                # Save Section
                gr.Markdown("#### 📤 Save Game")
                gr.Markdown("Save your current progress to continue later")
                save_button = gr.Button(
                    "💾 Save Current Game",
                    variant="primary",
                    size="lg"
                )
                
                # Download Section
                download_file = gr.File(
                    label="Your save file is ready for download",
                    visible=False,
                    interactive=False,
                    file_count="single"
                )
                
                # Load Section
                gr.Markdown("#### 📥 Load Game")
                gr.Markdown("Load a previously saved game")
                load_file = gr.File(
                    label="Select Save File",
                    file_types=[".json"],
                    file_count="single"
                )
                load_button = gr.Button(
                    "📂 Load Selected Game",
                    variant="secondary",
                    size="lg",
                    interactive=False  # Disabled until file is selected
                )
                
                # Save/Load status display
                gr.Markdown("#### 📋 Status")
                save_load_status = gr.Markdown(
                    "**Status:** Ready to save or load",
                    elem_id="save-load-status"
                )
            
            # === SETTINGS CONTENT (Visible by default) ===
            with gr.Column(visible=True) as settings_content:
                # Language Section
                gr.Markdown("#### 🌐 Language")
                language_dropdown = gr.Dropdown(
                    choices=handler_instance.get_language_choices(),
                    value=handler_instance.get_current_language_for_dropdown(),
                    label="Language"
                )
                
                # Game Options Section
                gr.Markdown("#### 🎯 Game Options")
                teleportation_checkbox = gr.Checkbox(
                    label="Teleportation Mode",
                    info="Allow teleportation to any room without checking exits",
                    value=handler_instance.get_current_teleportation()
                )
                
                # Status Display
                gr.Markdown("#### 📊 Current Settings")
                status_display = gr.Markdown(
                    handler_instance.update_status_display()
                )
                
                # Apply button (only for settings)
                apply_button = gr.Button(
                    "✅ Apply Changes",
                    variant="primary",
                    size="lg"
                )
    
    return (
        settings_modal,
        save_load_tab_btn,
        settings_tab_btn,
        close_tab_btn,
        save_load_content,
        settings_content,
        language_dropdown,
        teleportation_checkbox,
        status_display,
        apply_button,
        load_file,
        save_button,
        load_button,
        save_load_status,
        download_file
    )


def create_tab_navigation_handlers():
    """
    Create handlers for tab navigation
    Returns functions for switching between tabs
    """
    
    def show_save_load_tab():
        """Show save/load content, hide settings content"""
        return (
            gr.update(visible=True),   # save_load_content
            gr.update(visible=False),  # settings_content
            gr.update(variant="primary"),    # save_load_tab_btn (active)
            gr.update(variant="secondary"),  # settings_tab_btn (inactive)
        )
    
    def show_settings_tab():
        """Show settings content, hide save/load content"""
        return (
            gr.update(visible=False),  # save_load_content
            gr.update(visible=True),   # settings_content
            gr.update(variant="secondary"),  # save_load_tab_btn (inactive)
            gr.update(variant="primary"),    # settings_tab_btn (active)
        )
    
    def close_modal():
        """Close the modal"""
        return gr.update(visible=False, elem_classes=[])  # settings_modal
    
    return show_save_load_tab, show_settings_tab, close_modal