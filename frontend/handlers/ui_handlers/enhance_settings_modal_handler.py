#!/usr/bin/env python3
"""
Enhanced Settings Modal Handler - With Save/Load functionality including DOWNLOAD
"""

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Tuple, Optional

import gradio as gr

from frontend.core.logging_config import ui_logger
from frontend.services.language_service import get_language_service
from frontend.services.game_option_service import get_game_options_service
from game_engine.interfaces.game_facade import GameFacade


class EnhancedSettingsModalHandler:
    """Manages settings modal interactions including save/load functionality with download"""
    
    def __init__(self):
        self.language_service = get_language_service()
        self.game_options_service = get_game_options_service()
        ui_logger.debug("Enhanced settings modal handler initialized")
    
    # ===== DISPLAY METHODS =====
    
    @staticmethod
    def show_settings_modal() -> Any:
        """Show the settings modal"""
        ui_logger.info("Showing enhanced settings modal")
        return gr.update(visible=True, elem_classes=["modal-visible"])
    
    @staticmethod
    def hide_settings_modal() -> Any:
        """Hide the settings modal"""
        ui_logger.debug("Hiding enhanced settings modal")
        return gr.update(visible=False, elem_classes=[])
    
    # ===== SETTINGS METHODS (unchanged) =====
    
    @staticmethod
    def apply_settings_changes(
        selected_language: str, 
        teleportation_enabled: bool, 
        current_language_state: str, 
        current_teleportation_state: bool
    ) -> Tuple[Any, str, str, bool]:
        """Apply both language and teleportation changes"""
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
    
    # ===== NEW SAVE/LOAD METHODS WITH DOWNLOAD =====
    
    @staticmethod
    def handle_save_game(game_facade, chat_history) -> Tuple[Any, str]:
        """
        Handle save game request with automatic download
        
        Args:
            game_facade: Current GameFacade instance
            chat_history: Current chat history
            
        Returns:
            Tuple[download_file_update, status_message]
        """
        try:
            if not game_facade:
                return gr.update(visible=False), "**❌ Error:** No active game to save."
            
            ui_logger.user_action("save_game_requested")
            
            # ✅ NOUVEAU: Utilise la nouvelle méthode de téléchargement
            result = game_facade.create_download_save(chat_history)
            
            if result:
                file_path, filename = result
                
                # Get file size for display
                file_size = Path(file_path).stat().st_size
                size_kb = file_size / 1024
                
                ui_logger.info("Game save prepared for download", 
                              filename=filename, 
                              size_kb=size_kb)
                
                # Return file for download
                return (
                    gr.update(value=file_path, visible=True),  # Le fichier temporaire pour download
                    f"**✅ Success:** Save ready for download: `{filename}` ({size_kb:.1f} KB)"
                )
            else:
                return gr.update(visible=False), "**❌ Error:** Failed to create save file."
                
        except Exception as e:
            error_msg = f"Save failed: {str(e)}"
            ui_logger.error("Save game error", error=error_msg)
            return gr.update(visible=False), f"**❌ Error:** {error_msg}"
    
    @staticmethod
    def handle_file_upload(file_info) -> Tuple[Any, str]:
        """
        Handle save file upload and enable/disable load button
        
        Args:
            file_info: Gradio file upload info
            
        Returns:
            Tuple[load_button_update, status_message]
        """
        try:
            if file_info is None:
                return (
                    gr.update(interactive=False),
                    "**Status:** Select a save file to load"
                )
            
            # Validate file
            file_path = file_info.name
            ui_logger.debug("File uploaded", path=file_path)
            
            # Basic validation
            if not file_path.endswith('.json'):
                return (
                    gr.update(interactive=False),
                    "**❌ Error:** Please select a .json save file"
                )
            
            # ✅ NOUVEAU: Utilise la nouvelle méthode pour charger depuis le contenu
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            success, save_data, msg = GameFacade.load_save_from_content(file_content)
            
            if success:
                # Get save info for display
                from frontend.core.frontend_config import config
                ai_config = config.get_openai_config()
                temp_facade = GameFacade(ai_config)  # Temporary for getting save info
                save_info = temp_facade.get_save_info(save_data)
                
                if "error" not in save_info:
                    player_name = save_info.get("player_name", "Unknown")
                    timestamp = save_info.get("timestamp", "Unknown")
                    location = save_info.get("current_location", "Unknown")
                    
                    return (
                        gr.update(interactive=True),
                        f"**✅ Valid save file:**\n" +
                        f"Player: {player_name}\n" +
                        f"Location: {location}\n" +
                        f"Date: {timestamp[:10]}"  # Just the date part
                    )
                else:
                    return (
                        gr.update(interactive=False),
                        f"**❌ Error:** {save_info['error']}"
                    )
            else:
                return (
                    gr.update(interactive=False),
                    f"**❌ Error:** {msg}"
                )
                
        except Exception as e:
            ui_logger.error("File upload error", error=str(e))
            return (
                gr.update(interactive=False),
                f"**❌ Error:** Failed to read file - {str(e)}"
            )
    
    @staticmethod
    def handle_load_game(file_info, ai_config) -> Tuple[Optional[GameFacade], list, str]:
        """
        Handle load game request using new load_save_from_content method
        
        Args:
            file_info: Gradio file upload info
            ai_config: AI configuration for new game
            
        Returns:
            Tuple[new_game_facade, new_chat_history, status_message]
        """
        try:
            if not file_info:
                return None, [], "**❌ Error:** No file selected"
            
            ui_logger.user_action("load_game_requested", filename=file_info.name)
            
            # ✅ NOUVEAU: Charge depuis le contenu plutôt que le fichier
            with open(file_info.name, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            success, save_data, msg = GameFacade.load_save_from_content(file_content)
            
            if not success:
                return None, [], f"**❌ Error:** {msg}"
            
            # Create new game from save
            new_facade, chat_history, restore_msg = GameFacade.create_game_from_save(
                save_data, ai_config
            )
            
            if new_facade:
                ui_logger.info("Game loaded successfully", 
                              player=new_facade.state.player_name,
                              location=new_facade.state.current_location)
                
                return (
                    new_facade, 
                    chat_history, 
                    f"**✅ Success:** {restore_msg}"
                )
            else:
                return None, [], f"**❌ Error:** {restore_msg}"
                
        except Exception as e:
            error_msg = f"Load failed: {str(e)}"
            ui_logger.error("Load game error", error=error_msg)
            return None, [], f"**❌ Error:** {error_msg}"
    
    # ===== HELPER METHODS =====
    
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


def create_enhanced_settings_modal_factory() -> EnhancedSettingsModalHandler:
    """Factory function to create enhanced settings modal handler"""
    return EnhancedSettingsModalHandler()