# Not used

"""
Analysis Character Agent  
Handles player behavior and tone analysis for character interactions
"""

from ai_engine.prompts.prompt_config import get_rules_prompt
from game_engine.models.character import Character
from game_engine.models.player import Player


def create_player_analysis_prompt(
    game_state_str: str, 
    player: Player,
    character: Character,
    player_input: str, 
) -> str:
    """
    Create a reasoning prompt to analyze player tone and behavior.
    Args:
        player_input: What the player just said
        game_state_str: Current game state
        character: Character being addressed
    Returns:
        Analysis prompt for player behavior
    """
    return f"""
        # DETECTIVE BEHAVIOR ANALYSIS

        Analyze the detective's input and provide reasoning guidance:

        Detective said: "{player_input}"
        Addressing: {character.name} ({character.role})

        Game state:
        {game_state_str}

        ## ANALYSIS REQUIRED:

        **Detective Tone**: 
        - SERIOUS: Focused on investigation, formal language
        - HUMOROUS: Making jokes, playful references
        - CONFUSED: Asking for clarification, seems lost
        - ABSURD: Nonsensical, testing boundaries
        - AGGRESSIVE: Demanding, confrontational
        - CASUAL: Relaxed conversation, friendly

        **Response Strategy**:
        - How should {character.name} react to this tone?
        - Should they correct any misinformation?
        - What level of detail should they provide?
        - Decide if the character has to stop the conversation or not

        Provide short, direct analysis focusing on tone detection and response guidance.
        """