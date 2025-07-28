from typing import Dict, List, Optional

from game_engine.models.secret_list import Secret


class Character:
    def __init__(
        self,
        name: str,
        role: str,
        description: str,
        information_to_disclose: Optional[List[str]],
        traits: Optional[List[str]] = None,
        secrets: Optional[List[Secret]] = None,
        possible_locations: Optional[List[str]] = None,
        prompt: str = None,
        image_url: str = "",
        status: str = "alive",
    ):
        self.name: str = name
        self.role: str = role
        self.description: str = description
        self.information_to_disclose: List[str] = information_to_disclose or []
        self.traits: List[str] = traits or []
        self.secrets: List[Secret] = secrets or []
        self.possible_locations: List[str] = possible_locations or [
            "Main Hall"
        ]  # Default location if none provided
        self.memory_global: List[str] = []  # Stores a summary of past conversations
        self.memory_current: List[Dict[str, str]] = (
            []
        )  # Stores the ongoing conversation context
        self.dialogues: Dict[str, str] = {}  # Stores predefined dialogues
        self.image_url: str = image_url
        self.prompt: str = prompt
        self.status: str = status


    def remember(self, message: str, role: str = "user") -> None:
        """Add a message to the current conversation memory with the specified role."""
        if role not in {"user", "assistant"}:
            raise ValueError("Role must be either 'user' or 'assistant'.")

        self.memory_current.append({"role": role, "content": message})

    def summarize_and_store_memory(self, summary: str) -> None:
        """Summarize current memory and store it in global memory."""
        if self.memory_current:
            self.memory_global.append(summary)
            self.memory_current = []  # Reset current memory

    def speak(self, topic: str = "default") -> str:
        """Return the character's dialogue based on the topic."""
        return self.dialogues.get(topic, "I have nothing to say about that.")

    def add_dialogue(self, topic: str, response: str) -> None:
        """Add or update a dialogue for a given topic."""
        self.dialogues[topic] = response

    def update_status(self, new_status: str) -> None:
        """Update the character's status."""

        valid_statuses = ['alive', 'dead', 'unconscious', 'injured']

        if new_status in valid_statuses:
            self.status = new_status
        else:
            raise ValueError(f"Invalid status: {new_status}. Valid statuses are: {valid_statuses}")