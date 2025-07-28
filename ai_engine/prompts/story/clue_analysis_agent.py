"""
Clue Analysis Agent
Handles analysis and insights for discovered clues
"""

from ai_engine.prompts.prompt_config import get_rules_prompt


def create_clue_analysis_prompt(clue, collected_clues=None) -> str:
    """
    Create the prompt for clue analysis.

    Args:
        clue: The newly discovered clue object (must have name, description, room_name attributes)
        collected_clues: Optional list of previously collected clues

    Returns:
        Formatted prompt string for clue analysis
    """
    rules_prompt = get_rules_prompt()
    
    clue_info = _extract_clue_info(clue)
    analysis_instructions = _get_analysis_instructions()
    
    return f"""You are a detective game narrator analyzing a newly discovered clue.

        {clue_info}

        {analysis_instructions}

        {rules_prompt}"""


def _extract_clue_info(clue) -> str:
    """Extract clue information for the prompt"""
    return f"""Newly discovered clue: {clue.name}
        Description: {clue.description}
        Location: Found in {clue.room_name}"""


def _get_analysis_instructions() -> str:
    """Get the analysis instructions for the clue"""
    return """INSTRUCTIONS:
        - Keep it brief (2-3 sentences max)
        - Address the player directly with "you"
        - Describe how they find the clue
        - Focus on building intrigue and advancing the mystery narrative"""