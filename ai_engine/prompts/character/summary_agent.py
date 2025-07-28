"""
Summary Character Agent
Handles conversation summarization between detective and character
"""

from game_engine.models.character import Character
from game_engine.models.player import Player


def create_conversation_summary_prompt(character: Character, player: Player):
    """Create a prompt to generate a bullet-point summary of the entire conversation"""

    return f"""
    You are an AI assistant tasked with summarizing a conversation between a detective ({player.name}) and a character ({character.name}) in a detective game.

    Character information:
    - Name: {character.name}
    - Description: {character.description}

    Full conversation history:
    {character.memory_current}

    Please provide a structured summary of this conversation in bullet points. Your summary must:
    - Start directly with bullet points (no introduction or conclusion)
    - Be concise and focused on facts and relevant exchanges
    - Include the following types of points when applicable:
        - Main topics discussed or questions asked by the detective
        - Important information revealed by {character.name}
        - Any secrets that were disclosed or hinted at
        - Emotional reactions or changes in tone from {character.name}
        - Any clues, objects, or leads mentioned
        - Promises, suspicions, accusations, or future actions discussed

    Format each point as a short, standalone sentence (starting with a dash).
    Avoid repetition and keep the total summary under 150 words.
    """