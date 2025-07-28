# game_engine/utils/state_helper.py
"""Helper utilities for GameState operations - extracted from GameState"""
from typing import Any, Dict, List
from game_engine.core.game_state import GameState
from game_engine.models.reputation import ReputationSeverity


class StateHelper:
    """Helper for complex GameState operations"""

    @staticmethod
    def get_reputation_context_for_ai(state: GameState) -> Dict[str, Any]:
        """Generate reputation context using new system"""
        current_location = state.current_location
        room_rep = state.reputation.get_room(current_location)
       
        # Status in current room
        current_room_status = {
            "impromptu_count": room_rep.get_count_by_severity(ReputationSeverity.IMPROMPTU),
            "awkward_count": room_rep.get_count_by_severity(ReputationSeverity.AWKWARD),
            "dangerous_count": room_rep.get_count_by_severity(ReputationSeverity.DANGEROUS),
            "is_impromptu_local": room_rep.is_local_reputation(ReputationSeverity.IMPROMPTU),
            "is_awkward_local": room_rep.is_local_reputation(ReputationSeverity.AWKWARD),
            "is_dangerous_local": room_rep.is_local_reputation(ReputationSeverity.DANGEROUS)
        }
       
        # Global status
        global_status = {
            "is_impromptu_global": state.reputation.is_global_reputation(ReputationSeverity.IMPROMPTU),
            "is_awkward_global": state.reputation.is_global_reputation(ReputationSeverity.AWKWARD),
            "is_dangerous_global": state.reputation.is_global_reputation(ReputationSeverity.DANGEROUS),
        }
       
        # Recent events from new system
        recent_events = room_rep.get_recent_events(5)
        recent_actions = [
            {
                "category": event.severity.value,
                "command": event.command,
                "timestamp": event.timestamp,
                "summary": event.summary
            }
            for event in recent_events
        ]
       
        return {
            "current_room": current_room_status,
            "global": global_status,
            "recent_actions": recent_actions,
            "warnings": StateHelper.generate_warnings(state)
        }

    @staticmethod
    def generate_warnings(state: GameState) -> List[str]:
        """Generate warnings using new system"""
        warnings = []
       
        if state.reputation.is_global_reputation(ReputationSeverity.DANGEROUS):
            warnings.append("CRITICAL: Detective is globally dangerous - next dangerous action = EXPULSION")
       
        room_rep = state.reputation.get_room(state.current_location)
        dangerous_count = room_rep.get_count_by_severity(ReputationSeverity.DANGEROUS)
       
        if dangerous_count == 1:
            warnings.append("WARNING: One more dangerous action in this room = global dangerous reputation")
       
        if state.reputation.is_global_reputation(ReputationSeverity.AWKWARD):
            warnings.append("INFO: Detective has eccentric reputation throughout the manor")
       
        return warnings