"""
Story Prompts
Separated into specialized agents for story generation and object interaction
"""

from .room_description_agent import create_room_description_prompt
from .character_description_agent import create_character_description_prompt
from .clue_analysis_agent import create_clue_analysis_prompt
from .ending_writer_agent import create_write_ending
from .object_inspector_agent import create_inspect_object_prompt

__all__ = [
    'create_room_description_prompt',
    'create_character_description_prompt',
    'create_clue_analysis_prompt',
    'create_write_ending',
    'create_inspect_object_prompt',
]