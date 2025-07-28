#!/usr/bin/env python3
"""Type definitions for the detective game frontend - FIXED VERSION"""

from abc import ABC, abstractmethod
from enum import Enum

# Import for forward references
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    List,
    NamedTuple,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import gradio as gr
from PIL import Image

if TYPE_CHECKING:
    from game_engine.interfaces.game_facade import GameFacade
    from game_engine.core.game_state import GameMode

# === PROPER TYPE ALIASES ===

# Gradio component types - using proper types
GradioUpdate = Type[gr.update]  # Type of gr.update class
GradioComponent = Union[gr.Button, gr.Image, gr.Textbox, gr.Markdown, gr.ChatInterface]
ImageType = Optional[Image.Image]

# Instead of using gr.update as a type, we'll use Any for the return values
UpdateType = Any  # Represents the return value of gr.update()
ButtonUpdateType = Any  # Represents button update values

# Game data types
GameResponse = Dict[str, Any]
OpenAIConfig = Dict[str, Any]
StateSnapshot = Dict[str, Any]
UIState = Dict[str, Any]

# Callback types
ObserverCallback = Callable[[str, Any], None]
TransitionCallback = Callable[[], None]
ValidationCallback = Callable[[Any], bool]

# === STRUCTURED RESPONSE TYPES ===


class UIUpdateResult(NamedTuple):
    """Type-safe UI update result for main chat interface"""

    message: str
    room_view: Any  # gr.update() return value
    room_map: Any  # gr.update() return value
    inventory_display: Any  # gr.update() return value
    game_controller: "GameFacade"
    inventory_button: Any  # gr.update() return value
    conclude_button: Any  # gr.update() return value
    settings_button: Any  # gr.update() return value


class ModalUpdateResult(NamedTuple):
    """Type-safe result for modal transitions"""

    room_view: Any  # gr.update() return value
    room_map: Any  # gr.update() return value
    inventory_display: Any  # gr.update() return value
    game_controller: "GameFacade"
    inventory_button: Any  # gr.update() return value
    conclude_button: Any  # gr.update() return value
    modal_visibility: Any  # gr.update() return value
    modal_content: Any  # gr.update() return value


class InventoryToggleResult(NamedTuple):
    """Type-safe result for inventory toggle operations"""

    room_map: Any  # gr.update() return value
    inventory_display: Any  # gr.update() return value
    game_controller: "GameFacade"
    inventory_button: Any  # gr.update() return value


class GameResponseData(NamedTuple):
    """Type-safe game response from DetectiveGame"""

    location: str
    room_image_url: str
    message: str
    mode: str
    character_in_conversation: str
    character_image_url: str
    ending: int


class ImagePair(NamedTuple):
    """Type-safe pair of character and room images"""

    character_image: Image.Image
    room_image: Image.Image


# === ENUMS FOR TYPE SAFETY ===


class TransitionType(Enum):
    """Valid transition types for state management"""

    SHOW_MODAL = "show_modal"
    EXIT_CONVERSATION = "exit_conversation"
    RETURN_TO_EXPLORATION = "return_to_exploration"
    ABANDON_INVESTIGATION = "abandon_investigation"
    START_CONFRONTATION = "start_confrontation"


class ButtonState(Enum):
    """Button interaction states"""

    ENABLED = True
    DISABLED = False


class UIMode(Enum):
    """UI display modes"""

    SHOW_MAP = "map"
    SHOW_INVENTORY = "inventory"
    SHOW_CHARACTER = "character"
    SHOW_CONFRONTATION = "confrontation"
    SHOW_ENDING = "ending"


# === PROTOCOLS FOR DUCK TYPING ===


class GameControllerProtocol(Protocol):
    """Protocol defining expected GameFacade interface"""

    def get_current_mode(self) -> "GameMode": ...
    def get_current_location(self) -> str: ...
    def get_attempts_remaining(self) -> int: ...
    def get_show_inventory(self) -> bool: ...
    def is_game_running(self) -> bool: ...
    def interpret_chat(self, command: str) -> GameResponse: ...
    def action_inventory(self) -> str: ...
    def toggle_inventory_view(self) -> bool: ...


class StateManagerProtocol(Protocol):
    """Protocol for state management operations"""

    def add_observer(self, callback: ObserverCallback) -> None: ...
    def remove_observer(self, callback: ObserverCallback) -> None: ...
    def get_state_history(self) -> List[StateSnapshot]: ...
    def validate_state(self) -> Tuple[bool, List[str]]: ...


class ImageLoaderProtocol(Protocol):
    """Protocol for image loading operations"""

    def get_character_image(self, url: str) -> Image.Image: ...
    def get_room_image(self, url: str) -> Image.Image: ...
    def get_special_image(self, image_type: str) -> Image.Image: ...
    def get_ending_image(self, ending_type: int) -> Image.Image: ...


# === GENERIC TYPES ===

T = TypeVar("T")
StateT = TypeVar("StateT")
ResponseT = TypeVar("ResponseT")


class Result(Generic[T]):
    """Generic Result type for error handling"""

    def __init__(self, value: Optional[T] = None, error: Optional[Exception] = None):
        self._value = value
        self._error = error

    @property
    def is_success(self) -> bool:
        return self._error is None

    @property
    def is_error(self) -> bool:
        return self._error is not None

    @property
    def value(self) -> T:
        if self._error:
            raise self._error
        return self._value

    @property
    def error(self) -> Optional[Exception]:
        return self._error

    @classmethod
    def success(cls, value: T) -> "Result[T]":
        return cls(value=value)

    @classmethod
    def failure(cls, error: Exception) -> "Result[T]":
        return cls(error=error)


# === FUNCTION TYPE SIGNATURES ===

# Main UI function signatures
ChatInterpretFunction = Callable[
    [str, List[Dict[str, str]], Optional["GameFacade"]], UIUpdateResult
]
ButtonClickFunction = Callable[
    [], Tuple[Any, Any, Any]
]  # Returns tuple of gr.update() values
TransitionFunction = Callable[[Optional["GameFacade"]], Any]

# State management function signatures
StateValidatorFunction = Callable[["GameFacade"], Tuple[bool, List[str]]]
StateObserverFunction = Callable[[str, Any], None]
StateTransitionFunction = Callable[["GameFacade", str], bool]

# Image handling function signatures
ImageLoaderFunction = Callable[[str], Image.Image]
ImageUpdaterFunction = Callable[[GameResponse, "GameFacade"], ImagePair]

# === CONFIGURATION TYPES ===


class UIConfig(NamedTuple):
    """UI configuration settings"""

    max_attempts: int
    chatbot_height: str
    enable_debug: bool
    log_level: str


class GameConfig(NamedTuple):
    """Game configuration settings"""

    azure_openai_endpoint: str
    azure_openai_api_key: str
    deployment_name: str
    api_version: str
    dev_mode: bool


class ThemeConfig(NamedTuple):
    """Theme and styling configuration"""

    primary_color: str
    secondary_color: str
    background_color: str
    text_color: str
    enable_animations: bool


# === VALIDATION TYPES ===


class ValidationResult(NamedTuple):
    """Result of validation operations"""

    is_valid: bool
    errors: List[str]
    warnings: List[str]


class StateValidation(NamedTuple):
    """Game state validation result"""

    controller_valid: bool
    state_consistent: bool
    ui_synchronized: bool
    errors: List[str]


# === EVENT TYPES ===


class GameEvent(NamedTuple):
    """Game event data structure"""

    event_type: str
    timestamp: float
    data: Dict[str, Any]
    source: str


class UIEvent(NamedTuple):
    """UI event data structure"""

    component: str
    action: str
    value: Any
    timestamp: float


# === ABSTRACT BASE CLASSES ===


class UIHandler(ABC):
    """Abstract base class for UI handlers"""

    @abstractmethod
    def handle_response(self, response: GameResponse) -> UIUpdateResult:
        """Handle game response and return UI updates"""

    @abstractmethod
    def validate_input(self, input_data: Any) -> ValidationResult:
        """Validate input data"""


class StateManager(ABC):
    """Abstract base class for state managers"""

    @abstractmethod
    def update_state(self, updates: Dict[str, Any]) -> bool:
        """Update state with given changes"""

    @abstractmethod
    def get_current_state(self) -> StateSnapshot:
        """Get current state snapshot"""


class TransitionHandler(ABC):
    """Abstract base class for transition handlers"""

    @abstractmethod
    def can_transition(self, from_state: str, to_state: str) -> bool:
        """Check if transition is valid"""

    @abstractmethod
    def execute_transition(self, transition_type: TransitionType) -> Any:
        """Execute the transition"""


# === UTILITY TYPES ===

# Optional types for better readability
OptionalFacade = Optional["GameFacade"]
OptionalString = Optional[str]
OptionalImage = Optional[Image.Image]
OptionalDict = Optional[Dict[str, Any]]

# Union types for common patterns
StringOrNone = Optional[str]
ImageOrNone = Optional[Image.Image]
UpdateOrNone = Optional[Any]  # For gr.update() return values

# List types for collections
StringList = List[str]
ErrorList = List[str]
EventList = List[GameEvent]
HistoryList = List[StateSnapshot]

# Dict types for structured data
ConfigDict = Dict[str, Any]
ResponseDict = Dict[str, Any]
StateDict = Dict[str, Any]
MetricsDict = Dict[str, Union[int, float, str]]

# === TYPE GUARDS ===


def is_valid_controller(obj: Any) -> bool:
    """Type guard for GameFacade"""
    return hasattr(obj, "get_current_mode") and hasattr(obj, "interpret_chat")


def is_valid_response(obj: Any) -> bool:
    """Type guard for game response"""
    required_keys = {"location", "message", "mode"}
    return isinstance(obj, dict) and all(key in obj for key in required_keys)


def is_valid_image(obj: Any) -> bool:
    """Type guard for PIL Image"""
    return isinstance(obj, Image.Image)


def is_gradio_update(obj: Any) -> bool:
    """Type guard for Gradio update objects"""
    # Check if it's a gradio update by looking for typical attributes
    return hasattr(obj, "__dict__") and any(
        attr in str(type(obj)) for attr in ["update", "gradio"]
    )


# === EXPORT ALL TYPES ===

__all__ = [
    # Basic types (fixed)
    "GradioUpdate",
    "GradioComponent",
    "ImageType",
    "UpdateType",
    "ButtonUpdateType",
    "GameResponse",
    "OpenAIConfig",
    "StateSnapshot",
    "UIState",
    "ObserverCallback",
    "TransitionCallback",
    "ValidationCallback",
    # Structured types
    "UIUpdateResult",
    "ModalUpdateResult",
    "InventoryToggleResult",
    "GameResponseData",
    "ImagePair",
    # Enums
    "TransitionType",
    "ButtonState",
    "UIMode",
    # Protocols
    "GameControllerProtocol",
    "StateManagerProtocol",
    "ImageLoaderProtocol",
    # Generic types
    "Result",
    # Function signatures
    "ChatInterpretFunction",
    "ButtonClickFunction",
    "TransitionFunction",
    "StateValidatorFunction",
    "StateObserverFunction",
    "StateTransitionFunction",
    "ImageLoaderFunction",
    "ImageUpdaterFunction",
    # Configuration types
    "UIConfig",
    "GameConfig",
    "ThemeConfig",
    # Validation types
    "ValidationResult",
    "StateValidation",
    # Event types
    "GameEvent",
    "UIEvent",
    # Abstract classes
    "UIHandler",
    "StateManager",
    "TransitionHandler",
    # Utility types
    "OptionalFacade",
    "OptionalString",
    "OptionalImage",
    "OptionalDict",
    "StringOrNone",
    "ImageOrNone",
    "UpdateOrNone",
    "StringList",
    "ErrorList",
    "EventList",
    "HistoryList",
    "ConfigDict",
    "ResponseDict",
    "StateDict",
    "MetricsDict",
    # Type guards
    "is_valid_controller",
    "is_valid_response",
    "is_valid_image",
    "is_gradio_update",
]
