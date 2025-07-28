"""
Constants and common classes for AI Engine
"""

from typing import Dict, List, Union, Any

# Type alias
GameStateInput = Union[Any, Dict[str, Any]]

class ErrorMessages:
    COMMAND_NOT_UNDERSTOOD = "Sorry, I didn't understand your command."
    CENSORED_RESPONSE = "Might I implore you to rephrase your statement with greater decorum? The Almighty observes all, and discretion is the ally of every true detective."
    THEORY_ERROR = "Forgive me, detective, but the Almighty clouds my understanding of your theory. Could you repeat please ?"
    JSON_PARSE_ERROR = "I'm sorry, there was an error processing your theory. Please try again."
    COMMAND_CENSORED = "Your command eludes me. May the Almighty guide your words anew."

class DefaultAlternatives:
    BASIC_COMMANDS = ["look", "help", "talk", "conclude"]