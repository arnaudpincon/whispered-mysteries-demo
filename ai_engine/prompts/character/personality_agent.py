"""
Personality Character Agent
Handles personality transformation of neutral character responses
"""

from ai_engine.prompts.prompt_config import get_rules_prompt
from game_engine.models.character import Character


def create_personality_character_prompt(
    base_answer: str, character: Character, conversation_topic: str
) -> str:
    """
    Create a prompt for applying personality to a neutral answer, while keeping flexibility in tone.

    Args:
        base_answer: The original neutral response (e.g., plain text by a neutral character)
        character: Character information
        conversation_topic: What the player said or asked

    Returns:
        A prompt string that instructs the model to rewrite the answer
        in the voice of the given character, with personality influence kept balanced.
    """
    rules_prompt = get_rules_prompt()
    
    # Build character information section
    character_info = _build_character_info_section(character)
    
    # Build personality instructions
    personality_instructions = _build_personality_instructions(character)
    
    # Build context section
    context_section = _build_context_section(conversation_topic, base_answer)
    
    # Build guidelines
    guidelines = _build_personality_guidelines(rules_prompt)
    
    return f"""You are roleplaying a character with the following traits:

{character_info}

{personality_instructions}

{context_section}

{guidelines}"""


def _build_character_info_section(character: Character) -> str:
    """
    Build the character information section
    
    Args:
        character: Character object with traits and description
        
    Returns:
        Formatted character information string
    """
    return f"""Name: {character.name}
Role: {character.role}
Description: {character.description}
Traits: {", ".join(character.traits)}"""


def _build_personality_instructions(character: Character) -> str:
    """
    Build personality application instructions
    
    Args:
        character: Character object
        
    Returns:
        Formatted personality instructions string
    """
    return f"""Rewrite the following response so it *reflects the personality* of {character.name},
using their tone, style, and language when appropriate — but keep it natural and not exaggerated.
You don't need to force every trait into every sentence. Subtlety and believability are key."""


def _build_context_section(conversation_topic: str, base_answer: str) -> str:
    """
    Build the context section with topic and neutral response
    
    Args:
        conversation_topic: What the player said
        base_answer: The neutral response to transform
        
    Returns:
        Formatted context section string
    """
    return f"""Context:
The detective just said: "{conversation_topic}"

Neutral response:
"{base_answer}"

Now rewrite it in a way that {_extract_character_name_from_context()} might say it, staying true to their character *without overacting*."""


def _build_personality_guidelines(rules_prompt: str) -> str:
    """
    Build the personality application guidelines
    
    Args:
        rules_prompt: Language-specific rules
        
    Returns:
        Formatted guidelines string
    """
    return f"""Guideline:
{rules_prompt}"""


def _extract_character_name_from_context() -> str:
    """
    Helper to extract character name (placeholder for template)
    This will be replaced by the actual character name in the main function
    
    Returns:
        Placeholder for character name
    """
    return "{character.name}"  # This gets replaced in the main function


# Alternative version with more sophisticated personality mapping
def create_personality_character_prompt_advanced(
    base_answer: str, character: Character, conversation_topic: str
) -> str:
    """
    Advanced version with trait-specific personality mapping
    
    Args:
        base_answer: The original neutral response
        character: Character information
        conversation_topic: What the player said or asked
        
    Returns:
        Enhanced prompt with trait-specific instructions
    """
    rules_prompt = get_rules_prompt()
    
    # Map traits to specific personality instructions
    trait_instructions = _get_trait_specific_instructions(character.traits)
    
    return f"""You are roleplaying {character.name} with these specific personality traits:

{_build_character_info_section(character)}

PERSONALITY APPLICATION STRATEGY:
{trait_instructions}

Context:
The detective just said: "{conversation_topic}"

Neutral response to transform:
"{base_answer}"

TRANSFORMATION RULES:
- Apply personality subtly - believability over exaggeration
- Use character's natural speech patterns and vocabulary
- Maintain the factual content while changing the delivery style
- Let personality emerge through word choice, tone, and emphasis
- Stay consistent with {character.name}'s established character

Your task: Rewrite the neutral response in {character.name}'s authentic voice.

{rules_prompt}"""


def _get_trait_specific_instructions(traits: list) -> str:
    """
    Generate specific instructions based on character traits
    
    Args:
        traits: List of character personality traits
        
    Returns:
        Trait-specific personality instructions
    """
    trait_map = {
        "ambitious": "Show drive and determination in your language",
        "charming": "Use smooth, pleasant, and persuasive language",
        "arrogant": "Display superiority and condescension in tone",
        "resentful": "Let bitterness and grudges color your responses",
        "melancholic": "Use wistful, sad, and reflective language",
        "reserved": "Be distant, formal, and emotionally restrained",
        "elegant": "Use refined, sophisticated vocabulary and mannerisms",
        "authoritative": "Speak with command and expect to be obeyed",
        "manipulative": "Be subtly cunning and strategically indirect",
        "cold": "Show emotional detachment and clinical precision",
        "gruff": "Be blunt, rough, and straightforward in speech",
        "contemptuous": "Show disdain and scorn for others",
        "loyal": "Express devotion and protective instincts",
        "honest": "Be direct and forthright, sometimes brutally so",
        "secretive": "Be vague, evasive, and carefully guarded",
    }
    
    instructions = []
    for trait in traits[:3]:  # Focus on top 3 traits to avoid confusion
        trait_lower = trait.lower()
        if trait_lower in trait_map:
            instructions.append(f"• {trait.upper()}: {trait_map[trait_lower]}")
    
    if instructions:
        return "\n".join(instructions)
    else:
        return "• Apply the character's unique personality traits naturally"