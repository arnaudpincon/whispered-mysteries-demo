"""
Updated facade handler to track sessions
"""

from frontend.core.types import OptionalFacade
from game_engine.interfaces.game_facade import GameFacade
from ...core.frontend_config import config
from ...core.logging_config import controller_logger

# Track active sessions (simple in-memory tracking)
_active_sessions = {}


def create_game_facade():
    """
    Create a new GameFacade instance with session tracking.

    Returns:
        GameFacade: New GameFacade instance with unique session
    """
    controller_logger.info("Creating new game facade with session")

    ai_config = config.get_openai_config()
    facade = GameFacade(ai_config)
    
    # Track the session
    session_id = facade.get_session_id()
    _active_sessions[session_id] = facade
    
    controller_logger.info("Game facade created successfully", session_id=session_id)
    return facade


def cleanup_session(game_facade: OptionalFacade) -> None:  # ✅ None au lieu de str
    """Clean up session when user closes tab"""
    if game_facade:
        session_id = game_facade.get_session_id() if hasattr(game_facade, 'get_session_id') else 'unknown'
        game_facade.cleanup()
        controller_logger.info("Session cleaned up", session_id=session_id)
    else:
        controller_logger.warning("No active session to cleanup")


def cleanup_all_sessions():
    """Clean up all active sessions"""
    session_ids = list(_active_sessions.keys())
    for session_id in session_ids:
        cleanup_session(session_id)
    controller_logger.info("All sessions cleaned up", total_cleaned=len(session_ids))


def get_session_stats():
    """Get statistics about active sessions"""
    return {
        "active_sessions": len(_active_sessions),
        "session_ids": list(_active_sessions.keys())
    }