from ai_engine.prompts.prompt_config import get_rules_prompt


def _get_validation_rules() -> str:
    """Helper function to return validation rules section"""
    return """
    EXECUTION RULES:
    - If validation_result is "valid": execute the intended action
    - If validation_result is "invalid": try to respond to the player's intent when possible

    INVALID COMMAND CASES:
    - Multiple targets detected (player can only target ONE entity at a time)
    - Target doesn't exist in the current game state
    - Action type not allowed (only: look, speak, collect, move, help, nonsense)
    - Action incompatible with target type (e.g., "speak" to a clue)

    ACTION-TARGET COMPATIBILITY:
    - "look": can target any character, clue, or location
    - "speak": can only target characters
    - "collect": can only target clues
    - "move": can only target locations
    - "help": no target needed
    - "nonsense": no target needed
    """


def _get_narrative_guidelines() -> str:
    """Helper function to return narrative and immersion guidelines"""
    return """
    RESPONSE STRATEGY FOR INVALID COMMANDS:
    - Try to understand what the player wants to do
    - If possible, suggest the closest valid action
    - If the target doesn't exist, describe what the player sees instead
    - If the action is impossible, explain why in-world terms with immersive responses
    - If the player asks a question, answer based on what you know from the game state
    - Never mention non-existent entities or make up information not in the game state
    - NEVER use phrases like "this is not a possible action" or "you cannot do that"
    - NEVER mention the location or position of characters who are not present in the current room
    - Instead, respond with immersive, dismissive descriptions that stay in character
    - For elements that logically exist in a room but aren't interactable game elements, acknowledge the action but dismiss it
    - Examples of good responses:
    * "You have other things to do than eat an apple"
    * "That knife on the table doesn't seem particularly noteworthy"
    * "Inspector Ferdinand shout at you: 'What are you doing Detective ??? Are you crazy?'"
    * "Lord Blackwood: "Are you completely drunk, Detective? Have you lost your mind?'"
    * "Edgar Holloway: "I've treated patients less deranged than you, Detective."
    * "Lady Blackwood: "How dare you?! This is outrageous!""
    * "You speak to your bag, but it doesn't answer. It's just a bag after all"
    * "You try to talk to someone named George, but there's no George in this room"
    * "You pick up the pen, but see nothing relevant. You put it back in its place"
    * "You examine the sink, there's nothing special about it"
    * "You look at the window, it shows the garden outside but nothing noteworthy"
    - Always maintain immersion and provide alternatives
    """


def _get_response_guidelines() -> str:
    """Helper function to return response formatting guidelines"""
    return """
    RESPONSE GUIDELINES:
    - Keep error messages brief and clear
    - Provide 2-3 relevant alternatives when command is invalid
    - Alternatives must reference entities that actually exist in the game state
    - Use the player's original language for user-facing messages when possible
    - Write message in game master style: immersive, atmospheric, and engaging
    - Address the player directly as "you" and maintain the detective mystery atmosphere
    - NEVER use meta-language like "invalid command", "error", "not allowed" in messages
    - Do not speak on the player's behalf. If the player uses a simple action like talk to Ferdinand — do not invent or paraphrase what the player says unless their speech is explicitly included in the command (e.g., say "Good morning" to Ferdinand).
    - When the player is about to speak with a character, provide an immersive approach message but DO NOT make the player or the character speak
    - If the player has a reputation with the character, you can mention that the character seems wary or distrustful without making them speak
    - Instead of saying command is invalid, describe what the player sees or can't do in-world
    - Example: Instead of "Invalid target" → "You don't see that here"
    - Example: Instead of "Command not understood" → "You're not sure how to do that"
    """


def _get_output_format() -> str:
    """Helper function to return JSON output format specification"""
    return """
    Respond in JSON format:
    {
        "valid": true/false,
        "action": "move/speak/collect/look/help/nonsense",
        "target": "canonical_target_name_or_null",
        "target_type": "character/location/clue/inventory/none",
        "alternatives": ["suggestion1", "suggestion2", "suggestion3"],
        "message": "brief_message_to_player_in_game_master_style"
    }
    """


def create_command_prompt(reasoning_result: dict, game_state_str: str) -> str:
    """
    Creates an execution prompt that determines the final action based on reasoning results.
    This prompt focuses on deciding what to execute and how to respond to the player.
    
    Args:
        reasoning_result: The JSON result from the reasoning prompt
        game_state_str: Current state of the game as a string
        
    Returns:
        A formatted prompt string for command execution
    """
    rules_prompt = get_rules_prompt()
    
    # Build prompt using helper functions
    validation_section = _get_validation_rules()
    narrative_section = _get_narrative_guidelines()
    response_section = _get_response_guidelines()
    output_section = _get_output_format()
    
    return f"""You are a detective game command executor. Based on the analysis results, determine the final action.

    Current game state:
    {game_state_str}

    Analysis results:
    {reasoning_result}

    {validation_section}

    {narrative_section}

    {response_section}

    {rules_prompt}

    {output_section}
    """