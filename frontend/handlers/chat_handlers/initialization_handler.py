from typing import Dict, List
import gradio as gr
from ...core.constants import ButtonStates, GameText
from ...core.frontend_config import image_assets
from ...core.types import OptionalFacade, UIUpdateResult
from ...services.map_service import update_map
from ..ui_handlers.facade_handler import create_game_facade
from .base_handler import BaseChatHandler


class InitializationHandler(BaseChatHandler):
    """Handles player name input and game initialization"""
    
    def can_handle(
        self, chat: str, history: List[Dict[str, str]], facade: OptionalFacade
    ) -> bool:
        return len(history) == 1 and facade is None
    
    def handle(
        self, chat: str, history: List[Dict[str, str]], facade: OptionalFacade
    ) -> UIUpdateResult:
        # Create new game facade
        game_facade = create_game_facade()
        
        # Initialize game
        intro_text = game_facade.start_game(chat)
        updated_map = update_map(game_facade.get_current_location())
        
        return UIUpdateResult(
            message=intro_text,
            room_view=gr.update(
                visible=True,
                value=image_assets.room_image,
                label=GameText.FIRST_ROOM_VIEW_LABEL,
            ),
            room_map=gr.update(
                visible=True, value=updated_map, label=GameText.MANOR_MAP_LABEL
            ),
            inventory_display=gr.update(visible=False),
            game_controller=game_facade,
            inventory_button=gr.update(interactive=ButtonStates.ENABLED),
            conclude_button=gr.update(interactive=ButtonStates.ENABLED),
            settings_button=gr.update(interactive=ButtonStates.ENABLED),
        )