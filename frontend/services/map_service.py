#!/usr/bin/env python3
"""
Map service - Static simple version with fixed image and hardcoded positions
"""

from typing import Any, List

from PIL import Image

from game_engine.setup.game_data import create_rooms

from ..core.logging_config import PerformanceTimer, state_logger
from .static_map_generator import get_static_map_service, validate_room_positions


class MapService:
    """Service dedicated to generating and managing static maps"""

    def __init__(self):
        """Initialize map service with static map system"""
        with PerformanceTimer("map_service_init", state_logger):
            self.room_list: List[Any] = create_rooms()
            self.static_service = get_static_map_service()
            
            # Validate that all rooms have position definitions
            validate_room_positions(self.room_list)
            
            state_logger.info("MapService initialized", 
                            rooms_count=len(self.room_list),
                            service_type="static")

    def generate_initial_map(self, starting_location: str = "Main Hall") -> Image.Image:
        """
        Generate the initial map with performance logging

        Args:
            starting_location: Starting location for the player

        Returns:
            PIL Image of the initial manor map with player position
        """
        with PerformanceTimer("generate_initial_map", state_logger):
            initial_map_image: Image.Image = self.static_service.generate_map_with_player(starting_location)

            state_logger.info(
                "Generated initial map",
                location=starting_location,
                rooms_count=len(self.room_list),
                map_size=initial_map_image.size
            )
            return initial_map_image

    def update_map(self, location: str) -> Image.Image:
        """
        Updates the map with the player's new location

        Args:
            location: Current player location name

        Returns:
            PIL Image of the updated map with player position
        """
        with PerformanceTimer(f"update_map_{location}", state_logger):
            updated_map_image: Image.Image = self.static_service.generate_map_with_player(location)

            state_logger.debug("Updated map", 
                             location=location,
                             map_size=updated_map_image.size)
            return updated_map_image

    def get_room_count(self) -> int:
        """Get total number of rooms"""
        return len(self.room_list)

    def get_room_names(self) -> List[str]:
        """Get list of all room names"""
        return [room.name for room in self.room_list]

    def get_room_position(self, room_name: str) -> tuple[int, int]:
        """
        Get position coordinates for a specific room
        
        Args:
            room_name: Name of the room
            
        Returns:
            Tuple of (x, y) coordinates
        """
        return self.static_service.get_room_position(room_name)

    def validate_room_positions(self) -> dict[str, bool]:
        """
        Validate that all game rooms have position definitions
        
        Returns:
            Dictionary mapping room names to whether they have positions
        """
        room_names = self.get_room_names()
        return self.static_service.validate_all_positions(room_names)

    def debug_positions(self) -> None:
        """Debug method to print all room positions"""
        state_logger.info("=== ROOM POSITIONS DEBUG ===")
        
        for room in self.room_list:
            position = self.get_room_position(room.name)
            state_logger.info(f"Room: {room.name}", position=position)
        
        # Check for missing positions
        validation = self.validate_room_positions()
        missing_rooms = [room for room, has_pos in validation.items() if not has_pos]
        
        if missing_rooms:
            state_logger.warning("Missing position definitions", rooms=missing_rooms)
        else:
            state_logger.info("All rooms have position definitions")


# Global instance for compatibility with old code
_map_service_instance = None


def get_map_service() -> MapService:
    """Get or create the global map service instance"""
    global _map_service_instance
    if _map_service_instance is None:
        _map_service_instance = MapService()
    return _map_service_instance


# Compatibility functions for old code
def generate_initial_map(starting_location: str = "Main Hall") -> Image.Image:
    """Compatibility function for old MapManager.generate_initial_map()"""
    return get_map_service().generate_initial_map(starting_location)


def update_map(location: str) -> Image.Image:
    """Compatibility function for old MapManager.update_map()"""
    return get_map_service().update_map(location)


# Utility function to debug positions
def debug_all_room_positions() -> None:
    """Debug function to print all room positions"""
    service = get_map_service()
    service.debug_positions()


if __name__ == "__main__":
    # Test the new service
    service = MapService()
    
    print("MAP SERVICE TEST")
    print(f"Total rooms: {service.get_room_count()}")
    
    # Test initial map
    initial_map = service.generate_initial_map("Main Hall")
    print(f"Initial map generated: {initial_map.size}")
    
    # Test update map
    updated_map = service.update_map("Kitchen")
    print(f"Updated map generated: {updated_map.size}")
    
    # Debug positions
    debug_all_room_positions()
    
    # Validation
    validation = service.validate_room_positions()
    missing_count = sum(1 for has_pos in validation.values() if not has_pos)
    print(f"Position validation: {len(validation) - missing_count}/{len(validation)} rooms have positions")