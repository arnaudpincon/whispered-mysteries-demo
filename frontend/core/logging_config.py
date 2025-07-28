#!/usr/bin/env python3
"""
Professional logging configuration for the detective game - FIXED VERSION
Replaces print() statements with structured logging
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Import constants for configuration


class GameLoggerConfig:
    """Configuration for game logging system"""

    # Log levels
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    # Default configuration
    DEFAULT_LEVEL = INFO
    DEFAULT_FORMAT = "%(asctime)s | %(name)-12s | %(levelname)-8s | %(funcName)-20s:%(lineno)-4d | %(message)s"
    DEFAULT_DATE_FORMAT = "%H:%M:%S"

    # Console colors for different log levels
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels"""

    def __init__(self, fmt: str, datefmt: str = None, use_colors: bool = True):
        super().__init__()
        self.use_colors = use_colors
        self.fmt = fmt
        self.datefmt = datefmt

        # Create formatters for each level
        self.formatters = {}
        for level_name in GameLoggerConfig.COLORS:
            if level_name != "RESET":
                if self.use_colors:
                    colored_fmt = f"{GameLoggerConfig.COLORS[level_name]}{fmt}{GameLoggerConfig.COLORS['RESET']}"
                else:
                    colored_fmt = fmt
                self.formatters[level_name] = logging.Formatter(colored_fmt, datefmt)

    def format(self, record):
        """Format the log record with appropriate color"""
        formatter = self.formatters.get(record.levelname, self.formatters.get("INFO"))
        return formatter.format(record)


class GameLogger:
    """Enhanced logger with game-specific functionality"""

    def __init__(self, name: str, logger: logging.Logger):
        self.name = name
        self._logger = logger

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with optional context"""
        self._log_with_context(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message with optional context"""
        self._log_with_context(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with optional context"""
        self._log_with_context(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log error message with optional context"""
        self._log_with_context(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """Log critical message with optional context"""
        self._log_with_context(logging.CRITICAL, message, **kwargs)

    def _log_with_context(self, log_level: int, message: str, **kwargs) -> None:
        """Log message with additional context if provided - FIXED VERSION"""
        # Filter out reserved keywords that conflict with logging parameters
        reserved_keywords = {
            "level",
            "msg",
            "args",
            "exc_info",
            "extra",
            "stack_info",
            "stacklevel",
        }

        # Rename conflicting parameters
        filtered_kwargs = {}
        for key, value in kwargs.items():
            if key in reserved_keywords:
                # Rename conflicting parameters with prefix
                filtered_kwargs[f"ctx_{key}"] = value
            else:
                filtered_kwargs[key] = value

        if filtered_kwargs:
            context_str = " | ".join(f"{k}={v}" for k, v in filtered_kwargs.items())
            full_message = f"{message} | {context_str}"
        else:
            full_message = message

        self._logger.log(log_level, full_message)

    # Game-specific logging methods
    def state_change(
        self, old_state: str, new_state: str, reason: str = "", **context
    ) -> None:
        """Log state transitions with optional context"""
        self.info(
            f"State transition: {old_state} → {new_state}",
            transition_reason=reason,
            **context,
        )

    def user_action(self, action: str, details: str = "", **context) -> None:
        """Log user actions with optional context"""
        self.info(f"User action: {action}", action_details=details, **context)

    def game_event(self, event: str, **context) -> None:
        """Log game events with context"""
        self.info(f"Game event: {event}", **context)

    def ui_update(self, component: str, operation: str, **context) -> None:
        """Log UI updates"""
        self.debug(f"UI update: {component}.{operation}", **context)

    def image_operation(
        self, operation: str, image_type: str, url: str = "", **context
    ) -> None:
        """Log image loading operations"""
        self.debug(f"Image {operation}: {image_type}", image_url=url, **context)

    def transition(self, transition_type: str, **context) -> None:
        """Log game state transitions"""
        self.info(f"Transition: {transition_type}", **context)

    def performance(self, operation: str, duration_ms: float, **context) -> None:
        """Log performance metrics with optional context"""
        self.debug(f"Performance: {operation} took {duration_ms:.2f}ms", **context)


def setup_game_logger(
    name: str,
    log_level: str = "INFO",
    enable_file_logging: bool = False,
    log_file_path: Optional[str] = None,
    enable_colors: bool = True,
) -> GameLogger:
    """
    Setup enhanced game logger with consistent formatting

    Args:
        name: Logger name (e.g., "game", "ui", "state")
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        enable_file_logging: Whether to log to file
        log_file_path: Custom log file path
        enable_colors: Whether to use colored output

    Returns:
        GameLogger instance
    """

    logger = logging.getLogger(f"detective_game.{name}")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Avoid duplicate handlers
    if logger.handlers:
        return GameLogger(name, logger)

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Use colored formatter
    console_formatter = ColoredFormatter(
        GameLoggerConfig.DEFAULT_FORMAT,
        GameLoggerConfig.DEFAULT_DATE_FORMAT,
        use_colors=enable_colors,
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if enable_file_logging:
        if log_file_path is None:
            # Create logs directory if it doesn't exist
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)
            log_file_path = (
                logs_dir / f"detective_game_{datetime.now().strftime('%Y%m%d')}.log"
            )

        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # File formatter (no colors)
        file_formatter = logging.Formatter(
            GameLoggerConfig.DEFAULT_FORMAT, GameLoggerConfig.DEFAULT_DATE_FORMAT
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return GameLogger(name, logger)


def get_logger_config_from_env() -> Dict[str, Any]:
    """Get logger configuration from environment variables"""
    return {
        "log_level": os.getenv("GAME_LOG_LEVEL", "INFO"),
        "enable_file_logging": os.getenv("GAME_ENABLE_FILE_LOGGING", "false").lower()
        == "true",
        "enable_colors": os.getenv("GAME_ENABLE_LOG_COLORS", "true").lower() == "true",
        "log_file_path": os.getenv("GAME_LOG_FILE_PATH"),
    }


# Pre-configured loggers for different game components
def create_game_loggers() -> Dict[str, GameLogger]:
    """Create all game loggers with consistent configuration"""

    config = get_logger_config_from_env()

    loggers = {
        "game": setup_game_logger("game", **config),
        "ui": setup_game_logger("ui", **config),
        "state": setup_game_logger("state", **config),
        "image": setup_game_logger("image", **config),
        "transition": setup_game_logger("transition", **config),
        "controller": setup_game_logger("controller", **config),
        "response": setup_game_logger("response", **config),
    }

    return loggers


# Global logger instances
_loggers = create_game_loggers()

# Easy access to loggers
game_logger = _loggers["game"]
ui_logger = _loggers["ui"]
state_logger = _loggers["state"]
image_logger = _loggers["image"]
transition_logger = _loggers["transition"]
controller_logger = _loggers["controller"]
response_logger = _loggers["response"]


def set_log_level(log_level: str) -> None:
    """Set log level for all game loggers"""
    level_value = getattr(logging, log_level.upper(), logging.INFO)
    for logger in _loggers.values():
        logger._logger.setLevel(level_value)


def enable_debug_mode() -> None:
    """Enable debug mode for all loggers"""
    set_log_level("DEBUG")
    game_logger.info("Debug mode enabled for all loggers")


def disable_debug_mode() -> None:
    """Disable debug mode (set to INFO level)"""
    set_log_level("INFO")
    game_logger.info("Debug mode disabled")


def log_startup_info() -> None:
    """Log startup information - FIXED VERSION"""
    game_logger.info("=" * 50)
    game_logger.info("🎮 Detective Game Starting Up")
    game_logger.info("=" * 50)

    # Use different parameter names to avoid conflicts
    game_logger.info(
        "Logging system initialized",
        available_loggers=list(_loggers.keys()),
        current_log_level=os.getenv("GAME_LOG_LEVEL", "INFO"),
    )


def log_shutdown_info() -> None:
    """Log shutdown information"""
    game_logger.info("🎮 Detective Game Shutting Down")
    game_logger.info("=" * 50)


# Context manager for performance logging
class PerformanceTimer:
    """Context manager for logging operation performance"""

    def __init__(self, operation_name: str, logger: GameLogger = game_logger):
        self.operation_name = operation_name
        self.logger = logger
        self.start_time = None

    def __enter__(self):
        import time

        self.start_time = time.time() * 1000  # Convert to milliseconds
        self.logger.debug(f"Starting {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time

        end_time = time.time() * 1000
        duration = end_time - self.start_time

        if exc_type:
            self.logger.error(
                f"Failed {self.operation_name}",
                duration_ms=duration,
                error_info=str(exc_val),
            )
        else:
            self.logger.performance(self.operation_name, duration)


# Export all public interfaces
__all__ = [
    "GameLogger",
    "GameLoggerConfig",
    "setup_game_logger",
    "game_logger",
    "ui_logger",
    "state_logger",
    "image_logger",
    "transition_logger",
    "controller_logger",
    "response_logger",
    "set_log_level",
    "enable_debug_mode",
    "disable_debug_mode",
    "log_startup_info",
    "log_shutdown_info",
    "PerformanceTimer",
]
