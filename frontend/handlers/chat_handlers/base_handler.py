from abc import ABC, abstractmethod
from typing import Dict, List

from frontend.core.constants import GameModes

from ...core.types import OptionalFacade, UIUpdateResult
from ...services.map_service import update_map
from ...ui.response_handler import ResponseHandler


class BaseChatHandler(ABC):
    """Base handler for chat interactions with common processing logic"""

    @abstractmethod
    def can_handle(
        self, chat: str, history: List[Dict[str, str]], facade: OptionalFacade
    ) -> bool:
        """Check if this handler can process the request"""

    @abstractmethod
    def handle(
        self, chat: str, history: List[Dict[str, str]], facade: OptionalFacade
    ) -> UIUpdateResult:
        """Process the chat request"""

    def _process_command_with_mode_transition(
        self, chat: str, facade: OptionalFacade, current_mode: str
    ) -> UIUpdateResult:
        """
        Common logic for processing commands with potential mode transitions

        Args:
            chat: User input
            facade: Game facade
            current_mode: Expected current mode for this handler

        Returns:
            UIUpdateResult with appropriate mode handling
        """
        # Process command
        response = facade.process_command(chat)

        # Update images and state
        new_character_img, new_room_img = ResponseHandler.update_images_if_needed(
            response, facade
        )
        updated_map = update_map(facade.get_current_location())
        updated_inventory = facade.get_inventory()
        attempts = facade.get_attempts_remaining()

        # Handle mode transitions
        response_mode = response["mode"]

        if response_mode == GameModes.CONVERSATION:
            return ResponseHandler.handle_conversation_mode_simplified(
                response,
                new_character_img,
                facade.get_show_inventory(),
                updated_map,
                updated_inventory,
                facade,
                response_mode,
                response["location"],
                new_room_img,
                attempts,
            )
        elif response_mode == GameModes.EXPLORATION:
            return ResponseHandler.handle_exploration_mode_simplified(
                response,
                new_room_img,
                facade.get_show_inventory(),
                updated_map,
                updated_inventory,
                facade,
                response_mode,
                response["location"],
                new_character_img,
                attempts,
            )
        else:
            # Handle other modes (final_confrontation, game_over, etc.)
            return ResponseHandler.build_ui_response(response, facade)
