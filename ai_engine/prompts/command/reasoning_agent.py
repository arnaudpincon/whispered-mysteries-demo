from ai_engine.prompts.prompt_config import get_current_teleportation


def create_reasoning_prompt(game_state_str: str, command: str) -> str:
    """
    Creates a reasoning prompt that analyzes the player's command and game state.
    This prompt focuses purely on understanding and validation.
    Args:
        game_state_str: Current state of the game as a string
        command: Player's input command in any language
    Returns:
        A formatted prompt string for command analysis
    """

    # Get teleportation mode
    teleportation_enabled = get_current_teleportation()
    
    # Modify movement validation rules based on teleportation mode
    if teleportation_enabled:
        movement_rules = """
    - For "move" action: the target room MUST exist in the game state (teleportation mode - can move to any room)"""
    else:
        movement_rules = """
    - For "move" action: the target room MUST be in the "Possible exits" list (connected rooms only)
    - If trying to move to a non-connected room, the command is INVALID
    """
    
    return f"""You are a detective game command analyzer. Your job is to understand and validate player commands.

    Current game state:
    {game_state_str}

    Player's command: "{command}"

    GAME RULES:
    The player can ONLY perform these 6 actions:
    1. "look" - inspect/examine a character, clue, location or their inventory
    2. "speak" - talk to a character  
    3. "collect" - take/collect a clue
    4. "move" - move to another location
    5. "help" - ask for help
    6. "nonsense" - attempt unrealistic actions like fighting, destroying objects, or other non-detective behaviors

    CRITICAL VALIDATION RULES:
    - The player can target ONLY ONE entity per command (no multiple targets)
    - The target entity MUST exist exactly in the current game state
    - {movement_rules}
    - If multiple targets are detected, the command is INVALID
    - If the target doesn't exist in the game state, the command is INVALID
    - If the targeted character has status "dead", TALKING to them is INVALID

    ANALYSIS STEPS:
    1. List ALL entities (characters, locations, clues) that exist in the current game state
    3. Detect the language of the player's command
    4. Translate the command to English for analysis
    5. Identify what action the player wants to perform (must be one of the 6 above)
    6. Identify what single target the player is referring to
    7. Check if multiple targets are mentioned (if yes, command is INVALID)
    8. Map the target name to its canonical English name from the game state
    9. Verify the target EXISTS in the game state (if not, command is INVALID)
    10. Validate if the action can be performed on that target type

    COMMAND CATEGORIES (with multilingual examples):
    - "help": help, aide (French), ayuda (Spanish), Hilfe (German)
    - "move": go, walk, move to, aller (French), ir (Spanish), gehen (German)  
    - "speak": talk to, speak with, parler (French), hablar (Spanish), sprechen (German)
    - "collect": take, pick up, prendre (French), tomar (Spanish), nehmen (German)
    - "look": look at, examine, inspect, regarder (French), mirar (Spanish), ansehen (German)
    - "nonsense": any command that doesn't fit the above categories, e.g., "hit", "insult", "undress", "eat", "drink", "sleep", etc.

    TARGET MATCHING RULES:
    - The target name must map to an entity that EXISTS in the current game state
    - Allow reasonable synonyms (e.g., "paper" for "letter", "blade" for "knife")
    - Consider partial matches and semantic equivalents
    - If no exact match exists in game state, command is INVALID

    Respond in JSON format:
    {{
        "entities_in_game": ["list", "of", "all", "entities", "from", "game", "state"],
        "possible_exits": ["list", "of", "connected", "rooms"],
        "detected_language": "language_name",
        "translated_command": "english_translation",
        "intended_action": "move/speak/collect/look/help/nonsense",
        "intended_target": "single_target_name_in_canonical_english",
        "multiple_targets_detected": true/false,
        "target_exists_in_game": true/false,
        "target_type": "character/location/clue/inventory/none",
        "reasoning": "detailed explanation of your analysis",
        "validation_result": "valid/invalid",
        "validation_reason": "specific reason why valid or invalid"
    }}
    """