from dataclasses import dataclass, field
from typing import Dict, List
import time
from enum import Enum


class ReputationSeverity(Enum):
    IMPROMPTU = "impromptu"
    AWKWARD = "awkward"
    DANGEROUS = "dangerous"


@dataclass
class ReputationEvent:
    """A unique reputation event"""
    command: str
    severity: ReputationSeverity
    timestamp: float
    room_name: str
    summary: str = ""


@dataclass
class RoomReputation:
    """Reputation state for a room"""
    room_name: str
    events: List[ReputationEvent] = field(default_factory=list)
   
    def add_event(self, event: ReputationEvent) -> None:
        self.events.append(event)
   
    def get_count_by_severity(self, severity: ReputationSeverity) -> int:
        return len([e for e in self.events if e.severity == severity])
   
    def is_local_reputation(self, severity: ReputationSeverity) -> bool:
        """Check if this room has local reputation for this severity"""
        count = self.get_count_by_severity(severity)
        thresholds = {
            ReputationSeverity.IMPROMPTU: 5,
            ReputationSeverity.AWKWARD: 3,
            ReputationSeverity.DANGEROUS: 1
        }
        return count >= thresholds[severity]
   
    def get_recent_events(self, limit: int = 3) -> List[ReputationEvent]:
        """Return recent events"""
        return sorted(self.events, key=lambda x: x.timestamp, reverse=True)[:limit]


@dataclass
class GlobalReputation:
    """Global reputation state"""
    rooms: Dict[str, RoomReputation] = field(default_factory=dict)
   
    def get_room(self, room_name: str) -> RoomReputation:
        if room_name not in self.rooms:
            self.rooms[room_name] = RoomReputation(room_name)
        return self.rooms[room_name]
   
    def add_event(self, room_name: str, command: str, severity: ReputationSeverity, summary: str = "") -> ReputationEvent:
        """Add an event and return the created event"""
        event = ReputationEvent(
            command=command,
            severity=severity,
            timestamp=time.time(),
            room_name=room_name,
            summary=summary
        )
        self.get_room(room_name).add_event(event)
        return event
   
    def is_global_reputation(self, severity: ReputationSeverity) -> bool:
        """Check if we have global reputation for this severity"""
        if severity == ReputationSeverity.DANGEROUS:
            # Global if 2+ dangerous in ONE room OR dangerous in 2+ rooms
            for room in self.rooms.values():
                if room.get_count_by_severity(severity) >= 2:
                    return True
            dangerous_rooms = [r for r in self.rooms.values() if r.get_count_by_severity(severity) >= 1]
            return len(dangerous_rooms) >= 2
           
        elif severity == ReputationSeverity.AWKWARD:
            # Global if 5+ awkward in ONE room
            for room in self.rooms.values():
                if room.get_count_by_severity(severity) >= 5:
                    return True
            return False
           
        else:  # IMPROMPTU
            # Global if 10+ impromptu in ONE room
            for room in self.rooms.values():
                if room.get_count_by_severity(severity) >= 10:
                    return True
            return False
   
    def get_total_count(self, severity: ReputationSeverity) -> int:
        """Total count of events for a severity"""
        return sum(room.get_count_by_severity(severity) for room in self.rooms.values())
   
    def get_rooms_with_local_reputation(self, severity: ReputationSeverity) -> List[str]:
        """Return rooms with local reputation for this severity"""
        return [room.room_name for room in self.rooms.values() if room.is_local_reputation(severity)]