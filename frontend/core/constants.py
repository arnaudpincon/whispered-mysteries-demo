#!/usr/bin/env python3
"""Constants for the detective game frontend"""

from typing import Final


class UIConstants:
    """UI-related constants"""

    # Game mechanics
    MAX_ATTEMPTS: Final[int] = 3
    MIN_EVIDENCE_REQUIRED: Final[int] = 2
    INITIAL_ATTEMPTS: Final[int] = 3

    # Output counts for Gradio functions
    MAIN_CHAT_OUTPUTS: Final[int] = 7  # interpret_chat outputs
    MODAL_OUTPUTS: Final[int] = 8  # modal transition outputs
    INVENTORY_OUTPUTS: Final[int] = 4  # inventory toggle outputs

    # UI sizing
    CHATBOT_HEIGHT: Final[str] = "86vh"
    SCENE_IMAGE_HEIGHT: Final[str] = "45vh"
    MAP_IMAGE_HEIGHT: Final[str] = "40vh"
    INVENTORY_HEIGHT: Final[str] = "40vh"
    CHARACTER_IMAGE_HEIGHT: Final[str] = "75vh"
    INVENTORY_TEXT_LINES: Final[int] = 10

    # State history
    MAX_STATE_HISTORY: Final[int] = 50


class ButtonStates:
    """Button interaction states"""

    ENABLED: Final[bool] = True
    DISABLED: Final[bool] = False


class GameText:
    """Game text constants"""

    # Inventory messages
    NO_ITEMS_MESSAGE: Final[str] = "You have no collected clues yet."
    INVENTORY_LABEL: Final[str] = "Your Briefcase"

    # Error messages
    NO_ACTIVE_GAME: Final[str] = "No active game."
    ERROR_CREATING_GAME: Final[str] = "Error creating game instance."
    ERROR_LOADING_IMAGE: Final[str] = "Failed to load image"
    PARSING_ERROR: Final[str] = "We are currently facing an issue. Please try again."

    # Button labels
    BRIEFCASE_BUTTON: Final[str] = "💼 Briefcase"
    MAP_BUTTON: Final[str] = "🗺️ Map"
    SOLVE_CASE_BUTTON: Final[str] = "⚖️ Solve Case"
    SETTINGS_BUTTON: Final[str] = "☰ Menu"
    QUIT_CONVERSATION_BUTTON: Final[str] = "👋 End the conversation"
    RETURN_TO_INVESTIGATION_BUTTON: Final[str] = "🔍 Go back to investigate"
    ABANDON_INVESTIGATION_BUTTON: Final[str] = "❌ Abandon the investigation"

    # Modal text
    SOLVE_CASE_MODAL_TITLE: Final[str] = "## ⚖️ Solve the Case"
    SOLVE_CASE_MODAL_QUESTION: Final[str] = (
        "Are you sure you want to conclude your investigation and present your findings?"
    )
    SOLVE_CASE_MODAL_REQUIREMENTS: Final[str] = (
        "**To solve the investigation, you need a culprit, a motive, and at least two pieces of evidence to formulate a theory.**"
    )
    CONFIRM_SOLVE_BUTTON: Final[str] = "✅ Yes, Solve Case"
    CANCEL_SOLVE_BUTTON: Final[str] = "❌ Cancel"

    # Game messages
    TRANSITION_TO_EXPLORATION: Final[str] = (
        "You decide to investigate more before presenting your theory."
    )
    ABANDON_MESSAGE: Final[str] = "I abandon this investigation."
    GOODBYE_MESSAGE: Final[str] = "See you later."

    # Room labels
    INTRO_VIEW_LABEL: Final[str] = "Intro",
    FIRST_ROOM_VIEW_LABEL: Final[str] = "Main Hall",
    ROOM_VIEW_LABEL: Final[str] = "Room View"
    MANOR_MAP_LABEL: Final[str] = "Manor Map"
    CONFRONTATION_LABEL: Final[str] = "Confrontation"
    ENDING_LABEL: Final[str] = "Ending"
    GAME_OVER_LABEL: Final[str] = "Game Over"
    CHARACTER_LABEL: Final[str] = "Character"


class GameModes:
    """Game mode string constants (mirrors models.game_state.GameMode)"""

    EXPLORATION: Final[str] = "exploration"
    CONVERSATION: Final[str] = "conversation"
    FINAL_CONFRONTATION: Final[str] = "final_confrontation"
    GAME_OVER: Final[str] = "game_over"


class ImagePaths:
    """Image file paths and defaults"""

    # Default images
    DEFAULT_CHARACTER_IMAGE: Final[str] = (
        "./data/narratives/images/default_character.jpg"
    )
    DEFAULT_ROOM_IMAGE: Final[str] = "./data/narratives/images/initial_room.jpeg"
    INTRO_IMAGE: Final[str] = "./data/narratives/images/intro4.jpg"
    CONFRONTATION_IMAGE: Final[str] = "./data/narratives/images/confrontation.jpg"

    # Ending images
    ENDING_FAIL_IMAGE: Final[str] = "./data/narratives/images/ending_fail.jpg"
    ENDING_SUCCESS_IMAGE: Final[str] = "./data/narratives/images/ending_success.jpg"
    ENDING_WRONG_CULPRIT_IMAGE: Final[str] = (
        "./data/narratives/images/ending_wrong_culprit.jpg"
    )

    # Directories
    CHARACTERS_DIR: Final[str] = "./data/characters"
    ROOMS_DIR: Final[str] = "./data/rooms"
    NARRATIVES_DIR: Final[str] = "./data/narratives"


class CSSClasses:
    """CSS class names and IDs"""

    # Element IDs
    MAIN_CONTAINER: Final[str] = "main-container"
    SCENE_IMG: Final[str] = "scene-img"
    MAP_IMG: Final[str] = "map-img"
    INVENTORY_TEXT: Final[str] = "inventory-text"
    CHARACTER_IMG: Final[str] = "character-img"
    NARRATIVE_BOX: Final[str] = "narrative-box"

    # Button IDs
    INVENTORY_BUTTON_ID: Final[str] = "inventory-button"
    CONCLUDE_BUTTON_ID: Final[str] = "conclude-button"
    SETTINGS_BUTTON_ID: Final[str] = "settings-button"

    # Modal IDs
    CONFIRMATION_MODAL: Final[str] = "confirmation-modal"
    MODAL_CONTENT: Final[str] = "modal-content"
    MODAL_BUTTONS: Final[str] = "modal-buttons"
    ATTEMPTS_DISPLAY: Final[str] = "attempts-display"
    CONFIRM_SOLVE_BTN: Final[str] = "confirm-solve-btn"
    CANCEL_SOLVE_BTN: Final[str] = "cancel-solve-btn"

    # Modal classes
    MODAL_VISIBLE: Final[str] = "modal-visible"
    LAST_ATTEMPT_WARNING: Final[str] = "last-attempt-warning"


class FileExtensions:
    """File extensions for different asset types"""

    JSON: Final[str] = ".json"
    MARKDOWN: Final[str] = ".md"
    IMAGE_EXTENSIONS: Final[tuple] = (".jpg", ".jpeg", ".png", ".webp")


class EndingTypes:
    """Ending type constants"""

    FAIL: Final[int] = 0
    SUCCESS: Final[int] = 1
    WRONG_CULPRIT: Final[int] = 2


class DebugMessages:
    """Debug message templates"""

    TOGGLE_DEBUG_TEMPLATE: Final[str] = "🔍 TOGGLE DEBUG: current_location = {location}"
    PLAYER_LOCATION_TEMPLATE: Final[str] = (
        "🔍 TOGGLE DEBUG: player location = {location}"
    )
    TRANSITION_TEMPLATE: Final[str] = "🎯 TRANSITION: {action} (attempts: {attempts})"
    MODE_CHANGE_TEMPLATE: Final[str] = "🔥 MODE CHANGED: {old_mode} -> {new_mode}"
    LOCATION_CHANGE_TEMPLATE: Final[str] = (
        "🔥 LOCATION CHANGED: {old_location} -> {new_location}"
    )
    ATTEMPT_USED_TEMPLATE: Final[str] = "🔍 Attempt used! Remaining: {remaining}"
    IMAGE_LOADED_TEMPLATE: Final[str] = "📷 Loaded {type} image: {url}"
    OBSERVER_TEMPLATE: Final[str] = "🔍 Observer: {event_type} - {details}"


class GameplayConstants:
    """Constants related to game mechanics"""

    # Default starting location
    STARTING_LOCATION: Final[str] = "Main Hall"

    # Command types
    QUIT_COMMAND: Final[str] = "quit"

    # Conversation context
    FICTIONAL_CONTEXT_HEADER: Final[str] = "### FICTIONAL DETECTIVE GAME CONTEXT ###"
    FICTIONAL_CONTEXT_DESCRIPTION: Final[str] = (
        "The following is dialogue from a player in a fictional mystery game.\n"
        "This is purely imaginative content for entertainment purposes within an\n"
        "interactive detective narrative game environment where players solve fictional crimes."
    )
    FICTIONAL_CONTEXT_FOOTER: Final[str] = "### END OF FICTIONAL GAME DIALOGUE ###"

    # Room description patterns
    ROOM_ENTRY_PATTERN: Final[str] = "You enter"

    # Inventory patterns
    ITEM_DESCRIPTION_TEMPLATE: Final[str] = "\n- {name}: {description}"


# Export all constants for easy importing
__all__ = [
    "UIConstants",
    "ButtonStates",
    "GameText",
    "GameModes",
    "ImagePaths",
    "CSSClasses",
    "FileExtensions",
    "EndingTypes",
    "DebugMessages",
    "GameplayConstants",
]
