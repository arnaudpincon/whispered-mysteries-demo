#!/usr/bin/env python3
"""
Image preloader system to avoid threading issues with Gradio
"""

import os

os.environ["PIL_DISABLE_TKINTER"] = "1"
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from PIL import Image


@dataclass
class ImageCache:
    """Thread-safe image cache with preloading capabilities"""

    # Cache storage
    _character_cache: Dict[str, Image.Image] = field(default_factory=dict)
    _room_cache: Dict[str, Image.Image] = field(default_factory=dict)
    _fallback_images: Dict[str, Image.Image] = field(default_factory=dict)

    # Thread safety
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _preload_complete: bool = False

    def __post_init__(self):
        """Initialize fallback images immediately"""
        self._load_fallback_images()

    def _load_fallback_images(self) -> None:
        """Load fallback images that are always available"""
        try:
            self._fallback_images = {
                "character": Image.open(
                    "./data/narratives/images/default_character.jpg"
                ),
                "room": Image.open("./data/narratives/images/initial_room.jpeg"),
                "intro": Image.open("./data/narratives/images/intro4.jpg"),
                "confrontation": Image.open(
                    "./data/narratives/images/confrontation.jpg"
                ),
                "ending_fail": Image.open("./data/narratives/images/ending_fail.jpg"),
                "ending_success": Image.open(
                    "./data/narratives/images/ending_success.jpg"
                ),
                "ending_wrong": Image.open(
                    "./data/narratives/images/ending_wrong_culprit.jpg"
                ),
            }
            print("Fallback images loaded successfully")
        except Exception as e:
            print(f"Error loading fallback images: {e}")
            # Create minimal fallback if files don't exist
            self._create_minimal_fallbacks()

    def _create_minimal_fallbacks(self) -> None:
        """Create minimal fallback images if files are missing"""
        from PIL import Image, ImageDraw

        # Create a simple colored rectangle as fallback
        fallback_img = Image.new("RGB", (400, 300), color="gray")
        draw = ImageDraw.Draw(fallback_img)
        draw.text((180, 140), "Image not found", fill="white")

        self._fallback_images = {
            "character": fallback_img.copy(),
            "room": fallback_img.copy(),
            "intro": fallback_img.copy(),
            "confrontation": fallback_img.copy(),
            "ending_fail": fallback_img.copy(),
            "ending_success": fallback_img.copy(),
            "ending_wrong": fallback_img.copy(),
        }

    def preload_all_images(self) -> None:
        """Preload all game images in a separate thread"""

        def _preload_worker():
            try:
                self._preload_character_images()
                self._preload_room_images()

                with self._lock:
                    self._preload_complete = True

                print("All images preloaded successfully")

            except Exception as e:
                print(f"Error during image preloading: {e}")

        # Start preloading in background thread
        preload_thread = threading.Thread(target=_preload_worker, daemon=True)
        preload_thread.start()

    def _preload_character_images(self) -> None:
        """Preload all character images"""
        characters_dir = Path("./data/characters")

        if not characters_dir.exists():
            print(f"Characters directory not found: {characters_dir}")
            return

        # Scan for character folders
        for char_folder in characters_dir.iterdir():
            if char_folder.is_dir():
                # Look for info.json to get image_url
                info_file = char_folder / "info.json"
                if info_file.exists():
                    try:
                        import json

                        with open(info_file, "r", encoding="utf-8") as f:
                            char_info = json.load(f)

                        image_url = char_info.get("image_url", "")
                        if image_url:
                            image_path = characters_dir / image_url
                            if image_path.exists():
                                with self._lock:
                                    self._character_cache[image_url] = Image.open(
                                        image_path
                                    )
                                print(f"Preloaded character image: {image_url}")
                    except Exception as e:
                        print(f"Error preloading character {char_folder.name}: {e}")

    def _preload_room_images(self) -> None:
        """Preload all room images"""
        rooms_dir = Path("./data/rooms")

        if not rooms_dir.exists():
            print(f"Rooms directory not found: {rooms_dir}")
            return

        # Scan for room folders
        for room_folder in rooms_dir.iterdir():
            if room_folder.is_dir():
                # Look for info.json to get image_url
                info_file = room_folder / "info.json"
                if info_file.exists():
                    try:
                        import json

                        with open(info_file, "r", encoding="utf-8") as f:
                            room_info = json.load(f)

                        image_url = room_info.get(
                            "image", ""
                        )  # Note: "image" not "image_url" for rooms
                        if image_url:
                            image_path = rooms_dir / image_url
                            if image_path.exists():
                                with self._lock:
                                    self._room_cache[image_url] = Image.open(image_path)
                                print(f"Preloaded room image: {image_url}")
                    except Exception as e:
                        print(f"Error preloading room {room_folder.name}: {e}")

    def get_character_image(self, image_url: str) -> Image.Image:
        """Get character image from cache or fallback"""
        if not image_url:
            return self._fallback_images["character"]

        with self._lock:
            cached_image = self._character_cache.get(image_url)
            if cached_image:
                return cached_image

        # Try to load on-demand if not in cache
        try:
            image_path = Path(f"./data/characters/{image_url}")
            if image_path.exists():
                loaded_image = Image.open(image_path)

                # Cache for future use
                with self._lock:
                    self._character_cache[image_url] = loaded_image

                return loaded_image
        except Exception as e:
            print(f"Failed to load character image {image_url}: {e}")

        # Return fallback
        return self._fallback_images["character"]

    def get_room_image(self, image_url: str) -> Image.Image:
        """Get room image from cache or fallback"""
        if not image_url:
            return self._fallback_images["room"]

        with self._lock:
            cached_image = self._room_cache.get(image_url)
            if cached_image:
                return cached_image

        # Try to load on-demand if not in cache
        try:
            image_path = Path(f"./data/rooms/{image_url}")
            if image_path.exists():
                loaded_image = Image.open(image_path)

                # Cache for future use
                with self._lock:
                    self._room_cache[image_url] = loaded_image

                return loaded_image
        except Exception as e:
            print(f"Failed to load room image {image_url}: {e}")

        # Return fallback
        return self._fallback_images["room"]

    def get_special_image(self, image_type: str) -> Image.Image:
        """Get special images (intro, confrontation, endings)"""
        return self._fallback_images.get(image_type, self._fallback_images["room"])

    def get_ending_image(self, ending_type: int) -> Image.Image:
        """Get appropriate ending image based on ending type"""
        if ending_type == 0:
            return self._fallback_images["ending_fail"]
        elif ending_type == 1:
            return self._fallback_images["ending_success"]
        else:
            return self._fallback_images["ending_wrong"]

    def is_preload_complete(self) -> bool:
        """Check if preloading is complete"""
        with self._lock:
            return self._preload_complete

    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics for debugging"""
        with self._lock:
            return {
                "characters_cached": len(self._character_cache),
                "rooms_cached": len(self._room_cache),
                "fallbacks_loaded": len(self._fallback_images),
                "preload_complete": self._preload_complete,
            }


# Global image cache instance
image_cache = ImageCache()


def initialize_image_system() -> None:
    """Initialize the image system and start preloading"""
    print("Starting image system initialization...")
    image_cache.preload_all_images()
    print("Image system initialized")


# Convenience functions for easy access
def get_character_image(image_url: str) -> Image.Image:
    """Get character image safely"""
    return image_cache.get_character_image(image_url)


def get_room_image(image_url: str) -> Image.Image:
    """Get room image safely"""
    return image_cache.get_room_image(image_url)


def get_special_image(image_type: str) -> Image.Image:
    """Get special image safely"""
    return image_cache.get_special_image(image_type)


def get_ending_image(ending_type: int) -> Image.Image:
    """Get ending image safely"""
    return image_cache.get_ending_image(ending_type)


def get_cache_stats() -> Dict[str, int]:
    """Get cache statistics"""
    return image_cache.get_cache_stats()