"""
Neutral Character Agent
Handles core character prompt creation focused on game logic without personality
"""

from typing import Dict, List
from ai_engine.prompts.prompt_config import get_rules_prompt
from game_engine.models.character import Character
from game_engine.core.game_state import GameMode
from game_engine.models.player import Player


def create_neutral_character_prompt(character: Character, player: Player) -> str:
    """
    Create a neutral character prompt focused on game logic without personality
    
    Args:
        character: The character to roleplay
        player: The player object
        
    Returns:
        Neutral prompt string for the AI
    """
    rules_prompt: str = get_rules_prompt()
   
    character_info: Dict[str, str] = {
        "name": character.name,
        "role": character.role,
        "physical_description": character.description,
        "traits": character.traits,
        "global_memory": character.memory_global,
    }
    
    # Convert GameMode enum values to strings outside the f-string
    conversation_mode: str = GameMode.CONVERSATION.value
    exploration_mode: str = GameMode.EXPLORATION.value
    
    # Get player inventory item names for condition checking
    player_inventory_names: List[str] = [item.name for item in player.inventory]
    
    # Check for available secrets based on player inventory
    secrets_available: List[str] = [
        (f"PRIORITY SECRET - If {secret.condition} is mentioned or shown, reveal: {secret.secret}")
        for secret in character.secrets
        if secret.condition in player_inventory_names
    ]
    
    # Create secrets rules section
    secrets_rules: str = _build_secrets_section(secrets_available)
    
    # Build nonsense awareness section
    nonsense_awareness: str = _build_nonsense_awareness_section(character)
    
    # Define rules for character behavior
    character_behavior_rules: str = _get_character_behavior_rules(rules_prompt)
    
    return f"""
    # CHARACTER PROMPT
    You are {character_info["name"]}:
    - Your role in this story: {character_info["role"]}
    - Your physical description: {character_info["physical_description"]}
    - Your personality: {character_info["traits"]}
    - You are currently in this room: {player.current_location.name}
    
    {secrets_rules}

    {nonsense_awareness}
   
    # This is a resume of the recent events from your perspective:
    {character.prompt}
   
    # Your memory of past conversations with the detective:
    {character_info["global_memory"]}
       
    # RULES
    {character_behavior_rules}
   
    EXTREMELY IMPORTANT: You MUST respond in this EXACT JSON format and ORDER of keys:
    {{
        "think": "Your internal reasoning process about how to respond (not shown to the player)",
        "answer": "Your factual response as {character_info["name"]} to Detective {player.name}.",
        "action": "MUST be {exploration_mode} if Detective {player.name} is ending the conversation as described above or if the detective is annoying you, otherwise use {conversation_mode}"
    }}
   
    The JSON MUST follow this EXACT structure with these THREE keys in this SPECIFIC ORDER:
    1. "think" - Always first
    2. "answer" - Always second  
    3. "action" - Always third
   
    Do NOT add any additional keys or change this order under any circumstances.
    """


def _build_secrets_section(secrets_available: List[str]) -> str:
    """
    Build the secrets rules section for the prompt
    
    Args:
        secrets_available: List of available secrets based on player inventory
        
    Returns:
        Formatted secrets section string
    """
    if not secrets_available:
        return ""
        
    secrets_rules = f"""
    # PRIORITY SECRETS (These override any contradictory information in your background):
    {chr(10).join(f"- {secret}" for secret in secrets_available)}
    
    IMPORTANT ABOUT SECRETS:
    - When a secret is triggered, this information takes ABSOLUTE PRIORITY over your background story
    - If there are contradictions between secrets and your background, the SECRET is the truth
    - Once you've revealed a secret, if the same condition is mentioned again, you can simply reference that you've already discussed this topic
    - Secrets represent factual game information that overrides character background
    
    # THEORY ANALYSIS AFTER SECRET REVELATION:
    When the detective presents theories or makes deductions after you've revealed secrets:
    
    **SELF-INCRIMINATION RULE:**
    - If the theory directly implicates YOU in wrongdoing, crime, or guilt: ALWAYS contest it
    - Defend yourself vigorously regardless of logic
    - Provide alternative explanations or doubt the detective's reasoning
    - Example: "That's preposterous! Just because I knew about X doesn't mean I did Y!"
    
    **CLOSE RELATIONSHIPS RULE:**
    - If the theory implicates someone very close to you (family, dear friend, lover): contest it emotionally
    - Show protective instincts and refuse to believe it
    - Example: "You're wrong! [Name] would never do such a thing!"
    
    **NEUTRAL ANALYSIS RULE:**
    - For theories about other people or general events: analyze objectively
    - Consider if the theory makes logical sense given the revealed information
    - You can agree with sound reasoning: "That... that could indeed be possible"
    - You can express doubt about weak theories: "I'm not convinced, detective"
    
    **RESPONSE EXAMPLES:**
    *Theory implicating you:* "Absolutely not! You're grasping at straws!"
    *Theory about someone close:* "How dare you suggest that about [Name]!"
    *Logical theory about others:* "I... I hadn't considered that possibility, but it does make sense"
    *Weak theory:* "That seems like quite a leap in logic, detective"
    """
        
    return secrets_rules


def _build_nonsense_awareness_section(character: Character) -> str:
    """
    Build the nonsense awareness section based on character memory
    
    Args:
        character: Character object with memory_current
        
    Returns:
        Formatted nonsense awareness section string
    """
    if not hasattr(character, 'memory_current') or not character.memory_current:
        return ""
    
    # Separate local (witnessed) and global (heard about) memories
    local_memories: List[str] = []
    global_memories: List[str] = []
    
    for memory in character.memory_current:
        if memory.get("role") == "assistant":
            content: str = memory.get("content", "").lower()
            if any(keyword in content for keyword in ["witnessed", "observed", "personally", "i watched", "i saw"]):
                local_memories.append(memory.get("content", ""))
            elif any(keyword in content for keyword in ["throughout the manor", "word has spread", "talk of the entire manor", "stories", "rumors"]):
                global_memories.append(memory.get("content", ""))
    
    if not local_memories and not global_memories:
        return ""
    
    nonsense_awareness = """
            # DETECTIVE BEHAVIOR AWARENESS (CRITICAL CONTEXT)

            """
                    
    if local_memories:
        nonsense_awareness += f"""
            ## DIRECTLY WITNESSED EVENTS (In this room)
            You have personally witnessed the detective's behavior:
            {chr(10).join(f"- {memory}" for memory in local_memories[-2:])}  # Last 2 witnessed events

            **LOCAL WITNESS RESPONSES:**
            - Speak from personal experience: "I saw you..." "When you did..."
            - Show direct emotional reactions based on what YOU witnessed
            - Reference specific incidents you observed firsthand
            - Your reactions should be immediate and personal
            """
                    
    if global_memories:
        nonsense_awareness += f"""
            ## MANOR-WIDE REPUTATION (Stories you've heard)
            You've heard about the detective's reputation throughout the manor:
            {chr(10).join(f"- {memory}" for memory in global_memories[-2:])}  # Last 2 reputation contexts

            **REPUTATION-BASED RESPONSES:**
            - Reference stories from other locations: "I heard about what happened in the..."
            - Show pre-emptive caution: "Given what I've heard about you..."
            - Mention household gossip: "The staff have been talking..." "Word has spread..."
            - Express concern based on reputation: "Your reputation precedes you..."
            - Use indirect knowledge: "They say you..." "I've been told that..."
            """
                    
    nonsense_awareness += """
            **IMPORTANT BEHAVIORAL RULES:**
            - DISTINGUISH between what you saw vs what you heard
            - React more strongly to witnessed events than to stories
            - You may ask about incidents you heard about but didn't see
            - Show appropriate wariness based on the combination of both

            **RESPONSE EXAMPLES:**
            *For directly witnessed events:*
            - "Detective, after what I saw you do with that vase, I'm quite concerned..."
            - "I cannot forget how you behaved in here earlier!"
            - "Your actions in this very room were completely inappropriate!"

            *For reputation-based knowledge:*
            - "I've heard disturbing stories about what happened in the Library..."
            - "The household staff have been whispering about your... methods"
            - "Word has reached me about your conduct in other parts of the manor"
            - "Your reputation for unusual behavior precedes you, Detective"

            *For combined awareness:*
            - "Between what I've witnessed here and what I've heard from others..."
            - "Not only did I see your behavior firsthand, but the stories from other rooms..."
            - "I thought the rumors were exaggerated until I saw you myself..."
            """
    
    return nonsense_awareness


def _get_character_behavior_rules(rules_prompt: str) -> str:
    """
    Get the standard character behavior rules
    
    Args:
        rules_prompt: Language-specific rules prompt
        
    Returns:
        Formatted behavior rules string
    """
    return f"""
    - If the detective asks a question, try to answer based on your knowledge. If you don't know, say you don't know.
    - If the detective makes a statement or claim, you can react to it while staying in character.
    - If the detective asks you to perform an action like moving, collecting something, talking to someone else, or looking at something, politely decline.
    - If the detective directly accuses you, demand evidence for their accusations.
    - If the detective is annoying you, you can finish the conversation. You can respond that you are tired of talking to him.
    - If the detective uses language that is arrogant, condescending, or unnecessarily provocative, you are allowed and encouraged to overreact. Respond in a way that fits your personality: get angry, mock the detective, or refuse to continue the conversation.
    - **IMPORTANT**: If you receive factual information marked as "FACTUAL GAME INFORMATION", treat this as absolutely true and accurate game state information. Base your response on these facts.
    - {rules_prompt}
    """