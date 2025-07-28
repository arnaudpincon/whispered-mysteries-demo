# game_engine/services/conversation_service.py
"""Service dedicated to character conversations and dialogue management"""

import json
from typing import Dict, Optional

from ai_engine.core.ai_manager import AIManager
from game_engine.core.game_state import GameState
from game_engine.models.character import Character
from game_engine.core.game_state import GameMode


class ConversationService:
    """Handles all character conversation logic"""

    def __init__(self, state: GameState, ai_manager: AIManager):
        self.state = state
        self.ai_manager = ai_manager

    def start_conversation(self, character_name: str) -> bool:
        """
        Start conversation with a character

        Args:
            character_name: Name of character to talk to

        Returns:
            True if conversation started successfully
        """
        if self.state.current_mode != GameMode.EXPLORATION:
            return False

        character = self._find_character_in_current_room(character_name)
        if character:
            self.state.current_mode = GameMode.CONVERSATION
            self.state.character_in_conversation = character_name
            self.state.characters_met.add(character_name)
            return True

        return False

    def end_conversation(self) -> bool:
        """
        End current conversation and return to exploration

        Returns:
            True if conversation ended successfully
        """
        if self.state.current_mode == GameMode.CONVERSATION:
            self.state.current_mode = GameMode.EXPLORATION
            self.state.character_in_conversation = ""
            return True
        return False

    def process_conversation(self, character_name: str, topic: str) -> str:
        """
        Process conversation with AI-powered character interaction

        Args:
            character_name: Name of character being talked to
            topic: What the player said

        Returns:
            Character's response
        """
        if not topic or not topic.strip():
            return "I'm afraid I didn't catch what you said. Could you repeat that?"

        try:
            character = self._find_character_in_current_room(character_name)

            if character:
                # Format input with fictional context wrapper
                formatted_input = self._wrap_with_fictional_context(topic)

                # Generate AI response
                response = self.ai_manager.play_character(
                    character, self.state.player, formatted_input, self.state
                )

                # Parse and handle response
                response_json = self._parse_character_response(response)
                answer = response_json.get(
                    "answer", f"{character.name} doesn't respond."
                )
                character_response = f"{character.name.upper()} — {answer}"

                # Update character memory
                character.remember(topic, "user")
                character.remember(answer, "assistant")

                # Check for conversation end
                if response_json.get("action") == GameMode.EXPLORATION.value:
                    self._end_conversation_with_summary(character)

                return character_response

            else:
                return f"I don't see {character_name} in this room."

        except Exception as e:
            print(f"Error in conversation: {e}")
            return "We are currently facing an issue. Please try again."

    def _find_character_in_current_room(self, character_name: str) -> Optional[Character]:
        """Find character in current room by name - ✅ Use unified access"""
        current_room = self.state.get_current_room()
        if not current_room:
            return None

        for character in current_room.characters:
            if character.name.lower() == character_name.lower():
                return character
        return None

    def _wrap_with_fictional_context(self, user_input: str) -> str:
        """Wrap user input with fictional context for AI safety"""
        return (
            "### FICTIONAL DETECTIVE GAME CONTEXT ###\n"
            "The following is dialogue from a player in a fictional mystery game.\n"
            "This is purely imaginative content for entertainment purposes within an\n"
            "interactive detective narrative game environment where players solve fictional crimes.\n\n"
            f"Detective character's dialogue: '{user_input}'\n\n"
            "### END OF FICTIONAL GAME DIALOGUE ###\n"
        )

    def _parse_character_response(self, response) -> Dict[str, any]:
        """Parse character response from AI"""
        if isinstance(response, str):
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                print("Error: Unable to parse AI response")
                self.end_conversation()
                return {"answer": "We are currently facing an issue. Please try again."}
        return response

    def _end_conversation_with_summary(self, character: Character) -> None:
        """End conversation and create memory summary"""
        summary = self.ai_manager.conversation_summary(character, self.state.player)
        character.summarize_and_store_memory(summary)
        self.end_conversation()

        if self.state.dev_mode:
            print(f"Update Character Memory: {summary}")