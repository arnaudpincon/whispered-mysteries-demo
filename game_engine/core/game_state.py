"""GameState """

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
import uuid

from game_engine.models.reputation import GlobalReputation
from game_engine.models.player import Player
from game_engine.models.room import Room

class GameMode(Enum):
    EXPLORATION = "exploration"
    CONVERSATION = "conversation"
    FINAL_CONFRONTATION = "final_confrontation"
    GAME_OVER = "game_over"

@dataclass
class GameState:
    """Pure game state - data only"""
    
    # Basic data
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    current_mode: GameMode = GameMode.EXPLORATION
    current_location: str = "Main Hall"
    player_name: str = ""
    game_running: bool = False
    
    # Game objects
    rooms: Dict[str, Room] = field(default_factory=dict)
    player: Optional[Player] = None
    
    # Progression
    attempts_remaining: int = 3
    attempts_used: int = 0
    ending_type: int = 0
    investigation_stage: int = 0
    reputation: GlobalReputation = field(default_factory=GlobalReputation)
    
    # Collections
    rooms_visited: Set[str] = field(default_factory=set)
    characters_met: Set[str] = field(default_factory=set)
    
    # Conversation
    character_in_conversation: str = ""
    conclude_conversation: List[Dict[str, str]] = field(default_factory=list)
    
    # Metadata
    lore: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {"characters": {}, "rooms": {}})
    dev_mode: bool = False

    def __post_init__(self):
        """Initialize session-specific cache after object creation"""
        from ai_engine.cache.session_cache_manager import get_cache_for_session
        self._session_cache = get_cache_for_session(self.session_id)
        print(f"GameState created with session ID: {self.session_id}")

    def get_session_cache(self):
        """Get the cache instance for this session"""
        if not hasattr(self, '_session_cache'):
            from ai_engine.cache.session_cache_manager import get_cache_for_session
            self._session_cache = get_cache_for_session(self.session_id)
        return self._session_cache

    def cleanup_session(self):
        """Clean up session resources when game ends"""
        from ai_engine.cache.session_cache_manager import get_session_cache_manager
        manager = get_session_cache_manager()
        manager.remove_session(self.session_id)
        print(f"Session {self.session_id} cleaned up")

    def get_current_room(self) -> Optional[Room]:
        """Get current room object"""
        return self.rooms.get(self.current_location)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for UI consumption"""
        return {
            "mode": self.current_mode.value,
            "location": self.current_location,
            "player_name": self.player_name,
            "game_running": self.game_running,
            "attempts_remaining": self.attempts_remaining,
            "attempts_used": self.attempts_used,
            "ending_type": self.ending_type,
            "character_in_conversation": self.character_in_conversation,
            "rooms_visited": list(self.rooms_visited),
            "characters_met": list(self.characters_met),
            "investigation_stage": self.investigation_stage,
            "lore": self.lore,
            "reputation": {
                "total_counts": {
                    "impromptu": self.reputation.get_total_count(GlobalReputation.ReputationSeverity.IMPROMPTU),
                    "awkward": self.reputation.get_total_count(GlobalReputation.ReputationSeverity.AWKWARD),
                    "dangerous": self.reputation.get_total_count(GlobalReputation.ReputationSeverity.DANGEROUS)
                },
                "global_status": {
                    "impromptu": self.reputation.is_global_reputation(GlobalReputation.ReputationSeverity.IMPROMPTU),
                    "awkward": self.reputation.is_global_reputation(GlobalReputation.ReputationSeverity.AWKWARD),
                    "dangerous": self.reputation.is_global_reputation(GlobalReputation.ReputationSeverity.DANGEROUS)
                }
            }
        }

    def to_ai_format(self) -> Dict[str, Any]:
        """Convert to AI-compatible format"""
        from game_engine.utils.state_helper import StateHelper
        
        # Prepare player data safely
        player_data = {}
        if self.player:
            player_data = {
                "name": self.player.name,
                "location": self.current_location,
                "inventory": (
                    [
                        {"name": item.name, "description": item.description}
                        for item in self.player.inventory
                    ]
                    if hasattr(self.player, "inventory") and self.player.inventory
                    else []
                ),
            }
        else:
            player_data = {
                "name": self.player_name or "Detective",
                "location": self.current_location,
                "inventory": [],
            }

        # Use unified room access
        current_room_data = {}
        current_room = self.get_current_room()
        if current_room:
            current_room_data = {
                "name": current_room.name,
                "description": current_room.description,
                "characters": (
                [
                    {
                        "name": char.name,
                        "status": char.status,
                    }
                    for char in current_room.characters
                ]
            if hasattr(current_room, "characters")
            else []
                ),
                "clues": (
                    [clue.name for clue in current_room.clues]
                    if hasattr(current_room, "clues")
                    else []
                ),
                "exits": current_room.exits if hasattr(current_room, "exits") else [],
            }
        else:
            current_room_data = {
                "name": self.current_location,
                "description": "No description available",
                "characters": [],
                "clues": [],
                "exits": [],
            }

        # Use helper for reputation context
        reputation_context = StateHelper.get_reputation_context_for_ai(self)

        return {
            "player": player_data,
            "current_room": current_room_data,
            "rooms_visited": list(self.rooms_visited),
            "characters_met": list(self.characters_met),
            "mode": self.current_mode.value,
            "investigation_stage": self.investigation_stage,
            "character_in_conversation": self.character_in_conversation,
            "lore": self.lore,
            "conclude_conversation": self.conclude_conversation,
            "attempts": self.attempts_used,
            "ending": self.ending_type,
            "dev_mode": self.dev_mode,
            "reputation": reputation_context
        }