"""
Command Prompts
Separated into reasoning, execution and nonsense handling
"""

from .reasoning_agent import create_reasoning_prompt
from .executor_agent import create_command_prompt
from .nonsense_agent import create_nonsense_action_prompt

__all__ = [
    # New separated functions
    'create_reasoning_prompt',
    'create_command_prompt', 
    'create_nonsense_action_prompt',
    
    # Backward compatibility
    'create_command_prompt',
]