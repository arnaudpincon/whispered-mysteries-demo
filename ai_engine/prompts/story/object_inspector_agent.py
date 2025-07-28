"""
Object Inspector Agent
Handles inspection of non-clue objects and items
"""

from ai_engine.prompts.prompt_config import get_rules_prompt


def create_inspect_object_prompt(object_name: str) -> str:
    """
    Create prompt for inspecting non-clue objects
    
    Args:
        object_name: Name of the object to inspect
        
    Returns:
        Formatted prompt for object inspection
    """
    rules_prompt = get_rules_prompt()
    
    object_info = _format_object_info(object_name)
    inspection_instructions = _get_inspection_instructions()
    response_format = _get_response_format(object_name)
    
    return f"""
    You are a game manager for a detective game.

    {object_info}
    
    {inspection_instructions}
    
    {response_format}
    
    {rules_prompt}
    """


def _format_object_info(object_name: str) -> str:
    """Format the object information section"""
    return f'OBJECT TO EXAMINE: "{object_name}"'


def _get_inspection_instructions() -> str:
    """Get the inspection instructions"""
    return """INSTRUCTIONS:
    Respond directly to the detective, mentioning the object they are examining and saying there is nothing special about it.
    
    Respond with a short and simple sentence."""


def _get_response_format(object_name: str) -> str:
    """Get the response format guidelines"""
    return f"""Format: "You examine [object name], but there is nothing special about it."
    
    Replace [object name] with the object mentioned by the player."""