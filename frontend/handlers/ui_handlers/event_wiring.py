#!/usr/bin/env python3
"""Event wiring - Connect all UI components to their event handlers WITH DOWNLOAD"""

import gradio as gr
from typing import TYPE_CHECKING

from frontend.handlers.ui_handlers.settings_modal_handler import SettingsModalHandler

if TYPE_CHECKING:
    from game_engine.interfaces.game_facade import GameFacade
from ...core.constants import ButtonStates
from ..transition_handlers import ConfrontationHandler, ModalHandler

from .event_utils import (
    disable_buttons_on_submit,
    enable_all_buttons,
    execute_game_transition_via_button,
)
from .inventory_handler import InventoryHandler


def wire_all_events(
    narrative,
    inventory_button,
    conclude_button,
    settings_button,
    settings_modal,
    settings_modal_handler,
    # Tab navigation components
    save_load_tab_btn,
    settings_tab_btn, 
    close_tab_btn,
    save_load_content,
    settings_content,
    # Settings components
    language_dropdown,
    teleportation_checkbox,
    apply_button,
    status_display,
    # Confirmation modal components
    confirm_solve_btn,
    cancel_solve_btn,
    confirmation_modal,
    attempts_display,
    # Main UI components
    room_view,
    room_map,
    inventory_display,
    game_facade,
    # Save/Load components
    load_file,
    save_button,
    load_button,
    save_load_status,
    # ✅ NOUVEAU: Composant pour le téléchargement
    download_file=None,  # Will be created if not provided
    user_language="english",
    user_teleportation=False,
):
    """
    Wire all event handlers for the detective game UI with tab navigation and download

    Args:
        All the UI components that need event handlers
        download_file: Optional download file component
    """

    # Disable buttons when user submits message
    narrative.textbox.submit(
        fn=disable_buttons_on_submit,
        outputs=[conclude_button, inventory_button, settings_button],
    )

    # Inventory toggle event chain
    inventory_button.click(
        fn=disable_buttons_on_submit,
        outputs=[conclude_button, inventory_button, settings_button],
    ).then(
        fn=InventoryHandler.toggle_unified,
        inputs=[game_facade],
        outputs=[room_map, inventory_display, game_facade, inventory_button],
    ).then(
        fn=enable_all_buttons,
        outputs=[conclude_button, inventory_button, settings_button],
    )

    # Conclude button event chain
    conclude_button.click(
        fn=disable_buttons_on_submit,
        outputs=[conclude_button, inventory_button, settings_button],
    ).then(
        fn=execute_game_transition_via_button,
        inputs=[game_facade, narrative.chatbot],
        outputs=[
            room_view, room_map, inventory_display, game_facade,
            inventory_button, conclude_button, confirmation_modal, 
            attempts_display, settings_button, narrative.chatbot,
        ],
    )

    # Modal confirm button event chain
    confirm_solve_btn.click(
        fn=lambda: (
            ModalHandler.hide_solve_case_modal(),
            gr.update(interactive=ButtonStates.DISABLED),
            gr.update(interactive=ButtonStates.DISABLED),
            gr.update(interactive=ButtonStates.DISABLED),
        ),
        outputs=[confirmation_modal, conclude_button, inventory_button, settings_button],
    ).then(
        fn=ConfrontationHandler().execute,
        inputs=[game_facade, narrative.chatbot],
        outputs=[
            room_view, room_map, inventory_display, game_facade,
            inventory_button, conclude_button, inventory_button, 
            settings_button, narrative.chatbot,
        ],
    )

    # Modal cancel button
    cancel_solve_btn.click(
        fn=ModalHandler.hide_solve_case_modal, 
        outputs=[confirmation_modal]
    )

    # ===== TAB NAVIGATION EVENT HANDLERS =====
    
    # Show settings modal (default to settings tab)
    settings_button.click(
        fn=_show_settings_modal_with_default_tab,
        outputs=[settings_modal, save_load_content, settings_content, save_load_tab_btn, settings_tab_btn]
    )
    
    # Save/Load tab navigation
    save_load_tab_btn.click(
        fn=_show_save_load_tab,
        outputs=[save_load_content, settings_content, save_load_tab_btn, settings_tab_btn]
    )
    
    # Settings tab navigation  
    settings_tab_btn.click(
        fn=_show_settings_tab,
        outputs=[save_load_content, settings_content, save_load_tab_btn, settings_tab_btn]
    )
    
    # Close tab (closes entire modal)
    close_tab_btn.click(
        fn=_close_settings_modal,
        outputs=[settings_modal]
    )

    # ===== SETTINGS TAB EVENT HANDLERS =====
    
    # Apply settings changes (only available in settings tab)
    apply_button.click(
        fn=settings_modal_handler.apply_settings_changes,
        inputs=[language_dropdown, teleportation_checkbox, user_language, user_teleportation],
        outputs=[settings_modal, status_display, user_language, user_teleportation]
    )
    
    # ===== SAVE/LOAD TAB EVENT HANDLERS =====
    
    # Save game button
    if download_file is not None:
        # Si un composant download_file est fourni, l'utiliser
        save_button.click(
            fn=settings_modal_handler.handle_save_game,
            inputs=[game_facade, narrative.chatbot],
            outputs=[download_file, save_load_status]
        )
    else:
        # Fallback
        def handle_save_without_download(game_facade, chat_history):
            """Handle save without download component"""
            _, status = settings_modal_handler.handle_save_game(game_facade, chat_history)
            return status
        
        save_button.click(
            fn=handle_save_without_download,
            inputs=[game_facade, narrative.chatbot],
            outputs=[save_load_status]
        )
    
    # File upload handler - validates and enables/disables load button
    load_file.upload(
        fn=settings_modal_handler.handle_file_upload,
        inputs=[load_file],
        outputs=[load_button, save_load_status]
    )
    
    # Load game button - replaces entire game state
    load_button.click(
        fn=lambda file_info, current_facade: _handle_load_with_config(
            file_info, current_facade, settings_modal_handler
        ),
        inputs=[load_file, game_facade],
        outputs=[
            # Main game components that need updating
            game_facade,           # New game facade
            narrative.chatbot,     # New chat history 
            save_load_status,      # Status message
            room_view,             # Updated room view
            room_map,              # Updated map
            inventory_display,     # Updated inventory
            inventory_button,      # Reset button states
            conclude_button,       # Reset button states
            settings_modal         # Hide modal on successful load
        ]
    )


# ===== TAB NAVIGATION HELPER FUNCTIONS =====

def _show_settings_modal_with_default_tab():
    """Show settings modal with settings tab active by default"""
    return (
        gr.update(visible=True, elem_classes=["modal-visible"]),  # settings_modal
        gr.update(visible=False),                                 # save_load_content (hidden)
        gr.update(visible=True),                                  # settings_content (visible)
        gr.update(variant="secondary"),                           # save_load_tab_btn (inactive)
        gr.update(variant="primary"),                             # settings_tab_btn (active)
    )

def _show_save_load_tab():
    """Switch to save/load tab"""
    return (
        gr.update(visible=True),        # save_load_content (show)
        gr.update(visible=False),       # settings_content (hide)
        gr.update(variant="primary"),   # save_load_tab_btn (active)
        gr.update(variant="secondary"), # settings_tab_btn (inactive)
    )

def _show_settings_tab():
    """Switch to settings tab"""
    return (
        gr.update(visible=False),       # save_load_content (hide)
        gr.update(visible=True),        # settings_content (show)
        gr.update(variant="secondary"), # save_load_tab_btn (inactive)
        gr.update(variant="primary"),   # settings_tab_btn (active)
    )

def _close_settings_modal():
    """Close the entire settings modal"""
    return gr.update(visible=False, elem_classes=[])  # settings_modal


# ===== SAVE/LOAD HELPER FUNCTION =====

def _handle_load_with_config(file_info, current_facade, settings_modal_handler):
    """
    Internal handler for load game that manages AI config
    
    Args:
        file_info: Uploaded file info
        current_facade: Current game facade (for AI config)
        settings_modal_handler: Settings handler instance
        
    Returns:
        Tuple of all UI updates needed after load
    """
    try:
        # Get AI config from current facade or use default
        from frontend.core.frontend_config import config
        ai_config = config.get_openai_config()

        print(ai_config, "allo")
        
        # Handle load
        new_facade, chat_history, status_msg = settings_modal_handler.handle_load_game(
            file_info, ai_config
        )
        
        if new_facade:
            # Successful load - update all components
            from frontend.services.map_service import update_map
            from frontend.core.constants import ButtonStates
            
            # Get current state for UI updates
            current_location = new_facade.get_current_location()
            show_inventory = new_facade.get_show_inventory()
            
            # Update map and inventory
            updated_map = update_map(current_location)
            inventory_text = new_facade.get_inventory()
            
            # Determine room image
            current_room = new_facade.state.get_current_room()
            room_image_url = getattr(current_room, 'image_url', '') if current_room else ''
            
            if room_image_url:
                from frontend.services.image_preloader import get_room_image
                room_image = get_room_image(room_image_url)
            else:
                from frontend.services.image_preloader import get_special_image
                room_image = get_special_image('room')
            
            return (
                new_facade,                                             # New game facade
                chat_history,                                          # Restored chat history
                status_msg,                                            # Success message
                gr.update(value=room_image, label=current_location),   # Room view
                gr.update(value=updated_map, visible=not show_inventory),  # Map
                gr.update(value=inventory_text, visible=show_inventory),   # Inventory
                gr.update(interactive=ButtonStates.ENABLED),           # Inventory button
                gr.update(interactive=ButtonStates.ENABLED),           # Conclude button  
                gr.update(visible=False, elem_classes=[])              # Hide settings modal
            )
        else:
            # Failed load - keep current state, show error
            return (
                current_facade,                                        # Keep current facade
                [],                                                    # No chat changes
                status_msg,                                           # Error message
                gr.update(),                                          # No room change
                gr.update(),                                          # No map change  
                gr.update(),                                          # No inventory change
                gr.update(),                                          # No button change
                gr.update(),                                          # No button change
                gr.update(visible=True, elem_classes=["modal-visible"]) # Keep modal open
            )
            
    except Exception as e:
        error_msg = f"**Error:** Load failed - {str(e)}"
        
        return (
            current_facade,                                            # Keep current facade
            [],                                                        # No chat changes
            error_msg,                                                # Error message
            gr.update(),                                              # No changes to other components
            gr.update(),
            gr.update(), 
            gr.update(),
            gr.update(),
            gr.update(visible=True, elem_classes=["modal-visible"])   # Keep modal open
        )