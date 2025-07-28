#!/usr/bin/env python3
"""
Inventory UI operations handler

Handles inventory display and map/inventory toggling logic.
This is UI-specific logic that doesn't belong in business services.
"""

from typing import Tuple

import gradio as gr

from game_engine.interfaces.game_facade import GameFacade  # noqa
from ...core.constants import GameText
from ...core.logging_config import state_logger
from ...core.types import OptionalFacade
from ...services.map_service import update_map


class InventoryHandler:
    """
    Handles inventory UI operations and state management.

    This class manages the complex UI state changes required when switching
    between showing the inventory list and the manor map.
    """

    @staticmethod
    def toggle_unified(game_facade: OptionalFacade) -> Tuple[any, any, any, any]:
        """
        Toggle between inventory view and map view.

        This method handles all the UI state changes required when switching
        between showing the inventory list and the manor map, including:
        - Visibility toggles
        - Content updates
        - Button text changes
        - Logging state changes

        Args:
            game_facade: GameFacade instance (None if no active game)

        Returns:
            Tuple of (map_update, inventory_update, facade, button_update)
        """
        state_logger.user_action("inventory_toggle_requested")

        if game_facade is None:
            state_logger.error("No game facade for inventory toggle")
            return (gr.update(), gr.update(), game_facade, gr.update())

        # Toggle inventory state in facade
        old_state = game_facade.get_show_inventory()
        new_show_inventory = game_facade.toggle_inventory_view()

        state_logger.state_change(
            f"inventory_{'shown' if old_state else 'hidden'}",
            f"inventory_{'shown' if new_show_inventory else 'hidden'}",
        )

        if new_show_inventory:
            # Show inventory, hide map
            inventory_text = game_facade.get_inventory()
            items_count = (
                len(game_facade.state.player.inventory)
                if game_facade.state.player
                else 0
            )

            state_logger.info("Showing inventory view", items_count=items_count)

            return (
                gr.update(visible=False),  # Hide map
                gr.update(
                    visible=True, value=inventory_text, label=GameText.INVENTORY_LABEL
                ),
                game_facade,
                gr.update(value=GameText.MAP_BUTTON),
            )
        else:
            # Show map, hide inventory
            current_location = game_facade.get_current_location()
            state_logger.debug("Showing map view", location=current_location)

            updated_map = update_map(current_location)

            return (
                gr.update(
                    visible=True, value=updated_map, label=GameText.MANOR_MAP_LABEL
                ),
                gr.update(visible=False),
                game_facade,
                gr.update(value=GameText.BRIEFCASE_BUTTON),
            )

    @staticmethod
    def get_current_inventory_text(game_facade: OptionalFacade) -> str:
        """
        Get current inventory content as formatted text.

        Args:
            game_facade: Optional GameFacade instance

        Returns:
            Formatted inventory text
        """
        if game_facade is not None:
            inventory = game_facade.get_inventory()
            state_logger.debug(
                "Retrieved inventory content", content_length=len(inventory)
            )
            return inventory

        state_logger.warning("No game facade for inventory request")
        return GameText.NO_ITEMS_MESSAGE
