"""
Lore Character Agent
Handles lore information retrieval from game state for character conversations
"""

from typing import Dict, List
from ai_engine.prompts.prompt_config import get_rules_prompt
from game_engine.models.character import Character
from game_engine.models.player import Player


def create_get_lore_information(
    game_state_str: str, player: Player, character: Character, topic: str
) -> str:
    """
    Create a prompt to get lore information from the game state.
    
    Args:
        game_state_str: String containing the game state information
        player: The player object with current location and inventory
        character: The character being addressed by the player
        topic: The topic to get information about
        
    Returns:
        A formatted string containing the full prompt for lore information
    """
    # Validate inputs
    _validate_lore_inputs(topic, game_state_str)
    
    # Build core rule section
    core_rule = _build_core_rule_section()
    
    # Build response criteria sections
    when_to_respond = _build_when_to_respond_section()
    when_not_to_respond = _build_when_not_to_respond_section()
    
    # Build response rules and formats
    response_rules = _build_response_rules_section()
    character_info_format = _build_character_info_format_section()
    special_cases = _build_special_cases_section()
    
    # Build examples section
    examples = _build_examples_section()
    
    # Build context section
    context = _build_context_section(character, player, topic)
    
    # Build game state section
    game_state_section = _build_game_state_section(game_state_str)
    
    return f"""You are a game state analyzer for a detective game.

{core_rule}

{when_to_respond}

{when_not_to_respond}

{response_rules}

{character_info_format}

{special_cases}

{examples}

{context}

{game_state_section}

Respond with factual information only, or empty string if no factual response needed."""


def _validate_lore_inputs(topic: str, game_state_str: str) -> None:
    """
    Validate inputs for lore information retrieval
    
    Args:
        topic: The topic to validate
        game_state_str: Game state string to validate
        
    Raises:
        ValueError: If inputs are invalid
    """
    if not topic.strip():
        raise ValueError("Topic cannot be empty")
    if not game_state_str.strip():
        raise ValueError("Game state cannot be empty")


def _build_core_rule_section() -> str:
    """
    Build the core rule section for lore analysis
    
    Returns:
        Core rule section string
    """
    return """# CORE RULE
Analyze the question and return ONLY factual information about existence or location of characters, places, or objects.
Return NOTHING for opinions, thoughts, or plot events.
**IMPORTANT: Always provide ALL relevant factual information found in the question, even if multiple elements are mentioned.**"""


def _build_when_to_respond_section() -> str:
    """
    Build the section defining when to respond
    
    Returns:
        When to respond section string
    """
    return """# WHEN TO RESPOND
Return information ONLY if the question asks about:
- WHO: existence of characters ("who is here?", "who lives in the manor?")
- WHERE: location of characters/objects ("where is X?", "is there a knife in the kitchen?")
- WHAT: verification of objects ("look at this knife", "do you see this book?")
- STATUS: character condition ("how is X?", "is X alive?")"""


def _build_when_not_to_respond_section() -> str:
    """
    Build the section defining when NOT to respond
    
    Returns:
        When not to respond section string
    """
    return """# WHEN NOT TO RESPOND
Return empty string for:
- Opinions ("what do you think?", "how do you feel?")
- Plot events ("who killed X?", "what happened?")
- Speculation ("why did X do that?")"""


def _build_response_rules_section() -> str:
    """
    Build the response rules section
    
    Returns:
        Response rules section string
    """
    return """# RESPONSE RULES

## Character Information Format
When mentioning characters, always include:
- Name
- Role 
- Physical description
- Current status (alive, dead, injured, unconscious)"""


def _build_character_info_format_section() -> str:
    """
    Build the character information format section
    
    Returns:
        Character info format section string
    """
    return """## Special Cases

### Same Room Detection
If a character is in the same room as the player:
"[Character name] is here ([status]), clearly visible right beside you."

### Inventory Verification
If player claims to have/show an object:
- First check player inventory using flexible matching
- Accept synonyms: "burned paper" = "burned journal page"
- If found in inventory: "The detective has [exact object name from game state]."
- If not in inventory, check current room objects
- If found in room: "The [exact object name from game state] is visible in the room but the detective has not yet examined or picked it up."
- If object not found anywhere: "The detective does not seem to have the mentioned object."

### Multiple Elements
If question mentions multiple characters, objects, or locations:
- Provide information for ALL mentioned elements
- Separate each piece of information clearly
- Example: "Martha (Governess, stern woman with grey bun, alive) is in the Study. The Resignation Letter is visible in the room but the detective has not yet examined or picked it up.\""""


def _build_special_cases_section() -> str:
    """
    Build the special cases section with inventory and multiple elements handling
    
    Returns:
        Special cases section string
    """
    return """## Multiple Elements
If question mentions multiple characters, objects, or locations:
- Provide information for ALL mentioned elements
- Separate each piece of information clearly
- Example: "Martha (Governess, stern woman with grey bun, alive) is in the Study. The Resignation Letter is visible in the room but the detective has not yet examined or picked it up.\""""


def _build_examples_section() -> str:
    """
    Build the comprehensive examples section
    
    Returns:
        Examples section string
    """
    return """# EXAMPLES

**Question:** "Where is Martha and do you see her resignation letter?"
**Response:** "Martha (Governess, stern woman with grey bun, alive) is in the Study. The Resignation Letter is visible in the room but the detective has not yet examined or picked it up."

**Question:** "Who else is in this room?"
**Response:** "Character A (Butler, tall elderly man with grey hair, alive), Character B (Maid, young woman in uniform, injured)"

**Question:** "Where is the cook?"
**Response:** "Cook Martha (Head Cook, stout woman with flour-stained apron, alive) is in the Kitchen"

**Question:** "Look at this bloody knife"
**Response:** "The detective has Kitchen Knife (bloodstained)." (if knife in inventory)
**Response:** "The Butcher's Knife is visible in the room but the detective has not yet examined or picked it up." (if knife in room but not in inventory)
**Response:** "The detective does not seem to have the mentioned object." (if knife not found anywhere)

**Question:** "What do you think about the murder?"
**Response:** (empty - opinion question)

**Question:** "Who lives in the manor?"
**Response:** "Lord Blackwood (Owner, distinguished gentleman with silver hair, alive), Lady Blackwood (Wife, elegant woman in silk dress, dead), Butler James (Head Butler, tall man in formal attire, alive)..."

**Question:** "How is Lord Blackwood?"
**Response:** "Lord Blackwood is currently alive\""""


def _build_context_section(character: Character, player: Player, topic: str) -> str:
    """
    Build the context section with character, player, and topic information
    
    Args:
        character: Character being addressed
        player: Player object
        topic: Topic being discussed
        
    Returns:
        Context section string
    """
    return f"""# CONTEXT
Player addressing: {character.name} ({character.role})
Current location: {player.current_location.name}
Question: "{topic}\""""


def _build_game_state_section(game_state_str: str) -> str:
    """
    Build the game state section
    
    Args:
        game_state_str: Formatted game state string
        
    Returns:
        Game state section string
    """
    return f"""# GAME STATE
{game_state_str}"""