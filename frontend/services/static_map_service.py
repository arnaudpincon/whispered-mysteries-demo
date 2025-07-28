#!/usr/bin/env python3
"""
Simple static map service with fixed player positions
Replaces the complex matplotlib-based map generation
"""

import os
from typing import Dict, Tuple

os.environ["PIL_DISABLE_TKINTER"] = "1"

from PIL import Image, ImageDraw
from pathlib import Path

from ..core.logging_config import PerformanceTimer, state_logger


class StaticMapService:
    """Service for managing a static map with player position overlay"""

    # Hard-coded player positions for each room (x, y coordinates)
    ROOM_POSITIONS: Dict[str, Tuple[int, int]] = {
        # Ground Floor - Left Wing
        "Main Hall": (771, 814),
        "Main Salon": (429, 850),
        "Master's Study": (167, 600),
        "Library": (159, 943),

        # Ground Floor - Right Wing
        "Dining Room": (1114, 814),
        "Kitchen": (1500, 857),
        "Servant's Quarters": (1543, 1100),
        "Cellar": (1757, 857),
        "Stable": (1243, 1071),

        # Upper Floor
        "Landing": (943, 343),
        "Judith's Bedroom": (600, 129),
        "Grand Bathroom": (257, 429),
        "Edgar's Bedroom": (1260, 410),
        "Margarett's Bedroom": (1243, 257),
        "Guest's Bedroom": (943, 125),
        "Master Bedroom": (257, 257),
        "Attic": (1071, 600),
    }

    def __init__(self, map_image_path: str = "./data/narratives/images/manor_map.jpg"):
        """
        Initialize the static map service
        
        Args:
            map_image_path: Path to the base map image
        """
        self.map_image_path = Path(map_image_path)
        self.base_map_image: Image.Image = self._load_base_map()
        
        state_logger.info("StaticMapService initialized", 
                         rooms_count=len(self.ROOM_POSITIONS),
                         map_path=str(self.map_image_path))

    def _load_base_map(self) -> Image.Image:
        """Load the base map image"""
        try:
            if self.map_image_path.exists():
                base_image = Image.open(self.map_image_path)
                state_logger.info("Base map loaded successfully", 
                                size=base_image.size)
                return base_image
            else:
                state_logger.warning("Map image not found, creating fallback",
                                   path=str(self.map_image_path))
                return self._create_fallback_map()
        except Exception as e:
            state_logger.error("Error loading base map", error=str(e))
            return self._create_fallback_map()

    def _create_fallback_map(self) -> Image.Image:
        """Create a simple fallback map if the image is not found"""
        # Create a simple colored rectangle with text
        fallback_map = Image.new("RGB", (800, 500), color="#8B7355")
        draw = ImageDraw.Draw(fallback_map)
        
        # Add title
        draw.text((350, 50), "Blackwood Manor", fill="white", anchor="mm")
        draw.text((350, 80), "Map Image Not Found", fill="red", anchor="mm")
        
        # Add some basic room rectangles as placeholders
        rooms_layout = [
            ("Main Hall", (300, 200, 400, 250)),
            ("Library", (100, 100, 200, 150)),
            ("Kitchen", (500, 200, 600, 250)),
            ("Master Bedroom", (300, 350, 400, 400)),
        ]
        
        for room_name, (x1, y1, x2, y2) in rooms_layout:
            draw.rectangle([x1, y1, x2, y2], outline="black", fill="#D2B48C")
            draw.text((x1 + (x2-x1)//2, y1 + (y2-y1)//2), room_name, 
                     fill="black", anchor="mm")
        
        return fallback_map

    def generate_map_with_player(self, player_location: str) -> Image.Image:
        """
        Generate map with player position indicator
        
        Args:
            player_location: Current room name where player is located
            
        Returns:
            PIL Image with player position marked
        """
        with PerformanceTimer(f"generate_map_with_player_{player_location}", state_logger):
            # Create a copy of the base map to avoid modifying the original
            map_with_player = self.base_map_image.copy()
            
            # Get player position
            player_pos = self.ROOM_POSITIONS.get(player_location)
            
            if player_pos:
                # Draw player indicator
                map_with_player = self._draw_player_indicator(map_with_player, player_pos, player_location)
                state_logger.debug("Player indicator added", 
                                 location=player_location, 
                                 position=player_pos)
            else:
                state_logger.warning("Unknown room position", 
                                   location=player_location,
                                   available_rooms=list(self.ROOM_POSITIONS.keys()))
            
            return map_with_player
        

    def _draw_player_indicator(self, map_image: Image.Image, position: Tuple[int, int], room_name: str) -> Image.Image:
        """
        Draw player indicator on the map
        
        Args:
            map_image: Base map image
            position: (x, y) coordinates for player position
            room_name: Name of the current room
            
        Returns:
            Image with player indicator drawn
        """
        # Create transparent overlay of same size
        overlay = Image.new('RGBA', map_image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        x, y = position
        
        # Parameters
        cross_size = 50
        cross_width = 20
        border_width = 20  # Black border thickness
        cross_color = (255, 0, 0, 255)  # Red
        border_color = (0, 0, 0, 255)   # Black
        
        # Draw black borders first (thicker)
        # Border diagonal \ 
        draw.line(
            [(x - cross_size, y - cross_size), (x + cross_size, y + cross_size)],
            fill=border_color,
            width=cross_width + border_width  # Thicker for border
        )
        
        # Border diagonal /
        draw.line(
            [(x + cross_size, y - cross_size), (x - cross_size, y + cross_size)],
            fill=border_color,
            width=cross_width + border_width  # Thicker for border
        )
        
        # Then draw red X on top (thinner)
        # Red diagonal \ 
        draw.line(
            [(x - cross_size, y - cross_size), (x + cross_size, y + cross_size)],
            fill=cross_color,
            width=cross_width  # Normal thickness
        )
        
        # Red diagonal /
        draw.line(
            [(x + cross_size, y - cross_size), (x - cross_size, y + cross_size)],
            fill=cross_color,
            width=cross_width  # Normal thickness
        )
        
        # Merge with base image
        map_image = map_image.convert('RGBA')
        map_image = Image.alpha_composite(map_image, overlay)
        
        return map_image

    def get_room_position(self, room_name: str) -> Tuple[int, int]:
        """
        Get the position coordinates for a specific room
        
        Args:
            room_name: Name of the room
            
        Returns:
            Tuple of (x, y) coordinates, or (0, 0) if room not found
        """
        return self.ROOM_POSITIONS.get(room_name, (0, 0))

    def add_room_position(self, room_name: str, x: int, y: int) -> None:
        """
        Add or update a room position (useful for dynamic room additions)
        
        Args:
            room_name: Name of the room
            x: X coordinate
            y: Y coordinate
        """
        self.ROOM_POSITIONS[room_name] = (x, y)
        state_logger.info("Room position updated", 
                         room=room_name, 
                         position=(x, y))

    def get_available_rooms(self) -> list[str]:
        """Get list of all rooms with defined positions"""
        return list(self.ROOM_POSITIONS.keys())

    def validate_all_positions(self, room_names: list[str]) -> Dict[str, bool]:
        """
        Validate that all provided room names have defined positions
        
        Args:
            room_names: List of room names to validate
            
        Returns:
            Dictionary mapping room names to whether they have positions defined
        """
        validation_results = {}
        
        for room_name in room_names:
            has_position = room_name in self.ROOM_POSITIONS
            validation_results[room_name] = has_position
            
            if not has_position:
                state_logger.warning("Room missing position definition", 
                                   room=room_name)
        
        missing_count = sum(1 for has_pos in validation_results.values() if not has_pos)
        state_logger.info("Position validation complete", 
                         total_rooms=len(room_names),
                         missing_positions=missing_count)
        
        return validation_results


# Global instance
_static_map_service = None


def get_static_map_service() -> StaticMapService:
    """Get or create the global static map service instance"""
    global _static_map_service
    if _static_map_service is None:
        _static_map_service = StaticMapService()
    return _static_map_service


# Compatibility functions for easy replacement of existing map system
def generate_initial_map(starting_location: str = "Main Hall") -> Image.Image:
    """
    Generate initial map with player position
    
    Args:
        starting_location: Starting room name
        
    Returns:
        PIL Image of the map with player position
    """
    service = get_static_map_service()
    return service.generate_map_with_player(starting_location)


def update_map(location: str) -> Image.Image:
    """
    Update map with new player location
    
    Args:
        location: Current player location
        
    Returns:
        PIL Image of the updated map
    """
    service = get_static_map_service()
    return service.generate_map_with_player(location)


def validate_room_positions(room_list) -> None:
    """
    Validate that all rooms in the game have position definitions
    
    Args:
        room_list: List of Room objects or room names
    """
    service = get_static_map_service()
    
    # Extract room names from Room objects if needed
    if room_list and hasattr(room_list[0], 'name'):
        room_names = [room.name for room in room_list]
    else:
        room_names = room_list
    
    validation_results = service.validate_all_positions(room_names)
    
    missing_rooms = [room for room, has_pos in validation_results.items() if not has_pos]
    
    if missing_rooms:
        print("Warning: The following rooms are missing position definitions:")
        for room in missing_rooms:
            print(f"   - {room}")
        print(f"\nAdd these rooms to ROOM_POSITIONS in StaticMapService")
        print("Default position (0, 0) will be used for missing rooms.")
    else:
        print("All rooms have position definitions")


# Debug function to help with positioning
def debug_room_positions() -> None:
    """Print all defined room positions for debugging"""
    service = get_static_map_service()
    
    print("Defined room positions:")
    for room_name, (x, y) in sorted(service.ROOM_POSITIONS.items()):
        print(f"   {room_name}: ({x}, {y})")
    
    print(f"\nTotal rooms defined: {len(service.ROOM_POSITIONS)}")


if __name__ == "__main__":
    # Test the static map service
    service = StaticMapService()
    
    # Test map generation
    test_map = service.generate_map_with_player("Main Hall")
    print(f"Generated test map with size: {test_map.size}")
    
    # Debug positions
    debug_room_positions()