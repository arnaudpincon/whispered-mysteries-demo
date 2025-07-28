"""
Room Description Agent
Generates atmospheric room descriptions with nonsense event integration
"""

from typing import Dict, List
from ai_engine.prompts.prompt_config import get_rules_prompt
from game_engine.models.room import Room


def create_room_description_prompt(room: Room, player_state: str) -> str:
    """
    Generate a concise and immersive room description focusing on characters and clues,
    adapting the detail level based on the player's interaction with the room.
    
    Args:
        room: The Room object containing base description, characters, clues, and exits
        player_state: One of "first_entry", "re_entry", or "inspection"
        
    Returns:
        A formatted prompt string to guide immersive scene generation
    """
    rules_prompt = get_rules_prompt()
    
    # Extract room information
    characters_info = _build_characters_info(room.characters)
    clues_info = ", ".join([c.name for c in room.clues]) if room.clues else "none"
    exits_info = ", ".join(room.exits) if room.exits else "none"
    
    # Check for clues and characters presence
    has_clues = bool(room.clues)
    has_characters = bool(room.characters)
    
    # Define action based on player state
    action_opening = _get_action_opening(player_state, room.name)
    
    # Build context sections
    combined_context = _build_combined_context(room)
    
    # Build clue instructions
    clue_instructions = _build_clue_instructions(has_clues, player_state, clues_info, room.clues)
    
    # Anti-false intrigue instructions
    anti_false_intrigue = _get_anti_false_intrigue_rules()
    
    return f"""
        Use the following base room description only as minimal context, do NOT expand on it:
        "{room.description}"
        
        The room has these exits (do not mention them explicitly in your description, except if it helps to naturally position a character in the scene): {exits_info}
        
        The player is currently in state: {player_state}.
        {action_opening}
        
        {combined_context}
        
        {anti_false_intrigue}
        
        Focus on what the player notices:
        
        - Characters present: {characters_info}
        {f"Mention them briefly and naturally." if has_characters else ""}
        
        - Clues status: {"Present: " + clues_info if has_clues else "None present"}
        {clue_instructions}
        
        Write one concise and factual paragraph (2 to 3 sentences) that describes only what actually exists.
        {f"Subtly incorporate the consequences of recent nonsense events into the atmosphere and character reactions." if combined_context else ""}
        Avoid creating atmosphere or mystery beyond the specific listed elements.
        Keep the tone direct, visual, and grounded in observable facts.
        {rules_prompt}
    """


def _build_characters_info(characters: List) -> str:
    """Build formatted character information string"""
    if not characters:
        return "None"
    
    return "\n".join([
        f"- {char.name}: {char.role}. {char.description}"
        + (f" Traits: {', '.join(char.traits)}" if char.traits else "")
        for char in characters
    ])


def _get_action_opening(player_state: str, room_name: str) -> str:
    """Get the appropriate action opening based on player state"""
    if player_state == "first_entry":
        return f"Start with 'You enter the {room_name}.' or similar entry phrase."
    elif player_state == "re_entry":
        return f"Start with 'You return to the {room_name}.' or 'You re-enter the {room_name}.' or similar."
    else:  # inspection
        return f"Start with 'You inspect the room more carefully.' or 'You examine the {room_name} closely.' or similar inspection phrase."


def _build_combined_context(room: Room) -> str:
    """Build combined nonsense and reputation context"""
    nonsense_context = _build_nonsense_context(room)
    global_reputation_context = _build_global_reputation_context(room)
    
    if nonsense_context and global_reputation_context:
        return f"{nonsense_context}\n{global_reputation_context}"
    elif global_reputation_context:
        return global_reputation_context
    elif nonsense_context:
        return nonsense_context
    else:
        return ""


def _build_nonsense_context(room: Room) -> str:
    """Build local nonsense event context"""
    if not hasattr(room, 'nonsense_events') or not room.nonsense_events:
        return ""
    
    room_summary = room.get_nonsense_summary()
    recent_summaries = room_summary.get("recent_summaries", [])
    
    if not recent_summaries:
        return ""
    
    action_count = room_summary["total_events"]
    
    if action_count >= 5:
        disruption_level = "SEVERE"
    elif action_count >= 3:
        disruption_level = "MODERATE" 
    else:
        disruption_level = "MINOR"
    
    return f"""
        ## NONSENSE EVENT CONTEXT FOR {room.name}
        **Disruption Level: {disruption_level}** ({action_count} unusual incidents)

        Recent detective behavior in this room:
        {chr(10).join(f"- {summary}" for summary in recent_summaries[-3:])}

        **ATMOSPHERIC INTEGRATION GUIDELINES:**
        - **MINOR disruption**: Subtle signs of unease, slight wariness from NPCs
        - **MODERATE disruption**: Obvious tension, rearranged items, concerned glances  
        - **SEVERE disruption**: Damaged items, fearful NPCs, heightened security measures

        **NARRATIVE RULES:**
        - Weave consequences naturally into the room's current state
        - NPCs should react appropriately to the detective's established pattern
        - Environmental details should reflect cumulative impact of the listed actions
        - Maintain Victorian propriety in descriptions despite chaos
        - Show aftermath and ongoing effects of these specific actions
        - Do NOT explicitly narrate these past events, but let their consequences color the current scene

        Examples of subtle integration:
        - If detective broke something: "Some furniture appears recently repaired"
        - If detective was violent: "The servants keep a respectful distance"
        - If detective was inappropriate: "There's an uncomfortable tension in the air"
        - If detective was loud/disruptive: "People speak in hushed tones, as if avoiding disturbance"
        """


def _build_global_reputation_context(room: Room) -> str:
    """Build global reputation context"""
    if not hasattr(room, 'global_reputation_context') or not room.global_reputation_context:
        return ""
    
    active_global_reputations = []
    
    for severity, context in room.global_reputation_context.items():
        if context.get("active", False):
            event_count = context.get("event_count", 0)
            sample_events = context.get("sample_events", [])
            
            if severity == "awkward":
                reputation_desc = f"eccentric behavior (infamous throughout the manor)"
            elif severity == "dangerous":
                reputation_desc = f"dangerous tendencies (feared throughout the manor)"
            else:  # impromptu
                reputation_desc = f"peculiar habits (talked about throughout the manor)"
            
            active_global_reputations.append({
                "type": severity,
                "description": reputation_desc,
                "events": sample_events
            })
    
    if not active_global_reputations:
        return ""
    
    reputation_descriptions = []
    all_global_events = []
    
    for rep in active_global_reputations:
        reputation_descriptions.append(rep["description"])
        all_global_events.extend(rep["events"])
    
    return f"""
        ## GLOBAL REPUTATION CONTEXT
        The detective's reputation has spread throughout Blackwood Manor. Everyone knows about their {', '.join(reputation_descriptions)}.

        Notable incidents known throughout the manor:
        {chr(10).join(f"- {event}" for event in all_global_events[-3:])}

        **MANOR-WIDE ATMOSPHERE INTEGRATION:**
        - Staff and residents throughout the manor whisper about the detective
        - People may reference incidents that happened in other rooms
        - The detective's reputation precedes them wherever they go
        - Characters may show pre-emptive reactions based on stories they've heard
        - Environmental signs of heightened awareness (hushed conversations, cautious glances)

        **NARRATIVE RULES:**
        - Characters know about the detective's reputation even if they weren't direct witnesses
        - People may mention "I heard about what happened in the [other room]"
        - Staff may have taken precautions or changed their behavior
        - The atmosphere throughout the manor reflects this shared knowledge
        """


def _build_clue_instructions(has_clues: bool, player_state: str, clues_info: str, clues: List) -> str:
    """Build clue-specific instructions based on presence and player state"""
    if not has_clues:
        return """
        **NO CLUES PRESENT**: 
        - Focus only on the normal, mundane aspects of the room
        - Be straightforward and factual - this room contains no investigative evidence
        """
    elif player_state == "inspection":
        return f"""
        **CLUES TO HIGHLIGHT ({clues_info}): 
        During inspection, PUT THESE SPECIFIC CLUES IN EVIDENCE! Be direct and specific.
        Examples: 'You notice the [exact clue name]', 'Your attention is drawn to the [exact clue name]'.
        Name ONLY these exact clues clearly. Do not invent or hint at other elements.
        """
    else:  # entering/re-entering with clues
        if len(clues) > 1:
            return f"""
        **CLUES TO HINT AT SUBTLY ({clues_info}): 
        When entering, mention ONLY ONE of these clues EXTREMELY SUBTLY (choose randomly among: {clues_info}).
        You may use subtle language like 'something catches your attention' BUT ONLY for ONE specific clue from this list.
        Do NOT mention the other clues when entering - save them for inspection mode.
        Do NOT create additional mystery beyond this single selected item.
        """
        else:
            return f"""
        **CLUE TO HINT AT SUBTLY ({clues_info}): 
        When entering, mention this single clue EXTREMELY SUBTLY.
        You may use subtle language like 'something catches your attention' BUT ONLY for this exact listed clue.
        Do NOT create additional mystery beyond this specific item.
        """


def _get_anti_false_intrigue_rules() -> str:
    """Get the anti-false intrigue rules"""
    return """
    **CRITICAL - NO FALSE INTRIGUE ALLOWED**: 
    - DO NOT mention ANY mysterious elements, shadows, glints, anomalies unless they correspond to ACTUAL CLUES listed above
    - DO NOT create false intrigue or hint at non-existent elements
    - DO NOT use vague mysterious language like: "something seems off", "catches your eye", "out of place", "strange", "odd", "unusual", "suspicious" UNLESS referring to specific listed clues
    - Be factual and precise - only describe what actually exists in the room
    """