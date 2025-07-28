"""
AI Prompts
Template and prompt generation for different game scenarios
"""

# Character prompts
from .character import (
    create_neutral_character_prompt,
    create_personality_character_prompt,
    create_get_lore_information,
    create_conversation_summary_prompt,
    create_player_analysis_prompt,
)

# Story prompts
from .story import (
    create_room_description_prompt,
    create_clue_analysis_prompt,
    create_write_ending,
    create_character_description_prompt,
    create_inspect_object_prompt,
)

# Theory prompts
from .theory import (
    create_collect_theory,
    create_analyse_theory,
)

# Language support
from .prompt_config import (
    get_current_language,
    get_current_teleportation,
    get_rules_prompt,
)

__all__ = [
    # Character
    'create_neutral_character_prompt',
    'create_personality_character_prompt',
    'create_get_lore_information',
    'create_conversation_summary_prompt',

    # Command
    'create_reasoning_prompt',
    'create_command_prompt',
   
    # Story
    'create_room_description_prompt',
    'create_clue_analysis_prompt',
    'create_write_ending',
    'create_character_description_prompt',
   
    # Theory
    'create_collect_theory',
    'create_analyse_theory',
   
    # Utility
    'create_inspect_object_prompt',
    'create_player_analysis_prompt',
   
    # Language
    'get_current_language',
    'get_current_teleportation',
    'get_rules_prompt'
]