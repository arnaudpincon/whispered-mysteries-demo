"""
Room description generation component
"""

import logging
from typing import Any

from ai_engine.api.service import APIConfig
from ai_engine.prompts import create_room_description_prompt
from game_engine.core.game_state import GameState
from game_engine.models.room import Room

from .interfaces import IRoomDescriptionGenerator

logger = logging.getLogger(__name__)


class RoomDescriptionGenerator(IRoomDescriptionGenerator):
    """Generates atmospheric descriptions of rooms"""
    
    def __init__(self, api_service, cache, dev_mode: bool = False):
        self.api_service = api_service
        self.cache = cache
        self.dev_mode = dev_mode
    
    def generate_description(self, room: Room, game_state: Any, action: str) -> str:
        """
        Generates an atmospheric description of a room.

        Args:
            room: Room to describe (contains its own nonsense history)
            game_state: Current game state
            action: Action being performed

        Returns:
            Atmospheric description of the room
        """
        try:
            # Check if player inspect, enter or re-enter
            player_state = self._check_action_player(game_state, action, room)

            # Debug info for dev mode
            if hasattr(game_state, 'dev_mode') and game_state.dev_mode:
                nonsense_count = len(getattr(room, 'nonsense_events', []))
                if nonsense_count > 0:
                    print(f"🏠 ROOM DESCRIPTION: Including {nonsense_count} nonsense events for {room.name}")

            # Prompt to describe room (room contains its own nonsense history)
            prompt: str = create_room_description_prompt(room, player_state)

            # Check cache first - include nonsense in cache key
            nonsense_count = len(getattr(room, 'nonsense_events', []))
            cache_context = {
                "type": "room", 
                "name": room.name, 
                "nonsense_events": nonsense_count,
                "player_state": player_state
            }
            
            cached_result = self.cache.get(
                prompt, 
                {"temperature": 0.5}, 
                cache_context
            )
            
            if cached_result:
                if hasattr(game_state, 'dev_mode') and game_state.dev_mode:
                    print(f"🚀 CACHE HIT: Room description found in cache for {room.name}")
                return cached_result
            
            # No cache, make API call
            messages = [{"role": "user", "content": prompt}]
            system_content = "You are a game master running a tabletop detective role-playing game set in 19th century Blackwood Manor where a murder has been committed."

            content = self.api_service.make_api_call(
                messages=messages,
                system_content=system_content,
                max_tokens=APIConfig.MAX_TOKENS_MEDIUM,
            )

            # Always define result with a fallback
            if content:
                result = content
            else:
                result = f"You find yourself in {room.name}."
            
            # Store in cache
            self.cache.put(
                prompt, 
                {"temperature": 0.5}, 
                result, 
                cache_context
            )
            
            if hasattr(game_state, 'dev_mode') and game_state.dev_mode:
                print(f"💾 CACHE MISS: Generated and cached room description for {room.name}")
            
            return result

        except Exception as e:
            logger.error(f"Error in generate_room_description: {e}")
            # Safe fallback that always works
            room_name = getattr(room, 'name', 'an unknown location')
            return f"You find yourself in {room_name}."

    def _check_action_player(self, game_state: GameState, action: str, room: Room) -> str:
        """
        Determine player state based on game state and action.
        
        Args:
            game_state: Current game state
            action: Action being performed ("move", "look", etc.)
            room: Room object being interacted with
            
        Returns:
            str: Player state ("first_entry", "re_entry", or "inspection")
        """
        try:
            # Safe attribute access with fallbacks
            rooms_visited = getattr(game_state, 'rooms_visited', set())
            room_name = getattr(room, 'name', 'Unknown Room')
            
            # Determine if it's the first time in this room
            first_time = room_name not in rooms_visited
            
            # Determine player state based on action
            if action == "move":
                if first_time:
                    player_state = "first_entry"
                else:
                    player_state = "re_entry"
            else:
                player_state = "inspection"
            
            return player_state
            
        except Exception as e:
            logger.error(f"Error in _check_action_player: {e}")
            # Safe fallback
            return "inspection"