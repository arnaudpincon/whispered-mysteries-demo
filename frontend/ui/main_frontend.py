#!/usr/bin/env python3
"""Main frontend"""

import os
import sys
from typing import Dict, List

import gradio as gr
from PIL import Image

from frontend.handlers.ui_handlers.enhance_settings_modal_handler import create_enhanced_settings_modal_factory

from ..handlers.ui_handlers.facade_handler import cleanup_session
from frontend.ui.components.button_factory import create_control_buttons
from frontend.ui.components.chat_factory import create_chat_interface
from frontend.ui.components.display_factory import (
    create_inventory_display,
    create_room_map,
    create_room_view,
)
from frontend.handlers.ui_handlers.event_wiring import wire_all_events
from frontend.ui.components.modal_factory import create_confirmation_modal
from frontend.ui.components.settings_modal_factory import create_settings_modal

from ..handlers.chat_handlers.handler_factory import ChatHandlerFactory

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game_engine.interfaces.game_facade import GameFacade  # noqa
from frontend.core.frontend_config import image_assets, text_assets

# Import constants, types, and logging config
from ..core.constants import CSSClasses
from ..core.logging_config import PerformanceTimer, ui_logger
from ..core.types import OptionalFacade, UIUpdateResult

# Generate the initial map
from ..services.map_service import generate_initial_map
from .css_styles import CSS_STYLES

initial_map_image: Image.Image = generate_initial_map()

factory = ChatHandlerFactory()


def interpret_chat(
    chat: str, history: List[Dict[str, str]], game_facade: OptionalFacade
) -> UIUpdateResult:
    """Main chat interpretation"""
    handler = factory.get_handler(chat, history, game_facade)
    return handler.handle(chat, history, game_facade)


def create_gradio_app() -> gr.Blocks:
    """Create and return the Gradio app"""
    ui_logger.info("Creating Gradio application")
    settings_modal_handler = create_enhanced_settings_modal_factory()

    with PerformanceTimer("create_gradio_app", ui_logger):
        with gr.Blocks(
                fill_height=True,
                css=CSS_STYLES,
                title="🕵️ Whispered Mysteries",
            ) as demo:

            # State management
            game_facade: gr.State = gr.State(None)
            # Default language state
            user_language: gr.State = gr.State("english")
            user_teleportation: gr.State = gr.State(False)

            ui_logger.debug("Initialized Gradio state")

            # Main UI layout
            with gr.Row(elem_id=CSSClasses.MAIN_CONTAINER):
                with gr.Column():
                    # Room view section
                    with gr.Row():
                        room_view = create_room_view(image_assets.intro_image)
                    # Map/Inventory section
                    with gr.Row():
                        room_map = create_room_map(initial_map_image)
                        inventory_display = create_inventory_display()
                    # Control buttons section
                    with gr.Row():
                        inventory_button, conclude_button, settings_button = (
                            create_control_buttons()
                        )

                # Chat interface section
                with gr.Column(elem_id=CSSClasses.NARRATIVE_BOX):
                    with gr.Row(elem_id=CSSClasses.NARRATIVE_BOX, scale=2):
                        narrative = create_chat_interface(
                            interpret_chat_fn=interpret_chat,
                            text_assets=text_assets,
                            additional_inputs=[game_facade],
                            additional_outputs=[
                                room_view,  # 0
                                room_map,  # 1
                                inventory_display,  # 2
                                game_facade,  # 3
                                inventory_button,  # 4
                                conclude_button,  # 5
                                settings_button,  # 6
                            ],
                        )

            # Solve case modal
            (
                confirmation_modal,
                attempts_display,
                confirm_solve_btn,
                cancel_solve_btn,
            ) = create_confirmation_modal()

            # Settings modal with download support
            (
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
            ) = create_settings_modal(settings_modal_handler)

            # Event wiring
            wire_all_events(
                narrative=narrative,
                inventory_button=inventory_button,
                conclude_button=conclude_button,
                settings_button=settings_button,
                # Settings modal with navigation
                settings_modal=settings_modal,
                settings_modal_handler=settings_modal_handler,
                save_load_tab_btn=save_load_tab_btn,
                settings_tab_btn=settings_tab_btn,
                close_tab_btn=close_tab_btn,
                save_load_content=save_load_content,
                settings_content=settings_content,
                # Settings components
                language_dropdown=language_dropdown,
                teleportation_checkbox=teleportation_checkbox,
                apply_button=apply_button,
                status_display=status_display,
                # Confirmation modal
                confirm_solve_btn=confirm_solve_btn,
                cancel_solve_btn=cancel_solve_btn,
                confirmation_modal=confirmation_modal,
                attempts_display=attempts_display,
                # Main UI
                room_view=room_view,
                room_map=room_map,
                inventory_display=inventory_display,
                game_facade=game_facade,
                # Save/Load components
                load_file=load_file,
                save_button=save_button,
                load_button=load_button,
                save_load_status=save_load_status,
                # Download component
                download_file=download_file,
                # State
                user_language=user_language,
                user_teleportation=user_teleportation,
            )
            
            ui_logger.debug("Configured all event handlers with download support")

            # Clean sessions
            cleanup_btn = gr.Button("cleanup", visible=False, elem_id="cleanup-session-btn")
            cleanup_btn.click(
                fn=cleanup_session,
                inputs=[game_facade],
                outputs=[]
            )

            demo.load(
                fn=lambda: None,
                js="""
                function() {
                    window.addEventListener('beforeunload', function(e) {
                        const cleanupBtn = document.getElementById('cleanup-session-btn');
                        if (cleanupBtn) cleanupBtn.click();
                    });
                }
                """
            )

    ui_logger.info("Gradio application created successfully with download support")
    return demo


if __name__ == "__main__":
    # Initialize logging
    from ..core.logging_config import log_startup_info

    log_startup_info()

    try:
        demo = create_gradio_app()
        ui_logger.info("Starting Gradio server")
        demo.launch()
    except Exception as e:
        ui_logger.critical("Failed to start application", error=str(e))
        raise
    finally:
        from ..core.logging_config import log_shutdown_info

        log_shutdown_info()