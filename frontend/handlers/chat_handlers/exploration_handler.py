from typing import Dict, List

from game_engine.core.game_state import GameMode

from ...core.types import OptionalFacade, UIUpdateResult
from .base_handler import BaseChatHandler


class ExplorationHandler(BaseChatHandler):
    """Handles exploration mode interactions"""

    def can_handle(
        self, chat: str, history: List[Dict[str, str]], facade: OptionalFacade
    ) -> bool:
        return facade is not None and facade.get_current_mode() == GameMode.EXPLORATION

    def handle(
        self, chat: str, history: List[Dict[str, str]], facade: OptionalFacade
    ) -> UIUpdateResult:
        """Handle exploration mode with automatic mode transition detection"""
        return self._process_command_with_mode_transition(
            chat, facade, GameMode.EXPLORATION.value
        )
