import time
from typing import Any, Dict, List

from ai_engine.core.ai_manager import AIManager
from game_engine.core.game_state import GameState
from game_engine.services.reputation_service import ReputationService
from game_engine.models.reputation import ReputationSeverity


class MemoryService:
    """Handles character memory updates - pure memory management"""

    def __init__(self, state: GameState, ai_manager: AIManager, reputation_service: ReputationService):
        self.state = state
        self.ai_manager = ai_manager
        self.reputation_service = reputation_service

    def process_nonsense_action(self, command: str) -> Dict[str, Any]:
        """Process nonsense action with global memory propagation"""
        # 1. Generate AI response
        ai_result = self.ai_manager.nonsense_reaction(command, self.state)
        
        # 2. Process reputation with global change detection
        game_over, warnings, global_changes = self.reputation_service.process_nonsense_action(
            self.state.current_location, 
            command, 
            ai_result.get("severity", "awkward"),
            ai_result.get("summary", "")
        )
        
        # 3. Game over check
        if game_over:
            return {
                "message": "**EXPELLED FROM BLACKWOOD MANOR**\n\nYour dangerous behavior has crossed all acceptable limits...",
                "action_type": "expulsion",
                "game_over": True,
                "severity": "dangerous"
            }
        
        # 4. Update character memories locally
        self._update_character_memories_new(self.state.current_location)
        
        # 5. Propagate global reputation changes to ALL characters
        if global_changes:
            self._propagate_global_reputation_to_all_characters(global_changes)
        
        # 6. Return enhanced response
        return {
            "message": ai_result.get("message", ""),
            "action_type": "nonsense",
            "command_attempted": ai_result.get("command_attempted", ""),
            "severity": ai_result.get("severity", "awkward"),
            "warnings": warnings,
            "game_over": False,
            "global_changes": list(global_changes.keys()) if global_changes else []
        }
    
    def _propagate_global_reputation_to_all_characters(self, global_changes: Dict[str, Any]) -> None:
        """Propagate global reputation changes to ALL characters"""
        
        characters_updated = 0
        
        for severity_type, change_data in global_changes.items():
            if change_data["became_global"]:
                # Create global reputation message
                global_message = self.reputation_service.create_global_reputation_message(
                    severity_type, 
                    change_data["all_events"]
                )
                
                # Propagate to ALL characters in ALL rooms
                for room in self.state.rooms.values():
                    for character in room.characters:
                        # Check that character doesn't already have this global message
                        has_global_memory = any(
                            "MANOR-WIDE REPUTATION:" in memory.get("content", "")
                            and severity_type in memory.get("content", "")
                            for memory in character.memory_current
                            if memory.get("role") == "assistant"
                        )
                        
                        if not has_global_memory:
                            character.remember(global_message, "assistant")
                            characters_updated += 1
                
                if self.state.dev_mode:
                    print(f"GLOBAL REPUTATION: {severity_type.upper()} reputation spread to {characters_updated} characters across all rooms")
                    print(f"   Trigger event: {change_data['event'].summary}")
                    print(f"   Total {severity_type} events: {len(change_data['all_events'])}")

    def _update_character_memories_new(self, room_name: str) -> None:
        """Update character memories using ReputationService"""
        current_room = self.state.get_current_room()
        if not current_room or not current_room.characters:
            return
        
        # Get reputation context from NEW system
        memory_context = self.reputation_service.get_character_memory_context(room_name)
        room_status = self.reputation_service.get_status(room_name)
        
        # Create detailed witness context
        recent_events = room_status.get("recent_events", [])
        
        for character in current_room.characters:
            # Add global memories
            for global_memory in memory_context["global_memories"]:
                character.remember(global_memory, "assistant")
            
            # Add local witness memories based on recent events
            if recent_events:
                witness_memory = self._create_witness_memory(character, recent_events, room_name)
                if witness_memory:
                    character.remember(witness_memory, "assistant")
        
        if self.state.dev_mode:
            print(f"Updated memories for {len(current_room.characters)} characters in {room_name}")
            print(f"   Recent events from reputation system: {len(recent_events)}")
            print(f"   Local memories: {len(memory_context['local_memories'])}")
            print(f"   Global memories: {len(memory_context['global_memories'])}")

    def refresh_all_character_global_memories(self) -> None:
        """Refresh global memories for all characters (useful after bugs)"""
        
        severities = ["impromptu", "awkward", "dangerous"]
        characters_updated = 0
        
        for severity_str in severities:
            severity = ReputationSeverity(severity_str)
            
            if self.state.reputation.is_global_reputation(severity):
                # Get all events of this severity
                all_events = self.reputation_service._get_all_events_of_severity(severity)
                
                if all_events:
                    # Create global message
                    global_message = self.reputation_service.create_global_reputation_message(
                        severity_str, all_events
                    )
                    
                    # Add to all characters
                    for room in self.state.rooms.values():
                        for character in room.characters:
                            character.remember(global_message, "assistant")
                            characters_updated += 1
        
        if self.state.dev_mode:
            print(f"Refreshed global memories for {characters_updated} characters across all rooms")

    def _create_witness_memory(self, character, recent_events: List[Dict], room_name: str) -> str:
        """Create witness memory from reputation events"""
        if not recent_events:
            return ""
        
        # Get the most recent event
        latest_event = recent_events[0]
        severity = latest_event["severity"]
        summary = latest_event.get("summary", "The detective did something unusual")
        
        # Character's perspective based on role/traits
        if hasattr(character, 'traits') and "authoritative" in character.traits:
            perspective = "As someone of authority, I personally witnessed"
        elif "servant" in character.role.lower() or "governess" in character.role.lower():
            perspective = "As staff member present, I directly observed"
        else:
            perspective = "I was present and personally witnessed"
        
        # Reaction based on severity
        if severity == "dangerous":
            reaction = "This dangerous behavior is deeply alarming and I am genuinely concerned for everyone's safety"
        elif severity == "awkward":
            reaction = "This inappropriate behavior is quite disturbing and makes me very uncomfortable"
        else:  # impromptu
            reaction = "This unusual behavior is concerning and I question the detective's judgment"
        
        return f"DIRECT WITNESS: {perspective} the detective in {room_name}. {summary}. {reaction}. I saw this incident with my own eyes."

    def get_reputation_stats(self) -> Dict[str, Any]:
        """Get reputation statistics from unified system"""
        return self.reputation_service.get_status()

    def clear_reputation_history(self) -> None:
        """Clear reputation history"""
        self.reputation_service.clear_all()
        if self.state.dev_mode:
            print("All reputation history cleared")