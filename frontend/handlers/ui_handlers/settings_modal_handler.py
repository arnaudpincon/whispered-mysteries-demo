#!/usr/bin/env python3
"""
Settings Modal Handler - Simple session-based like language service
"""

from typing import Any, Tuple
import gradio as gr

from frontend.core.logging_config import ui_logger
from frontend.services.language_service import get_language_service
from frontend.services.game_option_service import get_game_options_service


class SettingsModalHandler:
    """Manages settings modal interactions and state updates"""
    
    def __init__(self):
        self.language_service = get_language_service()
        self.game_options_service = get_game_options_service()
        ui_logger.debug("Settings modal handler initialized")
    
    @staticmethod
    def show_settings_modal() -> Any:
        """Show the settings modal"""
        ui_logger.info("Showing settings modal")
        return gr.update(visible=True, elem_classes=["modal-visible"])
    
    @staticmethod
    def hide_settings_modal() -> Any:
        """Hide the settings modal"""
        ui_logger.debug("Hiding settings modal")
        return gr.update(visible=False, elem_classes=[])
    
    @staticmethod
    def apply_settings_changes(
        selected_language: str, 
        teleportation_enabled: bool, 
        current_language_state: str, 
        current_teleportation_state: bool
    ) -> Tuple[Any, str, str, bool]:
        """
        Apply both language and teleportation changes
        """
        ui_logger.user_action("settings_change_requested", 
                             language=selected_language, 
                             teleportation=teleportation_enabled)
        
        language_service = get_language_service()
        game_options_service = get_game_options_service()
        
        try:
            # Apply language change
            language_success = language_service.set_language(selected_language)
            
            # Apply teleportation change  
            teleportation_success = game_options_service.set_teleportation_mode(teleportation_enabled)
            
            if language_success and teleportation_success:
                # Both changes succeeded
                language_display = language_service.get_current_language_display()
                teleportation_display = game_options_service.get_teleportation_display()
                
                combined_message = f"**Language:** {language_display}\n\n**Teleportation mode:** {teleportation_display}"
                
                ui_logger.info("All settings changes applied successfully")
                
                # Hide modal and update states
                return (
                    gr.update(visible=False, elem_classes=[]),
                    combined_message,
                    selected_language,  # new language state
                    teleportation_enabled  # new teleportation state
                )
            else:
                # At least one change failed
                error_message = "**Error:** Failed to apply some settings. Please try again."
                ui_logger.error("Settings change failed")
                
                # Keep modal open
                return (
                    gr.update(visible=True, elem_classes=["modal-visible"]),
                    error_message,
                    current_language_state,
                    current_teleportation_state
                )
                
        except Exception as e:
            error_message = "**Error:** An unexpected error occurred."
            ui_logger.error("Exception during settings change", error=str(e))
            
            # Keep modal open on exception
            return (
                gr.update(visible=True, elem_classes=["modal-visible"]),
                error_message,
                current_language_state,
                current_teleportation_state
            )
    
    def get_current_language_for_dropdown(self) -> str:
        """Get current language code for dropdown value"""
        return self.language_service.get_current_language()
    
    def get_language_choices(self) -> list:
        """Get language choices for dropdown"""
        return self.language_service.get_language_choices()
    
    def get_current_teleportation(self) -> bool:
        """Get current teleportation mode for checkbox"""
        return self.game_options_service.get_teleportation_mode()
    
    def update_status_display(self) -> str:
        """Update combined status display"""
        language_display = self.language_service.get_current_language_display()
        teleportation_display = self.game_options_service.get_teleportation_display()
        
        return f"**Language:** {language_display}\n\n**Teleportation mode:** {teleportation_display}"
    
    def update_game_options_status(self) -> str:
        """Update game options status display"""
        teleportation_enabled = self.game_options_service.get_teleportation_mode()
        teleportation_display = "Enabled" if teleportation_enabled else "Disabled"
        
        return f"**Teleportation mode:** {teleportation_display}"


def create_settings_modal_factory() -> SettingsModalHandler:
    """Factory function to create settings modal handler"""
    return SettingsModalHandler()