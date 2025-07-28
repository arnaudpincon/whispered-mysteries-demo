from typing import Dict, List, Tuple, Any
from game_engine.models.reputation import GlobalReputation, ReputationSeverity

class ReputationService:
    """Unified service for ALL reputation management"""
    
    def __init__(self, reputation: GlobalReputation):
        self.reputation = reputation
    
    def process_nonsense_action(self, room_name: str, command: str, severity_str: str, summary: str = "") -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Process a nonsense action and detect global changes
        
        Returns:
            Tuple[bool, List[str], Dict]: (game_over, warnings, global_changes)
        """
        try:
            severity = ReputationSeverity(severity_str)
        except ValueError:
            severity = ReputationSeverity.AWKWARD
        
        # Check game over BEFORE adding the event
        if severity == ReputationSeverity.DANGEROUS and self.reputation.is_global_reputation(ReputationSeverity.DANGEROUS):
            return True, ["EXPELLED FROM MANOR"], {}
        
        # Capture global state BEFORE the action
        old_global_status = {
            "impromptu": self.reputation.is_global_reputation(ReputationSeverity.IMPROMPTU),
            "awkward": self.reputation.is_global_reputation(ReputationSeverity.AWKWARD),
            "dangerous": self.reputation.is_global_reputation(ReputationSeverity.DANGEROUS)
        }
        
        # Add the event
        event = self.reputation.add_event(room_name, command, severity, summary)
        
        # Capture global state AFTER the action
        new_global_status = {
            "impromptu": self.reputation.is_global_reputation(ReputationSeverity.IMPROMPTU),
            "awkward": self.reputation.is_global_reputation(ReputationSeverity.AWKWARD),
            "dangerous": self.reputation.is_global_reputation(ReputationSeverity.DANGEROUS)
        }
        
        # Detect global changes
        global_changes = {}
        for severity_type in ["impromptu", "awkward", "dangerous"]:
            if not old_global_status[severity_type] and new_global_status[severity_type]:
                global_changes[severity_type] = {
                    "became_global": True,
                    "event": event,
                    "all_events": self._get_all_events_of_severity(ReputationSeverity(severity_type))
                }
        
        # Generate warnings
        warnings = self._generate_warnings(room_name)
        
        return False, warnings, global_changes
    
    def _get_all_events_of_severity(self, severity: ReputationSeverity) -> List[Dict[str, Any]]:
        """Get all events of a given severity from all rooms"""
        all_events = []
        for room_name, room_rep in self.reputation.rooms.items():
            for event in room_rep.events:
                if event.severity == severity:
                    all_events.append({
                        "command": event.command,
                        "summary": event.summary,
                        "room": room_name,
                        "timestamp": event.timestamp
                    })
        return sorted(all_events, key=lambda x: x["timestamp"], reverse=True)
    
    def create_global_reputation_message(self, severity_type: str, all_events: List[Dict]) -> str:
        """Create a global reputation message for all characters"""
        
        if severity_type == "dangerous":
            reputation_desc = "dangerous and violent behavior"
            concern_level = "Everyone in the manor is genuinely afraid and concerned for their safety"
        elif severity_type == "awkward":
            reputation_desc = "eccentric and inappropriate behavior" 
            concern_level = "The detective has become the talk of the entire household"
        else:  # impromptu
            reputation_desc = "peculiar social habits"
            concern_level = "Amusing stories about the detective circulate throughout the manor"
        
        # List affected rooms
        affected_rooms = list(set(event["room"] for event in all_events))
        rooms_text = ", ".join(affected_rooms[:3])
        if len(affected_rooms) > 3:
            rooms_text += f" and {len(affected_rooms) - 3} other locations"
        
        # Sample of notable events
        notable_events = [event["summary"] for event in all_events[:3]]
        events_text = ". ".join(notable_events)
        
        return f"MANOR-WIDE REPUTATION: The detective's {reputation_desc} has spread throughout Blackwood Manor. Word from {rooms_text} includes: {events_text}. {concern_level}."
    
    def _generate_warnings(self, current_room: str) -> List[str]:
        """Generate reputation warnings"""
        warnings = []
        room_rep = self.reputation.get_room(current_room)
        
        # Critical warnings
        if self.reputation.is_global_reputation(ReputationSeverity.DANGEROUS):
            warnings.append("CRITICAL: Next dangerous action = IMMEDIATE EXPULSION!")
        else:
            dangerous_count = room_rep.get_count_by_severity(ReputationSeverity.DANGEROUS)
            if dangerous_count == 1:
                warnings.append("DANGER: One more dangerous action in this room = global reputation!")
            elif dangerous_count == 0:
                warnings.append("WARNING: Dangerous actions have serious consequences")
        
        # Other warnings
        awkward_count = room_rep.get_count_by_severity(ReputationSeverity.AWKWARD)
        if awkward_count == 4:
            warnings.append("One more awkward action in this room = global eccentric reputation")
        elif awkward_count == 2:
            warnings.append("Two more awkward actions = local awkward reputation")
        
        # Current status
        if self.reputation.is_global_reputation(ReputationSeverity.AWKWARD):
            warnings.append("You have an eccentric reputation throughout the manor")
        elif room_rep.is_local_reputation(ReputationSeverity.AWKWARD):
            warnings.append(f"You have an awkward reputation in {current_room}")
            
        return warnings
    
    def get_status(self, room_name: str = None) -> Dict[str, Any]:
        """Return complete reputation status"""
        if room_name:
            room_rep = self.reputation.get_room(room_name)
            return {
                "current_room": room_name,
                "room_counts": {
                    "impromptu": room_rep.get_count_by_severity(ReputationSeverity.IMPROMPTU),
                    "awkward": room_rep.get_count_by_severity(ReputationSeverity.AWKWARD),
                    "dangerous": room_rep.get_count_by_severity(ReputationSeverity.DANGEROUS)
                },
                "local_status": {
                    "impromptu": room_rep.is_local_reputation(ReputationSeverity.IMPROMPTU),
                    "awkward": room_rep.is_local_reputation(ReputationSeverity.AWKWARD),
                    "dangerous": room_rep.is_local_reputation(ReputationSeverity.DANGEROUS)
                },
                "global_status": {
                    "impromptu": self.reputation.is_global_reputation(ReputationSeverity.IMPROMPTU),
                    "awkward": self.reputation.is_global_reputation(ReputationSeverity.AWKWARD),
                    "dangerous": self.reputation.is_global_reputation(ReputationSeverity.DANGEROUS)
                },
                "recent_events": [
                    {"command": e.command, "severity": e.severity.value, "summary": e.summary}
                    for e in room_rep.get_recent_events()
                ]
            }
        
        return {
            "total_counts": {
                "impromptu": self.reputation.get_total_count(ReputationSeverity.IMPROMPTU),
                "awkward": self.reputation.get_total_count(ReputationSeverity.AWKWARD),
                "dangerous": self.reputation.get_total_count(ReputationSeverity.DANGEROUS)
            },
            "rooms_with_reputation": {
                "impromptu": self.reputation.get_rooms_with_local_reputation(ReputationSeverity.IMPROMPTU),
                "awkward": self.reputation.get_rooms_with_local_reputation(ReputationSeverity.AWKWARD), 
                "dangerous": self.reputation.get_rooms_with_local_reputation(ReputationSeverity.DANGEROUS)
            }
        }
    
    def get_character_memory_context(self, room_name: str) -> Dict[str, List[str]]:
        """Return context for character memory"""
        room_rep = self.reputation.get_room(room_name)
        recent_events = room_rep.get_recent_events(3)
        
        local_memories = []
        global_memories = []
        
        # Local memories (direct witness)
        if recent_events:
            if room_rep.is_local_reputation(ReputationSeverity.DANGEROUS):
                local_memories.append(f"I personally witnessed the detective's dangerous behavior in {room_name}")
            elif room_rep.is_local_reputation(ReputationSeverity.AWKWARD):
                local_memories.append(f"I observed the detective's strange behavior in {room_name}")
        
        # Global memories (rumors)
        if self.reputation.is_global_reputation(ReputationSeverity.DANGEROUS):
            global_memories.append("Word has spread throughout the manor about the detective's dangerous reputation")
        elif self.reputation.is_global_reputation(ReputationSeverity.AWKWARD):
            global_memories.append("The detective has gained an eccentric reputation throughout the manor")
        
        return {
            "local_memories": local_memories,
            "global_memories": global_memories
        }
    
    def clear_all(self) -> None:
        """Complete reset of the reputation system"""
        self.reputation.rooms.clear()