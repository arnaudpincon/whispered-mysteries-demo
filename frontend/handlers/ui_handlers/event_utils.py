#!/usr/bin/env python3
"""Event utility functions - extracted from main_frontend.py"""

from typing import Any, Dict, Tuple

import gradio as gr

from game_engine.interfaces.game_facade import GameFacade
from game_engine.core.game_state import GameMode

from ...core.constants import ButtonStates, GameModes, GameText, UIConstants
from ...core.logging_config import PerformanceTimer, ui_logger
from ...core.types import OptionalFacade
from ...services.image_preloader import (
    get_ending_image,
    get_room_image,
    get_special_image,
)
from ...services.map_service import update_map
from ...ui.response_handler import ResponseHandler
from ..transition_handlers import ButtonHandler, ModalHandler, ModeTransitionHandler


def disable_buttons_on_submit() -> Tuple[Any, Any, Any]:
    """Disable buttons when user submits a message"""
    ui_logger.ui_update("buttons", "disable_on_submit")
    return (
        gr.update(interactive=ButtonStates.DISABLED),  # conclude_button
        gr.update(interactive=ButtonStates.DISABLED),  # inventory_button
        gr.update(interactive=ButtonStates.DISABLED),  # settings_button
    )


def enable_all_buttons() -> Tuple[Any, Any, Any]:
    """Enable all buttons after processing"""
    ui_logger.ui_update("buttons", "enable_all")
    return (
        gr.update(interactive=ButtonStates.ENABLED),  # conclude_button
        gr.update(interactive=ButtonStates.ENABLED),  # inventory_button
        gr.update(interactive=ButtonStates.ENABLED),  # settings_button
    )


def execute_game_transition_via_button(controller: OptionalFacade, chat_history) -> Tuple[Any, ...]:
    """Execute transition with handlers"""

    with PerformanceTimer("execute_game_transition_via_button", ui_logger):
        if controller is None:
            ui_logger.error("No game controller provided for transition")
            return tuple(gr.update() for _ in range(UIConstants.MODAL_OUTPUTS))

        # Use ModeTransitionHandler to determine type transition
        mode_handler = ModeTransitionHandler()

        if not mode_handler.can_handle(controller):
            ui_logger.error("Cannot handle transition - invalid controller")
            return tuple(gr.update() for _ in range(UIConstants.MODAL_OUTPUTS))

        current_mode = controller.get_current_mode()
        attempts = controller.get_attempts_remaining()

        ui_logger.transition(
            "determine_transition_type",
            current_mode=current_mode.value,
            attempts_remaining=attempts,
        )

        # Transitions via handlers
        if current_mode == GameMode.CONVERSATION:
            # If we are in a conversation, the action is to exit the conversation to transit to exploration mode
            ui_logger.info("Exiting conversation mode")
            response = mode_handler.exit_conversation(controller)
            chat_history.append({"role": "user", "content": GameText.GOODBYE_MESSAGE})
            chat_history.append({
                "role": "assistant", 
                "content": response["message"]
            })
            return convert_chat_response_to_modal_format(response, controller, chat_history)

        elif current_mode == GameMode.FINAL_CONFRONTATION:
            if attempts <= 0:
                # If no attemps left, trigger game over
                ui_logger.warning("Abandoning investigation - no attempts left")
                mode_handler.abandon_investigation(controller, chat_history)
                return update_ui_for_game_over_via_handlers(controller, chat_history)
            else:
                # Return to exploration mode
                ui_logger.info("Returning to exploration from confrontation")
                mode_handler.return_to_exploration(controller)
                return update_ui_for_exploration_via_handlers(controller, chat_history)

        else:  # EXPLORATION
            # Open modal to confirm the transition to final confrontation mode
            ui_logger.info("Showing solve case modal", attempts_remaining=attempts)
            modal_updates = ModalHandler.show_solve_case_modal(attempts)

            return (
                gr.update(),  # room_view - no change
                gr.update(),  # room_map - no change
                gr.update(),  # inventory_display - no change
                controller,  # game_facade
                gr.update(interactive=ButtonStates.ENABLED),  # inventory_button
                ButtonHandler.update_main_action_button(current_mode.value, attempts),
                modal_updates[0],  # modal visibility
                modal_updates[1],  # modal content
                gr.update(interactive=ButtonStates.ENABLED),  # settings_button
                chat_history,
            )


def convert_chat_response_to_modal_format(
    response: Dict[str, Any], controller: GameFacade, chat_history
) -> Tuple[Any, ...]:
    """Convert chat response to modal format"""
    new_mode = response.get("mode", controller.get_current_mode().value)
    attempts = controller.get_attempts_remaining()
    updated_img = update_map(controller.get_current_location())
    updated_inventory = controller.get_inventory()

    new_character_img, new_room_img = ResponseHandler.update_images_if_needed(
        response, controller
    )

    if controller.get_show_inventory():
        ui_logger.ui_update("view", "show_inventory_after_chat")
        return (
            gr.update(visible=True, value=new_room_img, label=GameText.ROOM_VIEW_LABEL),
            gr.update(visible=False),
            gr.update(visible=True, value=updated_inventory),
            controller,
            gr.update(interactive=ButtonStates.ENABLED),
            ButtonHandler.update_main_action_button(new_mode, attempts),
            gr.update(visible=False),
            gr.update(),
            gr.update(interactive=ButtonStates.ENABLED),
            chat_history
        )
    else:
        ui_logger.ui_update("view", "show_map_after_chat")
        return (
            gr.update(visible=True, value=new_room_img, label=GameText.ROOM_VIEW_LABEL),
            gr.update(visible=True, value=updated_img, label=GameText.MANOR_MAP_LABEL),
            gr.update(visible=False),
            controller,
            gr.update(interactive=ButtonStates.ENABLED),
            ButtonHandler.update_main_action_button(new_mode, attempts),
            gr.update(visible=False),
            gr.update(),
            gr.update(interactive=ButtonStates.ENABLED),
            chat_history
        )


def update_ui_for_exploration_via_handlers(controller: GameFacade, chat_history) -> Tuple[Any, ...]:
    """Update UI for exploration via handlers"""
    ui_logger.state_change("confrontation", "exploration", reason="user_requested")

    # Get real room image
    new_room_img = get_special_image("room")
    if controller.state.player and controller.state.player.current_location:
        current_room = controller.state.player.current_location
        room_image_url = getattr(current_room, "image_url", "")
        if room_image_url:
            new_room_img = get_room_image(room_image_url)
            ui_logger.image_operation("loaded", "room", url=room_image_url)
        else:
            ui_logger.image_operation("fallback", "room")

    updated_img = update_map(controller.get_current_location())
    updated_inventory = controller.get_inventory()
    attempts = controller.get_attempts_remaining()

    chat_history.append({"role": "user", "content": "---------"})
    chat_history.append({
        "role": "assistant", 
        "content": "You decide to call off the gathering and return to your investigation. The guests disperse, resuming their usual activities."
    })

    if controller.get_show_inventory():
        return (
            gr.update(visible=True, value=new_room_img, label=GameText.ROOM_VIEW_LABEL),
            gr.update(visible=False),
            gr.update(visible=True, value=updated_inventory),
            controller,
            gr.update(interactive=ButtonStates.ENABLED),
            ButtonHandler.update_main_action_button(GameModes.EXPLORATION, attempts),
            gr.update(visible=False),
            gr.update(),
            gr.update(interactive=ButtonStates.ENABLED),
            chat_history
        )
    else:
        return (
            gr.update(visible=True, value=new_room_img, label=GameText.ROOM_VIEW_LABEL),
            gr.update(visible=True, value=updated_img, label=GameText.MANOR_MAP_LABEL),
            gr.update(visible=False),
            controller,
            gr.update(interactive=ButtonStates.ENABLED),
            ButtonHandler.update_main_action_button(GameModes.EXPLORATION, attempts),
            gr.update(visible=False),
            gr.update(),
            gr.update(interactive=ButtonStates.ENABLED),
            chat_history
        )


def update_ui_for_game_over_via_handlers(controller: GameFacade, chat_history) -> Tuple[Any, ...]:
    """Update UI for game over via handlers"""
    ui_logger.game_event(
        "game_over_ui_update",
        ending_type=controller.state.ending_type,
        attempts_used=controller.state.attempts_used,
    )

    ending_type = controller.state.ending_type
    ending_image = get_ending_image(ending_type)

    attempts = controller.get_attempts_remaining()
    current_mode = controller.get_current_mode().value

    ui_logger.image_operation("loaded", "ending", ending_type=ending_type)

    return (
        gr.update(visible=True, value=ending_image, label=GameText.GAME_OVER_LABEL),
        gr.update(visible=False),  # room_map
        gr.update(visible=False),  # inventory_display
        controller,  # game_facade
        gr.update(interactive=ButtonStates.DISABLED),  # inventory_button
        ButtonHandler.update_main_action_button(current_mode, attempts),  # conclude_button
        gr.update(visible=False),  # modal_visibility
        gr.update(),  # modal_content
        gr.update(interactive=ButtonStates.DISABLED),  # settings_button
        chat_history  # chat_history
    )