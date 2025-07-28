"""
AI Engine Utilities
Formatting, tools, and helper functions
"""

from .constants import ErrorMessages, DefaultAlternatives, GameStateInput

from .formatters import (
    format_game_state,
    clue_game_state,
    validate_game_state_format,
    debug_game_state_structure
)

from .tools import (
    get_agent_tools,
    get_conversation_tools,
    get_collect_theory_tools,
    get_analyse_theory_tools,
    get_write_ending_tools,
    get_process_command_tools
)

from .personality import (
    PersonalityContext,
    generate_personality_instructions,
    create_personality_context
)

__all__ = [
    # Formatters
    'format_game_state',
    'clue_game_state', 
    'validate_game_state_format',
    'debug_game_state_structure',
    
    # Tools
    'get_agent_tools',
    'get_conversation_tools',
    'get_collect_theory_tools',
    'get_analyse_theory_tools', 
    'get_write_ending_tools',
    'get_process_command_tools',
    
    # Personality
    'PersonalityContext',
    'generate_personality_instructions',
    'create_personality_context'

    # Logs
    'log_ai_response',
    'enable_ai_logging', 
    'disable_ai_logging',
]