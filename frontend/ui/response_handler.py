#!/usr/bin/env python3
"""
Response handler for UI updates

Provides a unified interface for handling game responses and converting them
to appropriate UI updates. Manages image updates, state transitions, and
UI component visibility based on game mode and player state.
"""

from typing import Any, Dict, Optional

import gradio as gr
from PIL import Image

from frontend.services.image_preloader import (
    get_character_image,
    get_ending_image,
    get_room_image,
    get_special_image,
)
from game_engine.interfaces.game_facade import GameFacade

# Import constants and types
from ..core.constants import ButtonStates, GameModes, GameText
from ..core.types import UIUpdateResult
from ..handlers.transition_handlers import ButtonHandler
from ..services.map_service import update_map


class ResponseHandler:
    """
    Unified response handler for all UI updates

    Provides a clean interface for converting game responses into UI updates,
    handling image management, state transitions, and component visibility.
    """

    @staticmethod
    def build_ui_response(
        response: Dict[str, Any], facade: GameFacade, image_type: str = "auto"
    ) -> UIUpdateResult:
        """
        Unified method for building UI responses from game data

        Args:
            response: Response from the game engine
            facade: GameFacade instance
            image_type: Type of image to display ("room", "character", "confrontation",
                       "ending", or "auto" for automatic detection)

        Returns:
            Complete UIUpdateResult for all UI components
        """
        # Extract base data
        mode = response.get("mode", GameModes.EXPLORATION)
        attempts = facade.get_attempts_remaining()
        show_inventory = facade.get_show_inventory()

        # Determine display image and label
        room_image, room_label = ResponseHandler._get_display_image_and_label(
            response, facade, image_type, mode
        )

        # Get map and inventory data
        map_image = ResponseHandler._get_map_image(facade)
        inventory_text = facade.get_inventory()

        # Determine button states
        main_button = ButtonHandler.update_main_action_button(mode, attempts)
        inventory_button_enabled = mode != GameModes.GAME_OVER

        # Build unified response based on inventory visibility
        if show_inventory:
            return UIUpdateResult(
                message=response["message"],
                room_view=gr.update(visible=True, value=room_image, label=room_label),
                room_map=gr.update(visible=False),
                inventory_display=gr.update(
                    visible=True, value=inventory_text, label=GameText.INVENTORY_LABEL
                ),
                game_controller=facade,
                inventory_button=gr.update(interactive=inventory_button_enabled),
                conclude_button=main_button,
                settings_button=gr.update(interactive=ButtonStates.ENABLED),
            )
        else:
            return UIUpdateResult(
                message=response["message"],
                room_view=gr.update(visible=True, value=room_image, label=room_label),
                room_map=gr.update(
                    visible=True, value=map_image, label=GameText.MANOR_MAP_LABEL
                ),
                inventory_display=gr.update(visible=False),
                game_controller=facade,
                inventory_button=gr.update(interactive=inventory_button_enabled),
                conclude_button=main_button,
                settings_button=gr.update(interactive=ButtonStates.ENABLED),
            )

    @staticmethod
    def handle_conversation_mode_simplified(
        response: Dict[str, Any],
        new_character_img: Image.Image,
        show_inventory: bool,
        updated_img: Image.Image,
        updated_inventory: str,
        game_controller: GameFacade,
        new_mode: str,
        new_location: str,
        new_room_img: Image.Image,
        attempts: int,
    ) -> UIUpdateResult:
        """Legacy compatibility for conversation mode"""
        return ResponseHandler.build_ui_response(response, game_controller, "character")

    @staticmethod
    def handle_exploration_mode_simplified(
        response: Dict[str, Any],
        new_room_img: Image.Image,
        show_inventory: bool,
        updated_img: Image.Image,
        updated_inventory: str,
        game_controller: GameFacade,
        new_mode: str,
        new_location: str,
        new_character_img: Image.Image,
        attempts: int,
    ) -> UIUpdateResult:
        """Legacy compatibility for exploration mode"""
        return ResponseHandler.build_ui_response(response, game_controller, "room")

    @staticmethod
    def handle_final_confrontation_simplified(
        response: Dict[str, Any],
        game_controller: GameFacade,
        new_mode: str,
        new_location: str,
        new_character_img: Image.Image,
        new_room_img: Image.Image,
        attempts: int,
    ) -> UIUpdateResult:
        """Legacy compatibility for final confrontation mode"""
        return ResponseHandler.build_ui_response(
            response, game_controller, "confrontation"
        )

    @staticmethod
    def handle_game_over_simplified(
        response: Dict[str, Any],
        game_controller: GameFacade,
        new_mode: str,
        new_location: str,
        new_character_img: Image.Image,
        new_room_img: Image.Image,
        attempts: int,
    ) -> UIUpdateResult:
        """Legacy compatibility for game over mode"""
        return ResponseHandler.build_ui_response(response, game_controller, "ending")

    # Helper methods

    @staticmethod
    def _get_display_image_and_label(
        response: Dict[str, Any], facade: GameFacade, image_type: str, mode: str
    ) -> tuple[Image.Image, str]:
        """
        Determine the appropriate image and label to display

        Args:
            response: Game response data
            facade: GameFacade instance
            image_type: Requested image type or "auto"
            mode: Current game mode

        Returns:
            Tuple of (image, label) for display
        """
        # Auto-detect image type based on mode if not specified
        if image_type == "auto":
            if mode == GameModes.CONVERSATION:
                image_type = "character"
            elif mode == GameModes.FINAL_CONFRONTATION:
                image_type = "confrontation"
            elif mode == GameModes.GAME_OVER:
                image_type = "ending"
            else:
                image_type = "room"

        # Get appropriate image and label
        if image_type == "character":
            character_name = response.get("character_in_conversation", "")
            character_image_url = response.get("character_image_url", "")

            image = (
                get_character_image(character_image_url)
                if character_image_url
                else get_special_image("character")
            )
            label = character_name if character_name else GameText.CHARACTER_LABEL
            return image, label

        elif image_type == "confrontation":
            image = get_special_image("confrontation")
            label = GameText.CONFRONTATION_LABEL
            return image, label

        elif image_type == "ending":
            ending_type = response.get("ending", 0)
            image = get_ending_image(ending_type)
            label = GameText.ENDING_LABEL
            return image, label

        else:  # "room" or default
            room_name = response.get("location", "")
            room_image_url = response.get("room_image_url", "")
            image = (
                get_room_image(room_image_url)
                if room_image_url
                else get_special_image("room")
            )
            label = room_name if room_name else GameText.ROOM_VIEW_LABEL
            return image, label

    @staticmethod
    def _get_map_image(facade: GameFacade) -> Image.Image:
        """Get updated map image for current location"""
        return update_map(facade.get_current_location())

    @staticmethod
    def update_images_if_needed(
        response: Dict[str, Any], facade: GameFacade
    ) -> tuple[Image.Image, Image.Image]:
        """
        Update character and room images based on response

        Args:
            response: Game response containing image URLs
            facade: GameFacade instance (unused but kept for compatibility)

        Returns:
            Tuple of (character_image, room_image)
        """
        # Get character image
        character_image_url = response.get("character_image_url", "")
        character_image = (
            get_character_image(character_image_url)
            if character_image_url
            else get_special_image("character")
        )

        # Get room image
        room_image_url = response.get("room_image_url", "")
        room_image = (
            get_room_image(room_image_url)
            if room_image_url
            else get_special_image("room")
        )

        return character_image, room_image

    @staticmethod
    def create_error_response(
        error_message: str, facade: Optional[GameFacade] = None
    ) -> UIUpdateResult:
        """
        Create a safe error response for UI display

        Args:
            error_message: Error message to display
            facade: Optional GameFacade instance

        Returns:
            UIUpdateResult with error state
        """
        error_response = {"message": error_message, "mode": GameModes.EXPLORATION}

        if facade:
            return ResponseHandler.build_ui_response(error_response, facade)
        else:
            # Fallback when no facade is available
            return UIUpdateResult(
                message=error_message,
                room_view=gr.update(),
                room_map=gr.update(),
                inventory_display=gr.update(),
                game_controller=None,
                inventory_button=gr.update(interactive=ButtonStates.DISABLED),
                conclude_button=gr.update(interactive=ButtonStates.DISABLED),
                settings_button=gr.update(interactive=ButtonStates.ENABLED),
            )
