"""
AI Personality Agent - Transforms neutral character responses with personality traits
"""

from dataclasses import dataclass
from typing import List


@dataclass
class PersonalityContext:
    """Context information for personality application"""

    character_name: str
    traits: List[str]
    role: str
    description: str


def generate_personality_instructions(traits: List[str]) -> str:
    """
    Generate specific instructions for how to apply personality traits to responses
    Args:
        traits: List of character personality traits
    Returns:
        Formatted string with personality application guidelines
    """
    trait_instructions = {
        "ambitious": "Show drive and goals",
        "opportunistic": "Look for advantages",
        "charming": "Be smooth and pleasant",
        "arrogant": "Act superior",
        "resentful": "Show bitterness",
        "determined": "Be firm and unwavering",
        "bumbling": "Stumble and self-correct",
        "good-hearted": "Be kind and caring",
        "earnest": "Be sincere",
        "accident-prone": "Be nervous",
        "melancholic": "Be sad and wistful",
        "reserved": "Be distant",
        "elegant": "Be refined",
        "authoritative": "Be commanding",
        "proud": "Maintain dignity",
        "traditional": "Reference proper behavior",
        "manipulative": "Be subtly cunning",
        "cold": "Be detached",
        "intelligent": "Be analytical",
        "observant": "Notice details",
        "devoted": "Show loyalty",
        "secretive": "Be vague",
        "loyal": "Defend others",
        "hardworking": "Mention duties",
        "honest": "Be direct",
        "gruff": "Be blunt",
        "contemptuous": "Show disdain and scorn",
    }

    instructions = []

    # Add primary trait emphasis
    if len(traits) > 0:
        primary_trait = traits[0].lower()
        instructions.append(
            f"PRIMARY PERSONALITY FOCUS - {traits[0].upper()}: {trait_instructions.get(primary_trait, 'Express this trait prominently')}"
        )

    # Add supporting traits
    for i, trait in enumerate(traits[1:], 1):
        trait_lower = trait.lower()
        if trait_lower in trait_instructions:
            instructions.append(
                f"Supporting trait - {trait}: {trait_instructions[trait_lower]}"
            )

    # Add integration guidance
    if len(traits) > 1:
        instructions.append(
            "INTEGRATION: Blend these traits naturally - they should complement each other, not compete"
        )

    return "\n".join(instructions)


# Utility function for easy integration
def create_personality_context(character) -> PersonalityContext:
    """
    Create a PersonalityContext from a character object
    Args:
        character: Character object with name, traits, role, description attributes
    Returns:
        PersonalityContext instance
    """
    return PersonalityContext(
        character_name=character.name,
        traits=character.traits,
        role=character.role,
        description=character.description,
    )
